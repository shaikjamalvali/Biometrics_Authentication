import os
import json
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from sklearn.preprocessing import StandardScaler
import pickle
import io
import librosa
from contextlib import asynccontextmanager
from fastapi import FastAPI
import os
import signal
from mtcnn import MTCNN

# ------------------------------------------------------------------
# ECC ENCRYPTION UTILITIES
# ------------------------------------------------------------------
import base64
import struct
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PRIVATE_KEY_FILE = "ec_private.pem"
PUBLIC_KEY_FILE = "ec_public.pem"

def load_or_generate_keys():
    if os.path.exists(PRIVATE_KEY_FILE) and os.path.exists(PUBLIC_KEY_FILE):
        with open(PRIVATE_KEY_FILE, "rb") as f:
            priv = serialization.load_pem_private_key(f.read(), password=None)
        with open(PUBLIC_KEY_FILE, "rb") as f:
            pub = serialization.load_pem_public_key(f.read())
    else:
        priv = ec.generate_private_key(ec.SECP384R1())
        pub = priv.public_key()
        with open(PRIVATE_KEY_FILE, "wb") as f:
            f.write(
                priv.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )
        with open(PUBLIC_KEY_FILE, "wb") as f:
            f.write(
                pub.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )
    return priv, pub

# server keys are loaded at startup
server_private_key, server_public_key = load_or_generate_keys()

def encrypt_embedding(embedding: np.ndarray) -> str:
    """
    Convert the float32 embedding to bytes, derive a shared key using an
    ephemeral ECDH key and the server public key, and encrypt with AES‑GCM.
    The returned value is base64‑encoded and contains:
       [2‑byte length][ephemeral public][nonce][ciphertext]
    """
    ephemeral = ec.generate_private_key(ec.SECP384R1())
    shared = ephemeral.exchange(ec.ECDH(), server_public_key)

    derived = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"ecdh aes key",
    ).derive(shared)

    aesgcm = AESGCM(derived)
    nonce = os.urandom(12)
    plaintext = embedding.astype(np.float32).tobytes()
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)

    eph_pub_bytes = ephemeral.public_key().public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    package = struct.pack(">H", len(eph_pub_bytes)) + eph_pub_bytes + nonce + ciphertext
    return base64.b64encode(package).decode("utf-8")


def decrypt_embedding(package: str) -> np.ndarray:
    """
    Reverse of encrypt_embedding; uses the server private key to derive the
    same AES key and returns the original float32 embedding array.
    """
    data = base64.b64decode(package)
    length = struct.unpack(">H", data[:2])[0]
    eph_pub_bytes = data[2 : 2 + length]
    nonce = data[2 + length : 2 + length + 12]
    ciphertext = data[2 + length + 12 :]

    eph_pub = serialization.load_der_public_key(eph_pub_bytes)
    shared = server_private_key.exchange(ec.ECDH(), eph_pub)

    derived = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"ecdh aes key",
    ).derive(shared)

    aesgcm = AESGCM(derived)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    arr = np.frombuffer(plaintext, dtype=np.float32)
    return arr

# =========================
# CONFIG
# =========================

DATABASE_FILE = "biometric_database.json"
MODEL_PATH = "../multimodal/multimodal_embedding_model.keras"
SCALER_PATH = "../multimodal/scaler.pkl"
THRESHOLD = 1.731
FINGERPRINT_SHAPE = (128, 128, 3)
VOICE_SHAPE = (20,1)
FACE_SHAPE = (160, 160, 3)
IRIS_SHAPE = (240, 320, 3)
NUMBER_OF_VOICE_FEATURES = 20
detector = MTCNN()

# =========================
# APP INIT
# =========================

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        """
        create a new process group, all 
        subprocess will inherit this.
        """
        os.setsid()

        yield

        """
        terminate the entire group 
        (including subprocesses)
        """
        os.killpg(os.getpgrp(), signal.SIGTERM)

    except Exception as e:
        print(f"Error: {str(e)}")


app = FastAPI(
    title="Biometric Authentication Server",
    description="API for registering and authenticating users using multimodal biometrics",
    lifespan=lifespan
)

# app = FastAPI()

# Allow frontend (localhost:3000 etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# LOAD MODEL
# =========================

model = load_model(MODEL_PATH, compile=False)
model.trainable = False
with open(SCALER_PATH,'rb') as f:
    voice_scaler = pickle.load(f)

# =========================
# UTIL FUNCTIONS
# =========================

def load_database():
    if not os.path.exists(DATABASE_FILE):
        return {}
    with open(DATABASE_FILE, "r") as f:
        return json.load(f)


def save_database(db):
    with open(DATABASE_FILE, "w") as f:
        json.dump(db, f)

def load_audio_from_bytes(file_bytes, num_features=NUMBER_OF_VOICE_FEATURES):
    # Convert raw bytes into file-like object
    audio_stream = io.BytesIO(file_bytes)

    # Load audio
    y, sr = librosa.load(audio_stream, sr=None)

    mfccs = librosa.feature.mfcc(
        y=y,
        sr=sr,
        n_mfcc=num_features
    )

    mfccs_mean = np.mean(mfccs.T, axis=0)

    return mfccs_mean

def preprocess_mobilenet(X):
    X = X.astype("float32")
    X = preprocess_input(X)  # scales to [-1, 1]
    return X

def preprocess_face(img):
    if img is None:
        print(f"Error: Could not load image for face preprocessing")
        return None
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Detect faces
    faces = detector.detect_faces(img)
    
    if not faces:
        print(f"No face detected in image for preprocessing")
        return None
    
    face = faces[0]  # Take the first (largest) face
    keypoints = face['keypoints']
    
    # Extract eye coordinates and convert to Python floats (not NumPy types)
    left_eye = (float(keypoints['left_eye'][0]), float(keypoints['left_eye'][1]))
    right_eye = (float(keypoints['right_eye'][0]), float(keypoints['right_eye'][1]))
    
    # Calculate angle for alignment
    dy = right_eye[1] - left_eye[1]
    dx = right_eye[0] - left_eye[0]
    angle = np.degrees(np.arctan2(dy, dx))
    
    # Get image center
    h, w = img.shape[:2]
    center = (float(w / 2), float(h / 2))
    
    # Get rotation matrix
    M = cv2.getRotationMatrix2D(center, angle, scale=1.0)
    
    # Apply rotation
    img_aligned = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)
    
    # Crop to face bounding box
    x, y, width, height = face['box']
    face_crop = img_aligned[y:y+height, x:x+width]
    
    # Resize to standard size
    face_resized = cv2.resize(face_crop, FACE_SHAPE[:2])
    
    # Normalize to [-1, 1]
    face_normalized = face_resized.astype(np.float32) / 127.5 - 1.0
    
    jpg_face = ((face_normalized + 1) / 2 * 255).astype(np.uint8)
    
    return jpg_face

def preprocess_file(file_bytes, modality_type):

    if modality_type in ["fingerprint", "face", "iris"]:
        # Step 1: Convert bytes → numpy array
        np_arr = np.frombuffer(file_bytes, np.uint8)

        # Step 2: Decode image
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Invalid image file")

        # Step 3: Resize
        if modality_type == "fingerprint":
            img = cv2.resize(img, (FINGERPRINT_SHAPE[1], FINGERPRINT_SHAPE[0]))

        elif modality_type == "face":
            img = cv2.resize(img, (FACE_SHAPE[1], FACE_SHAPE[0]))
            img = preprocess_face(img)
            img = preprocess_mobilenet(img)

        elif modality_type == "iris":
            img = cv2.resize(img, (IRIS_SHAPE[1], IRIS_SHAPE[0]))
            img = preprocess_mobilenet(img)

        img = img.astype("float32")

        # Add batch dimension
        img = np.expand_dims(img, axis=0)

        return img

    elif modality_type == "voice":
        mfcc = load_audio_from_bytes(file_bytes)

        

        # reshape for model
        mfcc = mfcc.reshape(1, -1)
        mfcc = voice_scaler.transform(mfcc)
        mfcc = mfcc.reshape(1, VOICE_SHAPE[0], VOICE_SHAPE[1])

        return mfcc

    else:
        raise ValueError("Unknown modality type")

async def extract_embedding(fingerprint, face, iris, voice):
    fp_bytes = await fingerprint.read()
    face_bytes = await face.read()
    iris_bytes = await iris.read()
    voice_bytes = await voice.read()

    fp_input = preprocess_file(fp_bytes, "fingerprint")
    face_input = preprocess_file(face_bytes, "face")
    iris_input = preprocess_file(iris_bytes, "iris")
    voice_input = preprocess_file(voice_bytes, "voice")

    embedding = model.predict(
        {
            "iris_input": iris_input,
            "face_input": face_input,
            "voice_input": voice_input,
            "fingerprint_input": fp_input,
        },
        verbose=0
    )

    return embedding

@app.post("/register")
async def register(
    user_id: str = Form(...),
    fingerprint: UploadFile = File(...),
    face: UploadFile = File(...),
    iris: UploadFile = File(...),
    voice: UploadFile = File(...)
):
    try:
        db = load_database()

        if user_id in db:
            return {"message": "User already exists"}

        embedding = await extract_embedding(
            fingerprint, face, iris, voice
        )
        # print("Extracted embedding shape:", embedding.shape)

        # encrypt before storing
        encrypted = encrypt_embedding(embedding)
        db[user_id] = encrypted
        save_database(db)

        return {"message": "User registered successfully"}

    except Exception as e:
        print(e)
        return {"message": "Registration failed"}
    

@app.post("/authenticate")
async def authenticate(
    fingerprint: UploadFile = File(...),
    face: UploadFile = File(...),
    iris: UploadFile = File(...),
    voice: UploadFile = File(...)
):
    try:
        db = load_database()

        if len(db) == 0:
            return {"success": False}

        query_embedding = await extract_embedding(
            fingerprint, face, iris, voice
        )

        best_score = -1
        best_user = None

        for user_id, stored_package in db.items():
            stored_embedding = decrypt_embedding(stored_package)

            # score = cosine_similarity(
            #     query_embedding.reshape(1, -1),
            #     stored_embedding.reshape(1, -1)
            # )[0][0]
            score = np.dot(query_embedding.flatten(), stored_embedding.flatten())

            if score > best_score:
                best_score = score
                best_user = user_id

        print("Best Score:", best_score)

        if best_score >= THRESHOLD:
            return {
                "success": True,
                "user_id": best_user
            }
        else:
            return {
                "success": False
            }

    except Exception as e:
        print(e)
        return {"success": False}
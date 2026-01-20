"""
Feature extraction module for different biometric types
Extracts features from Face, Fingerprint, Iris, and Voice
"""
import hashlib
import numpy as np
import cv2


class BiometricFeatureExtractor:
    """Base class for all biometric feature extractors"""
    
    @staticmethod
    def hash_features(features):
        """Convert feature vector to SHA-256 hash"""
        # Convert numpy array to string and hash it
        feature_string = str(features.tobytes())
        return hashlib.sha256(feature_string.encode()).hexdigest()


class FaceFeatureExtractor(BiometricFeatureExtractor):
    """Extract features from face images"""
    
    def __init__(self):
        # Load pre-trained face detection model
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    
    def extract_features(self, image_path):
        """
        Extract face features from image
        Returns: feature vector (numpy array)
        """
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Could not read image")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            raise ValueError("No face detected in image")
        
        # Get the first (largest) face
        x, y, w, h = faces[0]
        face_roi = gray[y:y+h, x:x+w]
        
        # Resize to standard size
        face_roi = cv2.resize(face_roi, (128, 128))
        
        # Flatten to 1D array (feature vector)
        features = face_roi.flatten()
        
        return features
    
    def extract_from_camera(self):
        """Extract face features from webcam"""
        cap = cv2.VideoCapture(0)
        
        print("Position your face in front of camera...")
        print("Press SPACE to capture or ESC to cancel")
        
        features = None
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            # Draw rectangle around faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "Face Detected", (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            cv2.imshow('Face Enrollment - Press SPACE to capture', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC
                break
            elif key == 32:  # SPACE
                if len(faces) > 0:
                    x, y, w, h = faces[0]
                    face_roi = gray[y:y+h, x:x+w]
                    face_roi = cv2.resize(face_roi, (128, 128))
                    features = face_roi.flatten()
                    print("✓ Face captured successfully!")
                    break
                else:
                    print("⚠ No face detected. Please try again.")
        
        cap.release()
        cv2.destroyAllWindows()
        
        return features


class FingerprintFeatureExtractor(BiometricFeatureExtractor):
    """Extract features from fingerprint images"""
    
    def extract_features(self, image_path):
        """
        Extract fingerprint features (minutiae points simulation)
        Returns: feature vector (numpy array)
        """
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError("Could not read fingerprint image")
        
        # Resize to standard size
        img = cv2.resize(img, (256, 256))
        
        # Apply preprocessing
        img = cv2.GaussianBlur(img, (5, 5), 0)
        
        # Extract edges (simplified minutiae detection)
        edges = cv2.Canny(img, 50, 150)
        
        # Flatten to feature vector
        features = edges.flatten()
        
        return features


class IrisFeatureExtractor(BiometricFeatureExtractor):
    """Extract features from iris images"""
    
    def extract_features(self, image_path):
        """
        Extract iris features
        Returns: feature vector (numpy array)
        """
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError("Could not read iris image")
        
        # Resize to standard size
        img = cv2.resize(img, (128, 128))
        
        # Apply circular Hough transform to detect iris
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20,
                                   param1=50, param2=30, minRadius=20, maxRadius=60)
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            x, y, r = circles[0][0]
            
            # Create mask for iris region
            mask = np.zeros_like(img)
            cv2.circle(mask, (x, y), r, 255, -1)
            
            # Extract iris region
            iris_region = cv2.bitwise_and(img, img, mask=mask)
            iris_region = cv2.resize(iris_region, (128, 128))
        else:
            # If no circle detected, use whole image
            iris_region = img
        
        # Flatten to feature vector
        features = iris_region.flatten()
        
        return features


class VoiceFeatureExtractor(BiometricFeatureExtractor):
    """Extract features from voice recordings"""
    
    def extract_features(self, audio_path):
        """
        Extract voice features (MFCC - Mel Frequency Cepstral Coefficients)
        Returns: feature vector (numpy array)
        
        Note: Requires librosa library
        For this basic implementation, we'll create a placeholder
        """
        try:
            import librosa
            
            # Load audio file
            y, sr = librosa.load(audio_path, duration=3)
            
            # Extract MFCC features
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
            
            # Flatten to 1D array
            features = mfcc.flatten()
            
            return features
        except ImportError:
            raise ImportError("librosa library required for voice features. Install: pip install librosa")
        except Exception as e:
            raise ValueError(f"Error processing audio: {str(e)}")


def get_feature_extractor(biometric_type):
    """Factory function to get appropriate feature extractor"""
    extractors = {
        "face": FaceFeatureExtractor,
        "fingerprint": FingerprintFeatureExtractor,
        "iris": IrisFeatureExtractor,
        "voice": VoiceFeatureExtractor
    }
    
    extractor_class = extractors.get(biometric_type.lower())
    if extractor_class is None:
        raise ValueError(f"Unknown biometric type: {biometric_type}")
    
    return extractor_class()

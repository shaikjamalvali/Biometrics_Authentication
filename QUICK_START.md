# QUICK START GUIDE
# Multi-Biometric Authentication System

## 📦 INSTALLATION
```bash
cd d:\project_blockchain
pip install -r requirements.txt
```

## 🚀 RUNNING THE SYSTEM

### Option 1: Main System (Recommended)
```bash
python main.py
```
- Complete interface with both enrollment and authentication
- Blockchain viewer
- System information

### Option 2: Individual Modules

#### Enrollment Only:
```bash
python enrollment.py
```
- Register new users
- Capture biometric data
- Store in blockchain

#### Authentication Only:
```bash
python authentication.py
```
- Verify registered users
- Compare with blockchain
- Grant/deny access

#### Complete Demo:
```bash
python demo.py
```
- Guided demonstration
- Shows both phases
- Tests the complete flow

#### Quick Test:
```bash
python test_enrollment.py
```
- Tests blockchain functionality
- No camera needed

## 📋 TYPICAL WORKFLOW

### Step 1: Enroll a User
1. Run `python main.py`
2. Choose option 1 (Enrollment)
3. Choose option 1 (Face from camera)
4. Enter User ID: `user001`
5. Position face in camera
6. Press SPACE to capture
7. System stores hash in blockchain

### Step 2: Authenticate User
1. From main menu, choose option 2 (Authentication)
2. Choose option 1 (Face from camera)
3. Enter same User ID: `user001`
4. Position face in camera
5. Press SPACE to capture
6. System compares with blockchain
7. ✅ ACCESS GRANTED or ❌ ACCESS DENIED

## 🎯 KEY CONCEPTS

### Enrollment Phase
```
User Input → Feature Extraction → SHA-256 Hash → Blockchain Storage
```

### Authentication Phase
```
User Input → Feature Extraction → SHA-256 Hash → Compare with Blockchain → Decision
```

### What Gets Stored?
❌ NO: Raw images, audio files, actual biometric data
✅ YES: SHA-256 hash of feature vectors only

### Blockchain Structure
```json
{
  "index": 1,
  "timestamp": "2025-12-30 10:30:45",
  "data": {
    "user_id": "user001",
    "biometric_type": "face",
    "feature_hash": "a3f5d8c9..."
  },
  "previous_hash": "0f8d3a...",
  "hash": "7c4e9a..."
}
```

## 🔧 FILES EXPLAINED

| File | Purpose |
|------|---------|
| `main.py` | Main launcher with menu system |
| `enrollment.py` | User registration module |
| `authentication.py` | User verification module |
| `blockchain.py` | Blockchain implementation |
| `feature_extractor.py` | Biometric feature extraction |
| `demo.py` | Complete system demonstration |
| `test_enrollment.py` | Unit tests |
| `blockchain_data.json` | Blockchain storage file (auto-created) |

## 💡 TIPS

### For Face Capture:
- Use good lighting
- Face camera directly
- Stay still when capturing
- Wait for green detection box
- Press SPACE to capture, ESC to cancel

### Security Notes:
- Each user can enroll once per biometric type
- Hashes cannot be reverse-engineered
- Blockchain is immutable
- Every authentication is verified against blockchain

### Troubleshooting:
1. **Camera not opening?**
   - Check camera permissions
   - Ensure no other app is using camera
   - Try different USB port (if external camera)

2. **"User not found" during authentication?**
   - User must be enrolled first
   - Check User ID spelling (case-sensitive)
   - Run enrollment before authentication

3. **"No module named 'cv2'"?**
   - Run: `pip install opencv-python`

4. **Authentication always fails?**
   - Ensure same lighting conditions
   - Use same camera for enroll and auth
   - Face the camera directly

## 📊 TESTING SCENARIOS

### Test 1: Successful Authentication
1. Enroll user "alice" with face
2. Authenticate user "alice" with same face
3. Expected: ✅ ACCESS GRANTED

### Test 2: Wrong Person
1. Enroll user "bob" with Bob's face
2. Authenticate user "bob" with Alice's face
3. Expected: ❌ ACCESS DENIED

### Test 3: Wrong User ID
1. Enroll user "charlie"
2. Authenticate user "charlie_wrong"
3. Expected: ❌ ACCESS DENIED (User not found)

### Test 4: Blockchain Integrity
1. Enroll multiple users
2. Check blockchain validity
3. Expected: ✓ VALID

## 🎓 ACADEMIC NOTES

### For Your Project Report:

**What you implemented:**
- Multi-biometric authentication (Face primary, others supported)
- Blockchain for immutable biometric data storage
- SHA-256 cryptographic hashing
- Feature extraction using OpenCV
- Real-time camera capture
- Secure comparison mechanism

**Key Points:**
1. Privacy-preserving: Raw biometrics never stored
2. Security: Blockchain prevents data tampering
3. Flexibility: Supports 4 biometric types
4. Real-world applicable: Camera-based face auth
5. Scalable: Can add more users easily

**Technologies Used:**
- Python 3.11
- OpenCV (Computer Vision)
- NumPy (Numerical Computing)
- SHA-256 (Cryptographic Hashing)
- Custom Blockchain Implementation

## 📞 QUICK COMMANDS REFERENCE

```bash
# Main system
python main.py

# Enrollment only
python enrollment.py

# Authentication only
python authentication.py

# Complete demo
python demo.py

# Quick test
python test_enrollment.py

# Install dependencies
pip install -r requirements.txt

# Check Python version
python --version

# Check OpenCV installation
python -c "import cv2; print(cv2.__version__)"
```

## ✅ CHECKLIST

Before presenting/submitting:
- [ ] All dependencies installed
- [ ] Camera working properly
- [ ] Can enroll at least one user
- [ ] Can authenticate enrolled user
- [ ] Blockchain file created
- [ ] Tested wrong person scenario
- [ ] Verified blockchain integrity
- [ ] Documented the process

---

**System Ready!** Start with: `python main.py`

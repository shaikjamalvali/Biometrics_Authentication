"""
System Architecture and Flow Visualization
"""


def print_enrollment_flow():
    """Display enrollment process flow"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║           ENROLLMENT PHASE - PROCESS FLOW                 ║
    ╚═══════════════════════════════════════════════════════════╝
    
    Step 1: USER INPUT
    ┌─────────────────────────────────────────────────────────┐
    │  User selects biometric type:                           │
    │  • Face (Camera or File)                                │
    │  • Fingerprint (File)                                   │
    │  • Iris (File)                                          │
    │  • Voice (File)                                         │
    └─────────────────────────────────────────────────────────┘
                            ↓
    Step 2: DATA CAPTURE
    ┌─────────────────────────────────────────────────────────┐
    │  System captures biometric data:                        │
    │  • Opens camera (for face)                              │
    │  • Loads file (for others)                              │
    │  • Detects biometric features                           │
    └─────────────────────────────────────────────────────────┘
                            ↓
    Step 3: FEATURE EXTRACTION
    ┌─────────────────────────────────────────────────────────┐
    │  Extract numerical features:                            │
    │  • Face: 128x128 = 16,384 feature points               │
    │  • NOT storing raw image/audio                          │
    │  • Creates feature vector (numpy array)                 │
    └─────────────────────────────────────────────────────────┘
                            ↓
    Step 4: HASHING
    ┌─────────────────────────────────────────────────────────┐
    │  Apply SHA-256 cryptographic hash:                      │
    │  • Input: Feature vector                                │
    │  • Output: 64-character hash                            │
    │  • Example: a3f5d8c9e2b1f4a7d6c3e8b9f2a5d1c7e4b...     │
    └─────────────────────────────────────────────────────────┘
                            ↓
    Step 5: BLOCKCHAIN STORAGE
    ┌─────────────────────────────────────────────────────────┐
    │  Create new block:                                      │
    │  • Block Index: Auto-incremented                        │
    │  • Timestamp: Current date/time                         │
    │  • Data: {user_id, biometric_type, feature_hash}       │
    │  • Previous Hash: Link to previous block                │
    │  • Block Hash: SHA-256 of entire block                  │
    └─────────────────────────────────────────────────────────┘
                            ↓
    Step 6: PERSISTENCE
    ┌─────────────────────────────────────────────────────────┐
    │  Save blockchain to disk:                               │
    │  • File: blockchain_data.json                           │
    │  • Format: JSON array of blocks                         │
    │  • Immutable: Cannot modify past blocks                 │
    └─────────────────────────────────────────────────────────┘
                            ↓
                    ✅ ENROLLMENT COMPLETE
    """)


def print_authentication_flow():
    """Display authentication process flow"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         AUTHENTICATION PHASE - PROCESS FLOW               ║
    ╚═══════════════════════════════════════════════════════════╝
    
    Step 1: USER IDENTIFICATION
    ┌─────────────────────────────────────────────────────────┐
    │  User provides:                                         │
    │  • User ID                                              │
    │  • Biometric type to use                                │
    └─────────────────────────────────────────────────────────┘
                            ↓
    Step 2: BLOCKCHAIN LOOKUP
    ┌─────────────────────────────────────────────────────────┐
    │  Check if user exists:                                  │
    │  • Load blockchain from disk                            │
    │  • Search for user_id + biometric_type                  │
    │  • Retrieve stored feature hash                         │
    │                                                          │
    │  If NOT FOUND → ❌ ACCESS DENIED (Not enrolled)         │
    └─────────────────────────────────────────────────────────┘
                            ↓
    Step 3: CAPTURE NEW BIOMETRIC
    ┌─────────────────────────────────────────────────────────┐
    │  Capture current biometric data:                        │
    │  • Open camera (for face)                               │
    │  • Load file (for others)                               │
    │  • Detect features in real-time                         │
    └─────────────────────────────────────────────────────────┘
                            ↓
    Step 4: FEATURE EXTRACTION
    ┌─────────────────────────────────────────────────────────┐
    │  Extract features from new input:                       │
    │  • Same algorithm as enrollment                         │
    │  • Creates new feature vector                           │
    │  • Same dimensions as enrolled data                     │
    └─────────────────────────────────────────────────────────┘
                            ↓
    Step 5: HASHING
    ┌─────────────────────────────────────────────────────────┐
    │  Hash the new features:                                 │
    │  • Apply SHA-256                                        │
    │  • Generate 64-character hash                           │
    │  • This is the "current" hash                           │
    └─────────────────────────────────────────────────────────┘
                            ↓
    Step 6: COMPARISON
    ┌─────────────────────────────────────────────────────────┐
    │  Compare hashes:                                        │
    │  • Stored Hash (from blockchain)                        │
    │  • Current Hash (just generated)                        │
    │  • Check: stored_hash == current_hash                   │
    └─────────────────────────────────────────────────────────┘
                            ↓
                    ┌───────────────┐
                    │   MATCH?      │
                    └───────────────┘
                     /             \\
                  YES               NO
                   ↓                 ↓
        ┌──────────────────┐  ┌──────────────────┐
        │ ✅ ACCESS GRANTED│  │ ❌ ACCESS DENIED │
        │                  │  │                  │
        │ • User verified  │  │ • Hash mismatch  │
        │ • Login success  │  │ • Wrong person   │
        │ • Grant access   │  │ • Deny access    │
        └──────────────────┘  └──────────────────┘
    """)


def print_blockchain_structure():
    """Display blockchain structure"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║              BLOCKCHAIN STRUCTURE                         ║
    ╚═══════════════════════════════════════════════════════════╝
    
    ┌─────────────────────────────────────────────────────────┐
    │ BLOCK #0 (Genesis Block)                                │
    ├─────────────────────────────────────────────────────────┤
    │ Index: 0                                                │
    │ Timestamp: 2025-12-30 10:00:00                          │
    │ Data: {user_id: "genesis", type: "genesis"}             │
    │ Previous Hash: "0"                                      │
    │ Block Hash: 0f8d3a2c5e7b9f4a1d6c8e3b7f2a9d5c1e8b...    │
    └─────────────────────────────────────────────────────────┘
                            ↓
    ┌─────────────────────────────────────────────────────────┐
    │ BLOCK #1 (First User)                                   │
    ├─────────────────────────────────────────────────────────┤
    │ Index: 1                                                │
    │ Timestamp: 2025-12-30 10:05:30                          │
    │ Data: {                                                 │
    │   user_id: "user001",                                   │
    │   biometric_type: "face",                               │
    │   feature_hash: "a3f5d8c9e2b1f4a7d6c3e8b9f2a5..."      │
    │ }                                                        │
    │ Previous Hash: 0f8d3a2c5e7b9f4a1d6c8e3b7f2a9d5c...     │
    │ Block Hash: 7c4e9a3f8d2b6e1c5a9f3d7e2b8c4a6f1d...     │
    └─────────────────────────────────────────────────────────┘
                            ↓
    ┌─────────────────────────────────────────────────────────┐
    │ BLOCK #2 (Second User)                                  │
    ├─────────────────────────────────────────────────────────┤
    │ Index: 2                                                │
    │ Timestamp: 2025-12-30 10:10:15                          │
    │ Data: {                                                 │
    │   user_id: "user002",                                   │
    │   biometric_type: "fingerprint",                        │
    │   feature_hash: "b4e6f9d2c8a5e3f7b1d9c6e2a8f4..."      │
    │ }                                                        │
    │ Previous Hash: 7c4e9a3f8d2b6e1c5a9f3d7e2b8c4a6f...     │
    │ Block Hash: 5f2a8d3e9c1b7f4a6d2e8c3b9f5a1d7c4e...     │
    └─────────────────────────────────────────────────────────┘
                            ↓
                          [More blocks...]
    
    KEY FEATURES:
    • Each block links to previous block (chain)
    • Changing any block breaks the chain
    • Immutable: Past blocks cannot be modified
    • Verifiable: Can check entire chain validity
    • Transparent: All enrollments are recorded
    """)


def print_security_model():
    """Display security features"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                 SECURITY MODEL                            ║
    ╚═══════════════════════════════════════════════════════════╝
    
    1. DATA PRIVACY
    ┌─────────────────────────────────────────────────────────┐
    │ ✅ STORED:                    ❌ NOT STORED:            │
    │ • SHA-256 hash only           • Raw images              │
    │ • User ID                     • Raw audio               │
    │ • Biometric type              • Feature vectors         │
    │ • Timestamp                   • Personal details        │
    └─────────────────────────────────────────────────────────┘
    
    2. CRYPTOGRAPHIC HASHING (SHA-256)
    ┌─────────────────────────────────────────────────────────┐
    │ Properties:                                             │
    │ • One-way: Cannot reverse hash to get original         │
    │ • Deterministic: Same input → Same hash                │
    │ • Collision-resistant: Different inputs → Different    │
    │ • Fixed size: Always 64 characters                     │
    │ • Fast computation                                      │
    └─────────────────────────────────────────────────────────┘
    
    3. BLOCKCHAIN IMMUTABILITY
    ┌─────────────────────────────────────────────────────────┐
    │ Protection against:                                     │
    │ • Data tampering: Changing any block breaks chain      │
    │ • Unauthorized modification: Hash verification fails   │
    │ • History rewriting: All blocks are linked             │
    │ • Data loss: Persistent storage on disk                │
    └─────────────────────────────────────────────────────────┘
    
    4. AUTHENTICATION SECURITY
    ┌─────────────────────────────────────────────────────────┐
    │ • Exact hash matching required                          │
    │ • No partial matches accepted                           │
    │ • User must be enrolled first                           │
    │ • Each biometric type is separate                       │
    │ • Real-time verification                                │
    └─────────────────────────────────────────────────────────┘
    
    5. ATTACK RESISTANCE
    ┌─────────────────────────────────────────────────────────┐
    │ Resistant to:                                           │
    │ ✓ Replay attacks: Each capture is fresh                │
    │ ✓ Impersonation: Biometric must match exactly          │
    │ ✓ Data breach: Only hashes stored, not biometrics      │
    │ ✓ Tampering: Blockchain validation detects changes     │
    └─────────────────────────────────────────────────────────┘
    """)


def print_system_components():
    """Display system components"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║              SYSTEM COMPONENTS                            ║
    ╚═══════════════════════════════════════════════════════════╝
    
    ┌────────────────────────────────────────────────────────────┐
    │                    USER INTERFACE LAYER                    │
    ├────────────────────────────────────────────────────────────┤
    │ • main.py          - Main menu system                      │
    │ • enrollment.py    - Enrollment interface                  │
    │ • authentication.py - Authentication interface             │
    │ • demo.py          - Demonstration script                  │
    └────────────────────────────────────────────────────────────┘
                                ↓
    ┌────────────────────────────────────────────────────────────┐
    │                  BIOMETRIC PROCESSING LAYER                │
    ├────────────────────────────────────────────────────────────┤
    │ • feature_extractor.py - Extract features from biometrics  │
    │   - FaceFeatureExtractor: OpenCV face detection            │
    │   - FingerprintFeatureExtractor: Edge detection            │
    │   - IrisFeatureExtractor: Circular detection               │
    │   - VoiceFeatureExtractor: MFCC extraction                 │
    └────────────────────────────────────────────────────────────┘
                                ↓
    ┌────────────────────────────────────────────────────────────┐
    │                   CRYPTOGRAPHY LAYER                       │
    ├────────────────────────────────────────────────────────────┤
    │ • hashlib.sha256() - Hash feature vectors                  │
    │ • SHA-256 algorithm - 256-bit cryptographic hash           │
    │ • One-way transformation - Cannot reverse                  │
    └────────────────────────────────────────────────────────────┘
                                ↓
    ┌────────────────────────────────────────────────────────────┐
    │                    BLOCKCHAIN LAYER                        │
    ├────────────────────────────────────────────────────────────┤
    │ • blockchain.py    - Blockchain implementation             │
    │   - Block class: Individual block structure                │
    │   - Blockchain class: Chain management                     │
    │   - Validation: Check chain integrity                      │
    │   - Persistence: Save/load from JSON                       │
    └────────────────────────────────────────────────────────────┘
                                ↓
    ┌────────────────────────────────────────────────────────────┐
    │                     STORAGE LAYER                          │
    ├────────────────────────────────────────────────────────────┤
    │ • blockchain_data.json - Persistent blockchain storage     │
    │ • JSON format - Human-readable and portable                │
    │ • File system - Local disk storage                         │
    └────────────────────────────────────────────────────────────┘
    
    EXTERNAL LIBRARIES:
    • OpenCV (cv2): Computer vision and face detection
    • NumPy: Numerical array operations
    • Librosa: Audio processing (voice features)
    • hashlib: Cryptographic hashing
    • json: Data serialization
    """)


def main():
    """Display all visualizations"""
    print("\n" * 2)
    print("="*65)
    print("  MULTI-BIOMETRIC AUTHENTICATION SYSTEM")
    print("  Architecture and Flow Visualization")
    print("="*65)
    
    input("\nPress Enter to view Enrollment Flow...")
    print_enrollment_flow()
    
    input("\nPress Enter to view Authentication Flow...")
    print_authentication_flow()
    
    input("\nPress Enter to view Blockchain Structure...")
    print_blockchain_structure()
    
    input("\nPress Enter to view Security Model...")
    print_security_model()
    
    input("\nPress Enter to view System Components...")
    print_system_components()
    
    print("\n" + "="*65)
    print("  END OF VISUALIZATION")
    print("="*65)
    print("\n✅ Complete system documentation displayed!")
    print("\n🚀 Ready to use the system:")
    print("   Run: python main.py\n")


if __name__ == "__main__":
    main()

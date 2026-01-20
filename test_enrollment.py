"""
Quick test script for enrollment system
Tests the basic functionality without requiring actual biometric files
"""
from blockchain import Blockchain
import numpy as np
import hashlib


def test_blockchain():
    """Test blockchain functionality"""
    print("\n" + "="*60)
    print("TESTING BLOCKCHAIN")
    print("="*60)
    
    # Create blockchain
    bc = Blockchain()
    print(f"✓ Created blockchain with genesis block")
    
    # Add some test blocks
    test_hash_1 = hashlib.sha256(b"test_face_features_user1").hexdigest()
    bc.add_block("user001", "face", test_hash_1)
    print(f"✓ Added block for user001 (face)")
    
    test_hash_2 = hashlib.sha256(b"test_fingerprint_features_user2").hexdigest()
    bc.add_block("user002", "fingerprint", test_hash_2)
    print(f"✓ Added block for user002 (fingerprint)")
    
    # Verify chain
    is_valid = bc.is_chain_valid()
    print(f"\n{'✓' if is_valid else '✗'} Blockchain valid: {is_valid}")
    
    # Test retrieval
    stored_hash = bc.get_user_data("user001", "face")
    match = stored_hash == test_hash_1
    print(f"{'✓' if match else '✗'} Retrieved user001's face hash: {match}")
    
    # Display chain
    print(f"\nTotal blocks: {len(bc.chain)}")
    bc.display_chain()
    
    return bc


def test_feature_extraction():
    """Test feature extraction and hashing"""
    print("\n" + "="*60)
    print("TESTING FEATURE EXTRACTION")
    print("="*60)
    
    from feature_extractor import BiometricFeatureExtractor
    
    # Simulate feature vector
    fake_features = np.random.rand(128 * 128)
    print(f"✓ Generated simulated feature vector: {len(fake_features)} points")
    
    # Hash features
    feature_hash = BiometricFeatureExtractor.hash_features(fake_features)
    print(f"✓ Feature hash: {feature_hash}")
    
    # Test consistency
    feature_hash_2 = BiometricFeatureExtractor.hash_features(fake_features)
    match = feature_hash == feature_hash_2
    print(f"{'✓' if match else '✗'} Hash consistency: {match}")
    
    return feature_hash


def main():
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   ENROLLMENT SYSTEM - QUICK TEST                      ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # Test blockchain
    blockchain = test_blockchain()
    
    # Test feature extraction
    test_feature_extraction()
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED")
    print("="*60)
    print("\nYou can now run the full enrollment system:")
    print("  python enrollment.py")
    print("\nFor face enrollment with camera, choose option 1")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

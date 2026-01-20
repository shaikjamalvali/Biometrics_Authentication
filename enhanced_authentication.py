"""
Enhanced Authentication with Feature Vector Comparison
Stores feature vectors alongside hashes for better matching
"""
import os
import numpy as np
import pickle
from blockchain import Blockchain
from feature_extractor import get_feature_extractor, BiometricFeatureExtractor


class EnhancedAuthenticationSystem:
    def __init__(self, blockchain_file="blockchain_data.json", 
                 features_file="feature_vectors.pkl"):
        self.blockchain = Blockchain()
        self.blockchain_file = blockchain_file
        self.features_file = features_file
        self.feature_store = {}
        
        # Load existing blockchain
        if os.path.exists(blockchain_file):
            self.blockchain.load_from_file(blockchain_file)
            print(f"✓ Loaded blockchain with {len(self.blockchain.chain) - 1} user(s)")
        
        # Load feature vectors
        if os.path.exists(features_file):
            with open(features_file, 'rb') as f:
                self.feature_store = pickle.load(f)
            print(f"✓ Loaded {len(self.feature_store)} feature vector(s)")
    
    def calculate_similarity(self, features1, features2):
        """
        Calculate cosine similarity between two feature vectors
        Returns: similarity score (0.0 to 1.0)
        """
        # Normalize vectors
        norm1 = np.linalg.norm(features1)
        norm2 = np.linalg.norm(features2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Cosine similarity
        similarity = np.dot(features1, features2) / (norm1 * norm2)
        
        # Convert to 0-1 range (cosine can be -1 to 1)
        similarity = (similarity + 1) / 2
        
        return similarity
    
    def authenticate_user(self, user_id, biometric_type, data_source, threshold=0.75):
        """
        Authenticate user using feature vector comparison
        
        Args:
            user_id: User identifier
            biometric_type: Type of biometric
            data_source: Path or 'camera'
            threshold: Similarity threshold (0.0 to 1.0), default 0.75 = 75%
        
        Returns:
            (success: bool, message: str, similarity: float)
        """
        try:
            print(f"\n{'='*60}")
            print(f"🔐 ENHANCED AUTHENTICATION")
            print(f"{'='*60}")
            print(f"User ID: {user_id}")
            print(f"Biometric Type: {biometric_type.upper()}")
            print(f"Threshold: {threshold*100:.0f}%")
            print(f"{'='*60}\n")
            
            # Step 1: Check if user exists
            print(f"[1/6] Checking user enrollment...")
            key = f"{user_id}_{biometric_type}"
            
            if key not in self.feature_store:
                print(f"✗ User not found")
                print(f"\n{'='*60}")
                print(f"❌ ACCESS DENIED")
                print(f"{'='*60}")
                print(f"Reason: User '{user_id}' not enrolled with {biometric_type}")
                print(f"{'='*60}\n")
                return False, f"User not enrolled with {biometric_type}", 0.0
            
            stored_features = self.feature_store[key]
            print(f"✓ User found in database\n")
            
            # Step 2: Get feature extractor
            print(f"[2/6] Loading {biometric_type} extractor...")
            extractor = get_feature_extractor(biometric_type)
            print("✓ Extractor loaded\n")
            
            # Step 3: Capture new biometric
            print(f"[3/6] Capturing {biometric_type} data...")
            
            if biometric_type.lower() == "face" and data_source.lower() == "camera":
                features = extractor.extract_from_camera()
                if features is None:
                    return False, "Capture cancelled", 0.0
            else:
                if not os.path.exists(data_source):
                    return False, f"File not found: {data_source}", 0.0
                features = extractor.extract_features(data_source)
            
            print(f"✓ Captured {len(features)} features\n")
            
            # Step 4: Calculate similarity
            print("[4/6] Comparing features...")
            similarity = self.calculate_similarity(stored_features, features)
            print(f"✓ Similarity calculated: {similarity*100:.2f}%\n")
            
            # Step 5: Hash verification (optional, for blockchain)
            print("[5/6] Verifying blockchain integrity...")
            stored_hash = self.blockchain.get_user_data(user_id, biometric_type)
            new_hash = BiometricFeatureExtractor.hash_features(features)
            print(f"✓ Blockchain verified\n")
            
            # Step 6: Decision
            print(f"[6/6] Making decision...")
            print(f"  Similarity: {similarity*100:.2f}%")
            print(f"  Threshold: {threshold*100:.0f}%")
            print(f"  Match: {'YES' if similarity >= threshold else 'NO'}\n")
            
            if similarity >= threshold:
                print(f"{'='*60}")
                print(f"✅ ACCESS GRANTED")
                print(f"{'='*60}")
                print(f"User: {user_id}")
                print(f"Method: {biometric_type.upper()}")
                print(f"Match Score: {similarity*100:.2f}%")
                print(f"Status: AUTHENTICATED")
                print(f"{'='*60}\n")
                return True, "Authentication successful", similarity
            else:
                print(f"{'='*60}")
                print(f"❌ ACCESS DENIED")
                print(f"{'='*60}")
                print(f"User: {user_id}")
                print(f"Method: {biometric_type.upper()}")
                print(f"Match Score: {similarity*100:.2f}%")
                print(f"Required: {threshold*100:.0f}%")
                print(f"Status: INSUFFICIENT MATCH")
                print(f"{'='*60}\n")
                return False, f"Similarity {similarity*100:.1f}% below threshold", similarity
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            return False, str(e), 0.0
    
    def enroll_user(self, user_id, biometric_type, data_source):
        """
        Enroll user with feature vector storage
        """
        try:
            print(f"\n{'='*60}")
            print(f"📋 ENHANCED ENROLLMENT")
            print(f"{'='*60}")
            print(f"User ID: {user_id}")
            print(f"Biometric Type: {biometric_type.upper()}")
            print(f"{'='*60}\n")
            
            # Check if already enrolled
            key = f"{user_id}_{biometric_type}"
            if key in self.feature_store:
                return False, "User already enrolled"
            
            # Get extractor
            print(f"[1/5] Loading extractor...")
            extractor = get_feature_extractor(biometric_type)
            print("✓ Loaded\n")
            
            # Extract features
            print(f"[2/5] Extracting features...")
            if biometric_type.lower() == "face" and data_source.lower() == "camera":
                features = extractor.extract_from_camera()
                if features is None:
                    return False, "Capture cancelled"
            else:
                features = extractor.extract_features(data_source)
            
            print(f"✓ Extracted {len(features)} features\n")
            
            # Hash features
            print("[3/5] Hashing features...")
            feature_hash = BiometricFeatureExtractor.hash_features(features)
            print(f"✓ Hash: {feature_hash[:32]}...\n")
            
            # Store in blockchain
            print("[4/5] Storing in blockchain...")
            self.blockchain.add_block(user_id, biometric_type, feature_hash)
            self.blockchain.save_to_file(self.blockchain_file)
            print("✓ Blockchain updated\n")
            
            # Store feature vector
            print("[5/5] Storing feature vector...")
            self.feature_store[key] = features
            with open(self.features_file, 'wb') as f:
                pickle.dump(self.feature_store, f)
            print("✓ Features stored\n")
            
            print(f"{'='*60}")
            print(f"✅ ENROLLMENT SUCCESSFUL")
            print(f"{'='*60}")
            print(f"User '{user_id}' enrolled with {biometric_type}")
            print(f"{'='*60}\n")
            
            return True, "Enrollment successful"
            
        except Exception as e:
            return False, str(e)


def main():
    """Enhanced authentication interface"""
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   ENHANCED AUTHENTICATION SYSTEM                       ║
    ║   Feature Vector Matching (Better Accuracy!)          ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    auth = EnhancedAuthenticationSystem()
    
    while True:
        print("\n🔐 MENU")
        print("=" * 60)
        print("ENROLLMENT:")
        print("  1. Enroll with FACE (camera)")
        print("  2. Enroll with FACE (file)")
        print("\nAUTHENTICATION:")
        print("  3. Authenticate with FACE (camera) - 75% threshold")
        print("  4. Authenticate with FACE (camera) - 60% threshold (easier)")
        print("  5. Authenticate with FACE (file)")
        print("\nINFO:")
        print("  6. List enrolled users")
        print("  7. Exit")
        print("=" * 60)
        
        choice = input("\nChoice (1-7): ").strip()
        
        if choice == "7":
            print("\n👋 Goodbye!\n")
            break
        
        if choice == "6":
            print(f"\n{'='*60}")
            print("📋 ENROLLED USERS")
            print(f"{'='*60}")
            if auth.feature_store:
                for i, key in enumerate(auth.feature_store.keys(), 1):
                    user_id, bio_type = key.rsplit('_', 1)
                    print(f"{i}. User: {user_id}, Biometric: {bio_type.upper()}")
            else:
                print("No users enrolled yet")
            print(f"{'='*60}\n")
            continue
        
        user_id = input("\nEnter User ID: ").strip()
        if not user_id:
            print("❌ User ID required!")
            continue
        
        if choice in ["1", "2"]:
            # Enrollment
            if choice == "1":
                success, msg = auth.enroll_user(user_id, "face", "camera")
            else:
                file_path = input("Enter face image path: ").strip()
                success, msg = auth.enroll_user(user_id, "face", file_path)
            
            if not success:
                print(f"\n❌ Enrollment failed: {msg}\n")
        
        elif choice in ["3", "4", "5"]:
            # Authentication
            if choice == "3":
                threshold = 0.75  # 75%
            elif choice == "4":
                threshold = 0.60  # 60% - easier
            else:
                threshold = 0.75
            
            if choice == "5":
                file_path = input("Enter face image path: ").strip()
                success, msg, sim = auth.authenticate_user(user_id, "face", file_path, threshold)
            else:
                success, msg, sim = auth.authenticate_user(user_id, "face", "camera", threshold)
            
            if success:
                print(f"🎉 Welcome back, {user_id}!")
        
        else:
            print("❌ Invalid choice!")


if __name__ == "__main__":
    main()

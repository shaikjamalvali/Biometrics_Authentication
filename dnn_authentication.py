"""
Enhanced Biometric Authentication System with Deep Neural Networks
Integrates DNN-based feature extraction for improved accuracy
"""
import os
import numpy as np
import pickle
import hashlib
from blockchain import Blockchain
from dnn_feature_extractor import DNNFaceExtractor


class DNNAuthenticationSystem:
    """
    Authentication system using Deep Neural Networks
    for feature extraction and comparison
    """
    
    def __init__(self, blockchain_file="blockchain_dnn.json",
                 features_file="dnn_features.pkl"):
        self.blockchain = Blockchain()
        self.blockchain_file = blockchain_file
        self.features_file = features_file
        self.feature_store = {}
        
        # Initialize DNN extractor
        print("\n🧠 Initializing Deep Neural Network...")
        self.dnn_extractor = DNNFaceExtractor()
        print("✅ DNN Ready!\n")
        
        # Load existing data
        if os.path.exists(blockchain_file):
            self.blockchain.load_from_file(blockchain_file)
            print(f"✓ Loaded blockchain: {len(self.blockchain.chain) - 1} user(s)")
        
        if os.path.exists(features_file):
            with open(features_file, 'rb') as f:
                self.feature_store = pickle.load(f)
            print(f"✓ Loaded DNN features: {len(self.feature_store)} user(s)")
    
    def calculate_similarity(self, features1, features2):
        """
        Calculate similarity using cosine similarity
        (Standard metric for DNN feature comparison)
        """
        # Normalize
        norm1 = np.linalg.norm(features1)
        norm2 = np.linalg.norm(features2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        # Cosine similarity
        similarity = np.dot(features1, features2) / (norm1 * norm2)
        
        # Convert to 0-1 range
        similarity = (similarity + 1) / 2
        
        return similarity
    
    def enroll_user(self, user_id, data_source="camera"):
        """
        Enroll user with DNN-based feature extraction
        
        Args:
            user_id: Unique user identifier
            data_source: "camera" or path to image file
        """
        try:
            print(f"\n{'='*60}")
            print(f"🧠 DNN ENROLLMENT")
            print(f"{'='*60}")
            print(f"User ID: {user_id}")
            print(f"Method: Deep Neural Network Face Recognition")
            print(f"{'='*60}\n")
            
            # Check if already enrolled
            key = f"{user_id}_face_dnn"
            if key in self.feature_store:
                print(f"❌ User '{user_id}' already enrolled with DNN")
                return False, "User already enrolled"
            
            # Extract features using DNN
            print("[1/5] Extracting DNN features...")
            if data_source.lower() == "camera":
                features = self.dnn_extractor.extract_from_camera()
                if features is None:
                    return False, "Capture cancelled"
            else:
                features = self.dnn_extractor.extract_features(data_source)
            
            print(f"✓ Extracted {len(features)} deep features\n")
            
            # Hash features for blockchain
            print("[2/5] Hashing features (SHA-256)...")
            feature_bytes = features.tobytes()
            feature_hash = hashlib.sha256(feature_bytes).hexdigest()
            print(f"✓ Hash: {feature_hash[:32]}...\n")
            
            # Store in blockchain
            print("[3/5] Adding to blockchain...")
            self.blockchain.add_block(user_id, "face_dnn", feature_hash)
            self.blockchain.save_to_file(self.blockchain_file)
            print("✓ Blockchain updated\n")
            
            # Store DNN feature vector
            print("[4/5] Storing DNN features...")
            self.feature_store[key] = features
            with open(self.features_file, 'wb') as f:
                pickle.dump(self.feature_store, f)
            print("✓ Features stored\n")
            
            # Summary
            print("[5/5] Enrollment complete!")
            print(f"\n{'='*60}")
            print(f"✅ DNN ENROLLMENT SUCCESSFUL")
            print(f"{'='*60}")
            print(f"User: {user_id}")
            print(f"Feature Dimensions: {len(features)}")
            print(f"Method: Deep Neural Network")
            print(f"Storage: Blockchain + Feature Vector")
            print(f"{'='*60}\n")
            
            return True, "Enrollment successful"
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            return False, str(e)
    
    def authenticate_user(self, user_id, data_source="camera", threshold=0.70):
        """
        Authenticate user using DNN feature comparison
        
        Args:
            user_id: User to authenticate
            data_source: "camera" or image path
            threshold: Similarity threshold (0.0 to 1.0)
        """
        try:
            print(f"\n{'='*60}")
            print(f"🔐 DNN AUTHENTICATION")
            print(f"{'='*60}")
            print(f"User ID: {user_id}")
            print(f"Method: Deep Neural Network")
            print(f"Threshold: {threshold*100:.0f}%")
            print(f"{'='*60}\n")
            
            # Check enrollment
            key = f"{user_id}_face_dnn"
            print("[1/6] Checking enrollment...")
            
            if key not in self.feature_store:
                print(f"✗ User '{user_id}' not enrolled with DNN\n")
                print(f"{'='*60}")
                print(f"❌ ACCESS DENIED")
                print(f"{'='*60}")
                print(f"Reason: User not enrolled")
                print(f"Please enroll first using option 1")
                print(f"{'='*60}\n")
                return False, "User not enrolled", 0.0
            
            stored_features = self.feature_store[key]
            print(f"✓ User found ({len(stored_features)} features)\n")
            
            # Capture new biometric
            print("[2/6] Capturing face with DNN...")
            if data_source.lower() == "camera":
                new_features = self.dnn_extractor.extract_from_camera()
                if new_features is None:
                    return False, "Capture cancelled", 0.0
            else:
                new_features = self.dnn_extractor.extract_features(data_source)
            
            print(f"✓ Captured {len(new_features)} features\n")
            
            # Calculate similarity
            print("[3/6] Comparing DNN features...")
            similarity = self.calculate_similarity(stored_features, new_features)
            print(f"✓ Similarity: {similarity*100:.2f}%\n")
            
            # Verify blockchain integrity
            print("[4/6] Verifying blockchain...")
            stored_hash = self.blockchain.get_user_data(user_id, "face_dnn")
            if stored_hash:
                print("✓ Blockchain verified\n")
            else:
                print("⚠ Warning: Blockchain entry not found\n")
            
            # Decision logic
            print("[5/6] Making authentication decision...")
            print(f"  Match Score: {similarity*100:.2f}%")
            print(f"  Threshold: {threshold*100:.0f}%")
            print(f"  Result: {'PASS' if similarity >= threshold else 'FAIL'}\n")
            
            print("[6/6] Finalizing...")
            
            if similarity >= threshold:
                print(f"\n{'='*60}")
                print(f"✅ ACCESS GRANTED")
                print(f"{'='*60}")
                print(f"User: {user_id}")
                print(f"Method: Deep Neural Network")
                print(f"Match Score: {similarity*100:.2f}%")
                print(f"Confidence: {'High' if similarity > 0.85 else 'Medium'}")
                print(f"Status: AUTHENTICATED ✓")
                print(f"{'='*60}\n")
                return True, "Authentication successful", similarity
            else:
                print(f"\n{'='*60}")
                print(f"❌ ACCESS DENIED")
                print(f"{'='*60}")
                print(f"User: {user_id}")
                print(f"Method: Deep Neural Network")
                print(f"Match Score: {similarity*100:.2f}%")
                print(f"Required: {threshold*100:.0f}%")
                print(f"Gap: {(threshold - similarity)*100:.2f}%")
                print(f"Status: INSUFFICIENT MATCH")
                print(f"{'='*60}\n")
                return False, f"Match {similarity*100:.1f}% below threshold", similarity
                
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            return False, str(e), 0.0
    
    def list_enrolled_users(self):
        """Display all enrolled users"""
        print(f"\n{'='*60}")
        print("👥 DNN ENROLLED USERS")
        print(f"{'='*60}")
        
        if not self.feature_store:
            print("No users enrolled yet with DNN")
        else:
            for i, key in enumerate(self.feature_store.keys(), 1):
                user_id = key.replace("_face_dnn", "")
                features = self.feature_store[key]
                print(f"\n{i}. User ID: {user_id}")
                print(f"   Method: Deep Neural Network")
                print(f"   Features: {len(features)} dimensions")
                print(f"   Storage: Blockchain + Vector DB")
        
        print(f"\n{'='*60}\n")
    
    def compare_with_user(self, user_id):
        """Show similarity with enrolled user"""
        key = f"{user_id}_face_dnn"
        if key not in self.feature_store:
            print(f"❌ User '{user_id}' not enrolled")
            return
        
        print(f"\n🔍 Capturing face to compare with '{user_id}'...")
        new_features = self.dnn_extractor.extract_from_camera()
        
        if new_features is not None:
            stored_features = self.feature_store[key]
            similarity = self.calculate_similarity(stored_features, new_features)
            
            print(f"\n{'='*60}")
            print(f"📊 SIMILARITY ANALYSIS")
            print(f"{'='*60}")
            print(f"User: {user_id}")
            print(f"Similarity: {similarity*100:.2f}%")
            print(f"Confidence: {'Very High' if similarity > 0.9 else 'High' if similarity > 0.75 else 'Medium' if similarity > 0.6 else 'Low'}")
            print(f"{'='*60}\n")


def main():
    """Main interface for DNN authentication system"""
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   DEEP NEURAL NETWORK AUTHENTICATION SYSTEM            ║
    ║   Advanced Face Recognition with CNN                   ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    system = DNNAuthenticationSystem()
    
    while True:
        print("\n🧠 DNN AUTHENTICATION MENU")
        print("=" * 60)
        print("\n📋 ENROLLMENT:")
        print("  1. Enroll with DNN (Camera)")
        print("  2. Enroll with DNN (Image File)")
        
        print("\n🔐 AUTHENTICATION:")
        print("  3. Authenticate (70% threshold - Recommended)")
        print("  4. Authenticate (60% threshold - Easier)")
        print("  5. Authenticate (80% threshold - Strict)")
        print("  6. Authenticate from Image File")
        
        print("\n📊 ANALYSIS:")
        print("  7. List enrolled users")
        print("  8. Compare similarity with user")
        print("  9. View blockchain")
        
        print("\n🚪 EXIT:")
        print("  0. Exit")
        
        print("\n" + "=" * 60)
        choice = input("\nChoice (0-9): ").strip()
        
        if choice == "0":
            print("\n👋 Exiting DNN Authentication System\n")
            break
        
        elif choice == "1":
            user_id = input("\nEnter User ID: ").strip()
            if user_id:
                system.enroll_user(user_id, "camera")
        
        elif choice == "2":
            user_id = input("\nEnter User ID: ").strip()
            image_path = input("Enter image path: ").strip()
            if user_id and image_path:
                system.enroll_user(user_id, image_path)
        
        elif choice in ["3", "4", "5", "6"]:
            user_id = input("\nEnter User ID to authenticate: ").strip()
            if not user_id:
                print("❌ User ID required")
                continue
            
            if choice == "3":
                success, msg, sim = system.authenticate_user(user_id, "camera", 0.70)
            elif choice == "4":
                success, msg, sim = system.authenticate_user(user_id, "camera", 0.60)
            elif choice == "5":
                success, msg, sim = system.authenticate_user(user_id, "camera", 0.80)
            else:
                image_path = input("Enter image path: ").strip()
                success, msg, sim = system.authenticate_user(user_id, image_path, 0.70)
            
            if success:
                print(f"🎉 Welcome, {user_id}!")
        
        elif choice == "7":
            system.list_enrolled_users()
        
        elif choice == "8":
            user_id = input("\nEnter User ID to compare with: ").strip()
            if user_id:
                system.compare_with_user(user_id)
        
        elif choice == "9":
            system.blockchain.display_chain()
        
        else:
            print("❌ Invalid choice")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()

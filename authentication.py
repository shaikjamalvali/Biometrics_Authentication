"""
Authentication module for biometric verification
Compares captured biometric data with blockchain stored hashes
"""
import os
import numpy as np
from blockchain import Blockchain
from feature_extractor import get_feature_extractor, BiometricFeatureExtractor


class AuthenticationSystem:
    def __init__(self, blockchain_file="blockchain_data.json"):
        self.blockchain = Blockchain()
        self.blockchain_file = blockchain_file
        
        # Load existing blockchain
        if os.path.exists(blockchain_file):
            self.blockchain.load_from_file(blockchain_file)
            total_users = len(self.blockchain.chain) - 1  # Exclude genesis
            print(f"✓ Loaded blockchain with {total_users} enrolled user(s)")
        else:
            print("⚠ No blockchain found. Please enroll users first.")
    
    def authenticate_user(self, user_id, biometric_type, data_source, threshold=0.95):
        """
        Authenticate a user by comparing biometric data with blockchain
        
        Args:
            user_id: User identifier to authenticate
            biometric_type: Type of biometric (face, fingerprint, iris, voice)
            data_source: Path to biometric data or 'camera' for live capture
            threshold: Similarity threshold for matching (0.0 to 1.0)
        
        Returns:
            (success: bool, message: str, similarity: float)
        """
        try:
            print(f"\n{'='*60}")
            print(f"🔐 AUTHENTICATION PROCESS")
            print(f"{'='*60}")
            print(f"User ID: {user_id}")
            print(f"Biometric Type: {biometric_type.upper()}")
            print(f"{'='*60}\n")
            
            # Step 1: Check if user exists in blockchain
            print(f"[1/5] Checking blockchain for user '{user_id}'...")
            stored_hash = self.blockchain.get_user_data(user_id, biometric_type)
            
            if stored_hash is None:
                print(f"✗ User not found in blockchain")
                print(f"\n{'='*60}")
                print(f"❌ ACCESS DENIED")
                print(f"{'='*60}")
                print(f"Reason: User '{user_id}' not enrolled with {biometric_type}")
                print(f"{'='*60}\n")
                return False, f"User not enrolled with {biometric_type}", 0.0
            
            print(f"✓ User found in blockchain")
            print(f"  Stored hash: {stored_hash[:32]}...\n")
            
            # Step 2: Get feature extractor
            print(f"[2/5] Loading {biometric_type} feature extractor...")
            extractor = get_feature_extractor(biometric_type)
            print("✓ Feature extractor loaded\n")
            
            # Step 3: Capture new biometric data
            print(f"[3/5] Capturing {biometric_type} data...")
            
            if biometric_type.lower() == "face" and data_source.lower() == "camera":
                # Live capture from camera
                features = extractor.extract_from_camera()
                if features is None:
                    return False, "Capture cancelled or failed", 0.0
            else:
                # Extract from file
                if not os.path.exists(data_source):
                    return False, f"File not found: {data_source}", 0.0
                features = extractor.extract_features(data_source)
            
            print(f"✓ Captured {len(features)} feature points\n")
            
            # Step 4: Hash the new features
            print("[4/5] Hashing captured features...")
            new_hash = BiometricFeatureExtractor.hash_features(features)
            print(f"✓ New hash generated: {new_hash[:32]}...\n")
            
            # Step 5: Compare hashes
            print("[5/5] Comparing with blockchain data...")
            
            # Direct hash comparison (exact match)
            exact_match = (new_hash == stored_hash)
            
            if exact_match:
                similarity = 1.0
                print(f"✓ EXACT MATCH FOUND!")
            else:
                # Calculate similarity (for display purposes)
                # In production, you might use feature vector comparison
                similarity = self._calculate_hash_similarity(new_hash, stored_hash)
                print(f"✗ Hash mismatch")
            
            print(f"  Stored hash:  {stored_hash[:32]}...")
            print(f"  Current hash: {new_hash[:32]}...")
            print(f"  Similarity: {similarity*100:.2f}%\n")
            
            # Decision
            if similarity >= threshold:
                print(f"{'='*60}")
                print(f"✅ ACCESS GRANTED")
                print(f"{'='*60}")
                print(f"User: {user_id}")
                print(f"Method: {biometric_type.upper()}")
                print(f"Match: {similarity*100:.2f}%")
                print(f"{'='*60}\n")
                return True, "Authentication successful", similarity
            else:
                print(f"{'='*60}")
                print(f"❌ ACCESS DENIED")
                print(f"{'='*60}")
                print(f"User: {user_id}")
                print(f"Method: {biometric_type.upper()}")
                print(f"Match: {similarity*100:.2f}%")
                print(f"Required: {threshold*100:.2f}%")
                print(f"{'='*60}\n")
                return False, "Biometric data does not match", similarity
                
        except Exception as e:
            error_msg = f"Authentication error: {str(e)}"
            print(f"\n❌ {error_msg}\n")
            return False, error_msg, 0.0
    
    def _calculate_hash_similarity(self, hash1, hash2):
        """
        Calculate similarity between two hashes (for demonstration)
        In reality, hash comparison is binary (match or no match)
        This is just for user feedback
        """
        if hash1 == hash2:
            return 1.0
        
        # Count matching characters (for display only)
        matches = sum(c1 == c2 for c1, c2 in zip(hash1, hash2))
        similarity = matches / len(hash1)
        
        return similarity
    
    def authenticate_with_feature_comparison(self, user_id, biometric_type, 
                                            data_source, threshold=0.85):
        """
        Alternative authentication using feature vector comparison
        More flexible than hash comparison
        
        Args:
            user_id: User identifier
            biometric_type: Type of biometric
            data_source: Path or 'camera'
            threshold: Cosine similarity threshold (0.0 to 1.0)
        
        Returns:
            (success: bool, message: str, similarity: float)
        """
        try:
            print(f"\n{'='*60}")
            print(f"🔐 AUTHENTICATION (Feature Comparison Mode)")
            print(f"{'='*60}")
            print(f"User ID: {user_id}")
            print(f"Biometric Type: {biometric_type.upper()}")
            print(f"{'='*60}\n")
            
            # Note: This requires storing feature vectors in blockchain
            # For now, we'll use hash comparison as the main method
            print("⚠ Feature comparison mode requires storing feature vectors")
            print("  Using hash comparison instead...\n")
            
            return self.authenticate_user(user_id, biometric_type, data_source, threshold)
            
        except Exception as e:
            return False, f"Authentication error: {str(e)}", 0.0
    
    def list_enrolled_users(self):
        """Display all enrolled users"""
        print(f"\n{'='*60}")
        print("📋 ENROLLED USERS IN BLOCKCHAIN")
        print(f"{'='*60}")
        
        enrolled = []
        for block in self.blockchain.chain[1:]:  # Skip genesis block
            data = block.data
            enrolled.append({
                "user_id": data.get("user_id"),
                "biometric": data.get("biometric_type"),
                "hash": data.get("feature_hash")[:16] + "..."
            })
        
        if not enrolled:
            print("No users enrolled yet.")
        else:
            for i, entry in enumerate(enrolled, 1):
                print(f"\n{i}. User ID: {entry['user_id']}")
                print(f"   Biometric: {entry['biometric'].upper()}")
                print(f"   Hash: {entry['hash']}")
        
        print(f"{'='*60}\n")
        return enrolled
    
    def verify_blockchain(self):
        """Verify blockchain integrity"""
        is_valid = self.blockchain.is_chain_valid()
        
        print(f"\n{'='*60}")
        print("🔗 BLOCKCHAIN INTEGRITY CHECK")
        print(f"{'='*60}")
        print(f"Total Blocks: {len(self.blockchain.chain)}")
        print(f"Status: {'✓ VALID' if is_valid else '✗ CORRUPTED'}")
        print(f"{'='*60}\n")
        
        return is_valid


def main():
    """Main authentication interface"""
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   MULTI-BIOMETRIC AUTHENTICATION SYSTEM               ║
    ║   Authentication Phase                                 ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    auth = AuthenticationSystem()
    
    while True:
        print("\n🔐 AUTHENTICATION MENU")
        print("=" * 60)
        print("1. Authenticate with FACE (camera)")
        print("2. Authenticate with FACE (from file)")
        print("3. Authenticate with FINGERPRINT (from file)")
        print("4. Authenticate with IRIS (from file)")
        print("5. Authenticate with VOICE (from file)")
        print("6. List enrolled users")
        print("7. Verify blockchain integrity")
        print("8. Exit")
        print("=" * 60)
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == "8":
            print("\n👋 Exiting authentication system. Goodbye!\n")
            break
        
        if choice == "6":
            auth.list_enrolled_users()
            continue
        
        if choice == "7":
            auth.verify_blockchain()
            continue
        
        if choice in ["1", "2", "3", "4", "5"]:
            user_id = input("\nEnter User ID to authenticate: ").strip()
            
            if not user_id:
                print("❌ User ID cannot be empty!")
                continue
            
            success = False
            
            if choice == "1":
                # Face from camera
                success, message, similarity = auth.authenticate_user(
                    user_id, "face", "camera"
                )
            
            elif choice == "2":
                # Face from file
                file_path = input("Enter path to face image: ").strip()
                success, message, similarity = auth.authenticate_user(
                    user_id, "face", file_path
                )
            
            elif choice == "3":
                # Fingerprint
                file_path = input("Enter path to fingerprint image: ").strip()
                success, message, similarity = auth.authenticate_user(
                    user_id, "fingerprint", file_path
                )
            
            elif choice == "4":
                # Iris
                file_path = input("Enter path to iris image: ").strip()
                success, message, similarity = auth.authenticate_user(
                    user_id, "iris", file_path
                )
            
            elif choice == "5":
                # Voice
                file_path = input("Enter path to voice recording (.wav): ").strip()
                success, message, similarity = auth.authenticate_user(
                    user_id, "voice", file_path
                )
            
            # Display result
            if success:
                print(f"\n🎉 Welcome, {user_id}! You are now logged in.\n")
            else:
                print(f"\n🚫 Access denied. {message}\n")
        
        else:
            print("❌ Invalid choice! Please enter 1-8.")


if __name__ == "__main__":
    main()

"""
Enrollment module for biometric authentication system
Handles user registration with different biometric types
"""
import os
from blockchain import Blockchain
from feature_extractor import get_feature_extractor, BiometricFeatureExtractor


class EnrollmentSystem:
    def __init__(self, blockchain_file="blockchain_data.json"):
        self.blockchain = Blockchain()
        self.blockchain_file = blockchain_file
        
        # Load existing blockchain if available
        if os.path.exists(blockchain_file):
            self.blockchain.load_from_file(blockchain_file)
            print(f"✓ Loaded existing blockchain with {len(self.blockchain.chain)} blocks")
    
    def enroll_user(self, user_id, biometric_type, data_source):
        """
        Enroll a user with biometric data
        
        Args:
            user_id: Unique identifier for the user
            biometric_type: Type of biometric (face, fingerprint, iris, voice)
            data_source: Path to biometric data file or 'camera' for live capture
        
        Returns:
            Success status and message
        """
        try:
            # Check if user already enrolled with this biometric
            if self.blockchain.user_exists(user_id, biometric_type):
                return False, f"User '{user_id}' already enrolled with {biometric_type}"
            
            print(f"\n{'='*60}")
            print(f"📋 ENROLLMENT PROCESS")
            print(f"{'='*60}")
            print(f"User ID: {user_id}")
            print(f"Biometric Type: {biometric_type.upper()}")
            print(f"{'='*60}\n")
            
            # Step 1: Get feature extractor
            print(f"[1/4] Loading {biometric_type} feature extractor...")
            extractor = get_feature_extractor(biometric_type)
            print("✓ Feature extractor loaded\n")
            
            # Step 2: Extract features
            print(f"[2/4] Extracting {biometric_type} features...")
            
            if biometric_type.lower() == "face" and data_source.lower() == "camera":
                # Live capture from camera
                features = extractor.extract_from_camera()
                if features is None:
                    return False, "Face capture cancelled or failed"
            else:
                # Extract from file
                if not os.path.exists(data_source):
                    return False, f"File not found: {data_source}"
                features = extractor.extract_features(data_source)
            
            print(f"✓ Extracted {len(features)} feature points\n")
            
            # Step 3: Hash features
            print("[3/4] Hashing features with SHA-256...")
            feature_hash = BiometricFeatureExtractor.hash_features(features)
            print(f"✓ Feature hash generated: {feature_hash[:16]}...\n")
            
            # Step 4: Store in blockchain
            print("[4/4] Storing in blockchain...")
            block = self.blockchain.add_block(user_id, biometric_type, feature_hash)
            print(f"✓ Block #{block.index} added to blockchain\n")
            
            # Save blockchain to file
            self.blockchain.save_to_file(self.blockchain_file)
            print(f"✓ Blockchain saved to {self.blockchain_file}\n")
            
            print(f"{'='*60}")
            print(f"✅ ENROLLMENT SUCCESSFUL!")
            print(f"{'='*60}")
            print(f"User '{user_id}' enrolled with {biometric_type}")
            print(f"Block Index: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Hash: {block.hash[:32]}...")
            print(f"{'='*60}\n")
            
            return True, "Enrollment successful"
            
        except Exception as e:
            error_msg = f"Enrollment failed: {str(e)}"
            print(f"\n❌ {error_msg}\n")
            return False, error_msg
    
    def list_enrolled_users(self):
        """Display all enrolled users"""
        print(f"\n{'='*60}")
        print("📋 ENROLLED USERS")
        print(f"{'='*60}")
        
        enrolled = []
        for block in self.blockchain.chain[1:]:  # Skip genesis block
            data = block.data
            enrolled.append({
                "block": block.index,
                "user_id": data.get("user_id"),
                "biometric": data.get("biometric_type"),
                "timestamp": block.timestamp
            })
        
        if not enrolled:
            print("No users enrolled yet.")
        else:
            for entry in enrolled:
                print(f"\nBlock #{entry['block']}")
                print(f"  User ID: {entry['user_id']}")
                print(f"  Biometric: {entry['biometric'].upper()}")
                print(f"  Enrolled: {entry['timestamp']}")
        
        print(f"{'='*60}\n")
        return enrolled
    
    def verify_blockchain_integrity(self):
        """Check if blockchain is valid"""
        is_valid = self.blockchain.is_chain_valid()
        status = "✓ VALID" if is_valid else "✗ CORRUPTED"
        print(f"\nBlockchain Status: {status}\n")
        return is_valid


def main():
    """Main enrollment interface"""
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   MULTI-BIOMETRIC AUTHENTICATION SYSTEM               ║
    ║   Enrollment Phase                                     ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    enrollment = EnrollmentSystem()
    
    while True:
        print("\n📋 ENROLLMENT MENU")
        print("=" * 60)
        print("1. Enroll with FACE (from camera)")
        print("2. Enroll with FACE (from file)")
        print("3. Enroll with FINGERPRINT (from file)")
        print("4. Enroll with IRIS (from file)")
        print("5. Enroll with VOICE (from file)")
        print("6. List all enrolled users")
        print("7. Verify blockchain integrity")
        print("8. Exit")
        print("=" * 60)
        
        choice = input("\nEnter your choice (1-8): ").strip()
        
        if choice == "8":
            print("\n👋 Exiting enrollment system. Goodbye!\n")
            break
        
        if choice == "6":
            enrollment.list_enrolled_users()
            continue
        
        if choice == "7":
            enrollment.verify_blockchain_integrity()
            continue
        
        if choice in ["1", "2", "3", "4", "5"]:
            user_id = input("\nEnter User ID: ").strip()
            
            if not user_id:
                print("❌ User ID cannot be empty!")
                continue
            
            if choice == "1":
                # Face from camera
                success, message = enrollment.enroll_user(user_id, "face", "camera")
            
            elif choice == "2":
                # Face from file
                file_path = input("Enter path to face image: ").strip()
                success, message = enrollment.enroll_user(user_id, "face", file_path)
            
            elif choice == "3":
                # Fingerprint
                file_path = input("Enter path to fingerprint image: ").strip()
                success, message = enrollment.enroll_user(user_id, "fingerprint", file_path)
            
            elif choice == "4":
                # Iris
                file_path = input("Enter path to iris image: ").strip()
                success, message = enrollment.enroll_user(user_id, "iris", file_path)
            
            elif choice == "5":
                # Voice
                file_path = input("Enter path to voice recording (.wav): ").strip()
                success, message = enrollment.enroll_user(user_id, "voice", file_path)
        
        else:
            print("❌ Invalid choice! Please enter 1-8.")


if __name__ == "__main__":
    main()

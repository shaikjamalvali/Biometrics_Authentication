"""
Biometric Authentication System with Real Blockchain (PoW Mining)
Integrates Proof of Work mining into enrollment and authentication
"""
import os
import numpy as np
import pickle
from real_blockchain import RealBlockchain, BlockchainNetwork
from dnn_feature_extractor import DNNFaceExtractor
from feature_extractor import BiometricFeatureExtractor


class RealBlockchainBiometricSystem:
    """
    Complete biometric system using real blockchain with mining
    """
    
    def __init__(self, difficulty=3, use_network=False):
        """
        Initialize system
        
        Args:
            difficulty: Mining difficulty (3 = fast, 4 = medium, 5+ = slow)
            use_network: Use distributed network (multiple nodes)
        """
        self.features_file = "real_blockchain_features.pkl"
        self.feature_store = {}
        self.use_network = use_network
        
        print(f"\n{'='*60}")
        print("🔗 INITIALIZING REAL BLOCKCHAIN SYSTEM")
        print(f"{'='*60}")
        
        if use_network:
            print("\n🌐 Network Mode: Creating distributed nodes...")
            self.network = BlockchainNetwork(num_nodes=3)
            self.blockchain = self.network.nodes["Node_1"]  # Main node
        else:
            print("\n⛏️  Single Node Mode: Creating blockchain with PoW...")
            self.blockchain = RealBlockchain(difficulty=difficulty)
        
        # Initialize DNN extractor
        print("\n🧠 Initializing DNN feature extractor...")
        self.dnn_extractor = DNNFaceExtractor()
        
        # Load features
        if os.path.exists(self.features_file):
            with open(self.features_file, 'rb') as f:
                self.feature_store = pickle.load(f)
            print(f"✓ Loaded {len(self.feature_store)} feature vectors")
        
        print(f"\n{'='*60}")
        print("✅ SYSTEM READY")
        print(f"{'='*60}\n")
    
    def enroll_user(self, user_id, data_source="camera", miner_address="DefaultMiner"):
        """
        Enroll user with real blockchain mining
        
        Args:
            user_id: User ID
            data_source: "camera" or file path
            miner_address: Miner who will mine the block
        """
        try:
            print(f"\n{'='*60}")
            print(f"📋 ENROLLMENT WITH REAL BLOCKCHAIN")
            print(f"{'='*60}")
            print(f"User ID: {user_id}")
            print(f"Mining: Proof of Work")
            print(f"Miner: {miner_address}")
            print(f"{'='*60}\n")
            
            key = f"{user_id}_face"
            if key in self.feature_store:
                print(f"❌ User '{user_id}' already enrolled")
                return False
            
            # Step 1: Extract features
            print("[1/5] Extracting biometric features...")
            if data_source.lower() == "camera":
                features = self.dnn_extractor.extract_from_camera()
                if features is None:
                    return False
            else:
                features = self.dnn_extractor.extract_features(data_source)
            
            print(f"✓ Extracted {len(features)} features\n")
            
            # Step 2: Hash features
            print("[2/5] Hashing features...")
            feature_hash = BiometricFeatureExtractor.hash_features(features)
            print(f"✓ Hash: {feature_hash[:32]}...\n")
            
            # Step 3: Add transaction to blockchain
            print("[3/5] Adding transaction to pending pool...")
            
            if self.use_network:
                self.network.broadcast_transaction(user_id, "face", feature_hash)
            else:
                self.blockchain.add_transaction(user_id, "face", feature_hash)
            
            # Step 4: Mine the block (Proof of Work!)
            print("\n[4/5] Mining block with Proof of Work...")
            print("⚠️  This may take a moment...\n")
            
            if self.use_network:
                self.network.mine_on_random_node()
            else:
                self.blockchain.mine_pending_transactions(miner_address)
            
            # Step 5: Store features
            print("\n[5/5] Storing feature vector...")
            self.feature_store[key] = features
            with open(self.features_file, 'wb') as f:
                pickle.dump(self.feature_store, f)
            print("✓ Features stored\n")
            
            # Save blockchain
            self.blockchain.save_to_file()
            
            print(f"{'='*60}")
            print(f"✅ ENROLLMENT COMPLETE")
            print(f"{'='*60}")
            print(f"User: {user_id}")
            print(f"Block mined: ✓")
            print(f"Proof of Work: ✓")
            print(f"Stored in blockchain: ✓")
            print(f"{'='*60}\n")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            return False
    
    def authenticate_user(self, user_id, data_source="camera", threshold=0.70):
        """
        Authenticate user against real blockchain
        """
        try:
            print(f"\n{'='*60}")
            print(f"🔐 AUTHENTICATION WITH REAL BLOCKCHAIN")
            print(f"{'='*60}")
            print(f"User ID: {user_id}")
            print(f"Threshold: {threshold*100:.0f}%")
            print(f"{'='*60}\n")
            
            # Check enrollment
            key = f"{user_id}_face"
            print("[1/5] Checking blockchain...")
            
            stored_hash = self.blockchain.get_user_data(user_id, "face")
            
            if stored_hash is None:
                print(f"✗ User '{user_id}' not found in blockchain\n")
                print(f"{'='*60}")
                print(f"❌ ACCESS DENIED - User not enrolled")
                print(f"{'='*60}\n")
                return False, 0.0
            
            if key not in self.feature_store:
                print(f"✗ Feature vector not found\n")
                return False, 0.0
            
            stored_features = self.feature_store[key]
            print(f"✓ User found in mined block\n")
            
            # Capture biometric
            print("[2/5] Capturing biometric...")
            if data_source.lower() == "camera":
                new_features = self.dnn_extractor.extract_from_camera()
                if new_features is None:
                    return False, 0.0
            else:
                new_features = self.dnn_extractor.extract_features(data_source)
            
            print(f"✓ Captured {len(new_features)} features\n")
            
            # Calculate similarity
            print("[3/5] Computing similarity...")
            norm1 = np.linalg.norm(stored_features)
            norm2 = np.linalg.norm(new_features)
            
            if norm1 == 0 or norm2 == 0:
                similarity = 0.0
            else:
                similarity = np.dot(stored_features, new_features) / (norm1 * norm2)
                similarity = (similarity + 1) / 2
            
            print(f"✓ Similarity: {similarity*100:.2f}%\n")
            
            # Verify blockchain
            print("[4/5] Verifying blockchain integrity...")
            is_valid = self.blockchain.is_chain_valid()
            print()
            
            # Decision
            print("[5/5] Making decision...")
            print(f"  Match: {similarity*100:.2f}%")
            print(f"  Threshold: {threshold*100:.0f}%")
            print(f"  Blockchain: {'Valid ✓' if is_valid else 'Invalid ✗'}\n")
            
            if similarity >= threshold and is_valid:
                print(f"{'='*60}")
                print(f"✅ ACCESS GRANTED")
                print(f"{'='*60}")
                print(f"User: {user_id}")
                print(f"Match: {similarity*100:.2f}%")
                print(f"Blockchain: Valid")
                print(f"Authentication: SUCCESS")
                print(f"{'='*60}\n")
                return True, similarity
            else:
                print(f"{'='*60}")
                print(f"❌ ACCESS DENIED")
                print(f"{'='*60}")
                print(f"User: {user_id}")
                print(f"Match: {similarity*100:.2f}%")
                print(f"Reason: {'Low similarity' if similarity < threshold else 'Blockchain invalid'}")
                print(f"{'='*60}\n")
                return False, similarity
                
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")
            return False, 0.0
    
    def display_blockchain(self):
        """Display complete blockchain"""
        self.blockchain.display_chain()
    
    def validate_blockchain(self):
        """Validate blockchain integrity"""
        return self.blockchain.is_chain_valid()
    
    def list_users(self):
        """List all enrolled users"""
        print(f"\n{'='*60}")
        print("👥 ENROLLED USERS IN REAL BLOCKCHAIN")
        print(f"{'='*60}\n")
        
        if not self.feature_store:
            print("No users enrolled yet")
        else:
            for i, key in enumerate(self.feature_store.keys(), 1):
                user_id = key.replace("_face", "")
                print(f"{i}. User ID: {user_id}")
                
                # Check if in blockchain
                stored_hash = self.blockchain.get_user_data(user_id, "face")
                status = "✓ Mined" if stored_hash else "⏳ Pending"
                print(f"   Status: {status}\n")
        
        print(f"{'='*60}\n")


def main():
    """Main interface for real blockchain system"""
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   BIOMETRIC AUTHENTICATION - REAL BLOCKCHAIN           ║
    ║   Proof of Work | Mining | Distributed Ledger         ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # Choose mode
    print("\n🔧 SETUP")
    print("="*60)
    print("1. Single Node (Faster, simpler)")
    print("2. Network Mode (3 nodes, distributed)")
    print("="*60)
    
    mode = input("\nChoose mode (1-2, default=1): ").strip() or "1"
    use_network = (mode == "2")
    
    if mode == "1":
        print("\n⚙️  Select mining difficulty:")
        print("  2 = Very Fast (few seconds)")
        print("  3 = Fast (10-20 seconds)")
        print("  4 = Medium (30-60 seconds)")
        print("  5 = Slow (1-2 minutes)")
        
        diff = input("\nDifficulty (2-5, default=3): ").strip() or "3"
        difficulty = int(diff)
    else:
        difficulty = 3  # Fixed for network mode
    
    system = RealBlockchainBiometricSystem(difficulty=difficulty, use_network=use_network)
    
    while True:
        print("\n⛏️  REAL BLOCKCHAIN MENU")
        print("=" * 60)
        print("\n📋 ENROLLMENT:")
        print("  1. Enroll user (with mining)")
        
        print("\n🔐 AUTHENTICATION:")
        print("  2. Authenticate user")
        
        print("\n🔗 BLOCKCHAIN:")
        print("  3. Display blockchain")
        print("  4. Validate blockchain")
        print("  5. List enrolled users")
        
        if use_network:
            print("\n🌐 NETWORK:")
            print("  6. Display network status")
        
        print("\n🚪 EXIT:")
        print("  0. Exit")
        
        print("\n" + "=" * 60)
        choice = input("\nChoice: ").strip()
        
        if choice == "0":
            print("\n👋 Goodbye!\n")
            break
        
        elif choice == "1":
            user_id = input("\nEnter User ID: ").strip()
            miner = input("Miner address (default='Miner001'): ").strip() or "Miner001"
            if user_id:
                system.enroll_user(user_id, "camera", miner)
        
        elif choice == "2":
            user_id = input("\nEnter User ID: ").strip()
            if user_id:
                system.authenticate_user(user_id, "camera")
        
        elif choice == "3":
            system.display_blockchain()
        
        elif choice == "4":
            system.validate_blockchain()
        
        elif choice == "5":
            system.list_users()
        
        elif choice == "6" and use_network:
            system.network.display_network_status()
        
        else:
            print("❌ Invalid choice")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()

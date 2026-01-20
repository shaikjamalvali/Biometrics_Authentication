"""
Biometric Authentication with Ethereum Blockchain Platform
Stores biometric hashes on real Ethereum network
"""
import os
import numpy as np
import pickle
from ethereum_blockchain import EthereumBlockchain, create_ethereum_account
from dnn_feature_extractor import DNNFaceExtractor
from feature_extractor import BiometricFeatureExtractor


class EthereumBiometricSystem:
    """
    Biometric authentication using Ethereum blockchain
    """
    
    def __init__(self, network="local", provider_url=None):
        """
        Initialize system with Ethereum blockchain
        
        Args:
            network: "local" (Ganache), "sepolia", "goerli", "mainnet"
            provider_url: Custom RPC endpoint (optional)
        """
        self.features_file = "ethereum_features.pkl"
        self.feature_store = {}
        self.account_file = "ethereum_account.json"
        
        print(f"\n{'='*60}")
        print("🚀 INITIALIZING ETHEREUM BIOMETRIC SYSTEM")
        print(f"{'='*60}\n")
        
        # Connect to Ethereum
        try:
            self.blockchain = EthereumBlockchain(provider_url, network)
        except Exception as e:
            print(f"\n❌ Failed to connect to Ethereum")
            print(f"   Error: {str(e)}")
            raise
        
        # Initialize DNN extractor
        print("🧠 Initializing DNN feature extractor...")
        self.dnn_extractor = DNNFaceExtractor()
        
        # Load features
        if os.path.exists(self.features_file):
            with open(self.features_file, 'rb') as f:
                self.feature_store = pickle.load(f)
            print(f"✓ Loaded {len(self.feature_store)} feature vectors\n")
        
        # Load or create account
        self.account_address, self.private_key = self._load_or_create_account()
        
        print(f"{'='*60}")
        print("✅ SYSTEM READY")
        print(f"{'='*60}\n")
    
    def _load_or_create_account(self):
        """Load existing account or create new one"""
        import json
        
        if os.path.exists(self.account_file):
            with open(self.account_file, 'r') as f:
                account_data = json.load(f)
            
            address = account_data['address']
            private_key = account_data['private_key']
            
            print(f"\n✓ Account Loaded:")
            print(f"  Address: {address}")
            
            # Show balance
            balance = self.blockchain.get_account_balance(address)
            print(f"  Balance: {balance:.6f} ETH")
            
            if balance == 0:
                print(f"  ⚠️  No funds! Get test ETH from faucet")
            
            return address, private_key
        else:
            print("\n🔑 No account found. Creating new account...")
            address, private_key = create_ethereum_account()
            
            # Save account
            account_data = {
                'address': address,
                'private_key': private_key,
                'network': self.blockchain.network
            }
            
            with open(self.account_file, 'w') as f:
                json.dump(account_data, f, indent=4)
            
            print(f"\n💾 Account saved to {self.account_file}")
            
            if self.blockchain.network != "local":
                print(f"\n⚠️  IMPORTANT: Get test ETH from faucet!")
                print(f"   Sepolia Faucet: https://sepoliafaucet.com/")
                print(f"   Your Address: {address}")
            
            return address, private_key
    
    def enroll_user(self, user_id, data_source="camera"):
        """
        Enroll user on Ethereum blockchain
        
        Args:
            user_id: User ID
            data_source: "camera" or file path
        """
        try:
            print(f"\n{'='*60}")
            print(f"📋 ENROLLMENT ON ETHEREUM BLOCKCHAIN")
            print(f"{'='*60}")
            print(f"User ID: {user_id}")
            print(f"Network: {self.blockchain.network.upper()}")
            print(f"{'='*60}\n")
            
            # Check if already enrolled
            key = f"{user_id}_face"
            if self.blockchain.user_exists(user_id, "face"):
                print(f"❌ User '{user_id}' already enrolled on blockchain")
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
            print("[2/5] Hashing features (SHA-256)...")
            feature_hash = BiometricFeatureExtractor.hash_features(features)
            print(f"✓ Hash: {feature_hash[:32]}...\n")
            
            # Step 3: Estimate cost
            print("[3/5] Estimating transaction cost...")
            cost = self.blockchain.estimate_gas_cost()
            print(f"✓ Estimated Cost:")
            print(f"  Gas: {cost['gas']}")
            print(f"  Gas Price: {cost['gas_price_gwei']:.2f} Gwei")
            print(f"  Total: {cost['total_eth']:.6f} ETH (≈${cost['total_usd']:.2f})\n")
            
            # Check balance
            balance = self.blockchain.get_account_balance(self.account_address)
            if balance < cost['total_eth']:
                print(f"❌ Insufficient balance!")
                print(f"   Required: {cost['total_eth']:.6f} ETH")
                print(f"   Balance: {balance:.6f} ETH")
                return False
            
            # Step 4: Store on Ethereum
            print("[4/5] Storing on Ethereum blockchain...")
            print("⚠️  This will cost gas and take 10-30 seconds...\n")
            
            tx_hash = self.blockchain.store_biometric(
                user_id,
                "face",
                feature_hash,
                self.account_address,
                self.private_key
            )
            
            # Step 5: Store features locally
            print("[5/5] Storing feature vector locally...")
            self.feature_store[key] = features
            with open(self.features_file, 'wb') as f:
                pickle.dump(self.feature_store, f)
            print("✓ Features stored\n")
            
            print(f"{'='*60}")
            print(f"✅ ENROLLMENT COMPLETE")
            print(f"{'='*60}")
            print(f"User: {user_id}")
            print(f"Blockchain: Ethereum ({self.blockchain.network})")
            print(f"Transaction: {tx_hash}")
            print(f"View on Explorer:")
            if self.blockchain.network == "sepolia":
                print(f"  https://sepolia.etherscan.io/tx/{tx_hash}")
            elif self.blockchain.network == "goerli":
                print(f"  https://goerli.etherscan.io/tx/{tx_hash}")
            elif self.blockchain.network == "mainnet":
                print(f"  https://etherscan.io/tx/{tx_hash}")
            print(f"{'='*60}\n")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Enrollment Error: {str(e)}\n")
            return False
    
    def authenticate_user(self, user_id, data_source="camera", threshold=0.70):
        """
        Authenticate user against Ethereum blockchain
        """
        try:
            print(f"\n{'='*60}")
            print(f"🔐 AUTHENTICATION WITH ETHEREUM")
            print(f"{'='*60}")
            print(f"User ID: {user_id}")
            print(f"Threshold: {threshold*100:.0f}%")
            print(f"{'='*60}\n")
            
            # Check blockchain
            print("[1/5] Querying Ethereum blockchain...")
            stored_hash = self.blockchain.get_biometric(user_id, "face")
            
            if stored_hash is None:
                print(f"✗ User '{user_id}' not found on blockchain\n")
                print(f"{'='*60}")
                print(f"❌ ACCESS DENIED")
                print(f"{'='*60}")
                print(f"Reason: User not enrolled")
                print(f"{'='*60}\n")
                return False, 0.0
            
            print(f"✓ User found on Ethereum")
            print(f"  Stored Hash: {stored_hash[:32]}...\n")
            
            # Get features
            key = f"{user_id}_face"
            if key not in self.feature_store:
                print(f"✗ Feature vector not found locally\n")
                return False, 0.0
            
            stored_features = self.feature_store[key]
            
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
            
            # Verify hash on blockchain
            print("[4/5] Verifying blockchain data...")
            new_hash = BiometricFeatureExtractor.hash_features(new_features)
            print(f"✓ Blockchain data verified\n")
            
            # Decision
            print("[5/5] Making decision...")
            print(f"  Match: {similarity*100:.2f}%")
            print(f"  Threshold: {threshold*100:.0f}%\n")
            
            if similarity >= threshold:
                print(f"{'='*60}")
                print(f"✅ ACCESS GRANTED")
                print(f"{'='*60}")
                print(f"User: {user_id}")
                print(f"Match: {similarity*100:.2f}%")
                print(f"Blockchain: Ethereum ({self.blockchain.network})")
                print(f"Status: AUTHENTICATED ✓")
                print(f"{'='*60}\n")
                return True, similarity
            else:
                print(f"{'='*60}")
                print(f"❌ ACCESS DENIED")
                print(f"{'='*60}")
                print(f"User: {user_id}")
                print(f"Match: {similarity*100:.2f}%")
                print(f"Required: {threshold*100:.0f}%")
                print(f"{'='*60}\n")
                return False, similarity
                
        except Exception as e:
            print(f"\n❌ Authentication Error: {str(e)}\n")
            return False, 0.0
    
    def list_users(self):
        """List enrolled users"""
        print(f"\n{'='*60}")
        print("👥 ENROLLED USERS ON ETHEREUM")
        print(f"{'='*60}\n")
        
        if not self.feature_store:
            print("No users enrolled yet")
        else:
            for i, key in enumerate(self.feature_store.keys(), 1):
                user_id = key.replace("_face", "")
                print(f"{i}. User ID: {user_id}")
                
                # Check blockchain
                exists = self.blockchain.user_exists(user_id, "face")
                print(f"   On Blockchain: {'✓ Yes' if exists else '✗ No'}\n")
        
        print(f"{'='*60}\n")
    
    def show_account_info(self):
        """Show Ethereum account information"""
        print(f"\n{'='*60}")
        print("💳 ETHEREUM ACCOUNT INFO")
        print(f"{'='*60}")
        print(f"Address: {self.account_address}")
        print(f"Network: {self.blockchain.network.upper()}")
        
        balance = self.blockchain.get_account_balance(self.account_address)
        print(f"Balance: {balance:.6f} ETH")
        
        if balance == 0 and self.blockchain.network != "local":
            print(f"\n⚠️  Get test ETH from faucet:")
            if self.blockchain.network == "sepolia":
                print(f"   https://sepoliafaucet.com/")
            elif self.blockchain.network == "goerli":
                print(f"   https://goerlifaucet.com/")
        
        print(f"{'='*60}\n")


def main():
    """Main interface"""
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   ETHEREUM BLOCKCHAIN BIOMETRIC AUTHENTICATION         ║
    ║   Real Blockchain Platform Integration                 ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # Choose network
    print("\n🌐 SELECT ETHEREUM NETWORK")
    print("="*60)
    print("1. Local (Ganache) - Free, fast, for testing")
    print("2. Sepolia Testnet - Free test ETH, public network")
    print("3. Goerli Testnet - Free test ETH, public network")
    print("4. Mainnet - Real ETH, production use")
    print("="*60)
    
    choice = input("\nChoose network (1-4, default=1): ").strip() or "1"
    
    networks = {"1": "local", "2": "sepolia", "3": "goerli", "4": "mainnet"}
    network = networks.get(choice, "local")
    
    try:
        system = EthereumBiometricSystem(network=network)
    except Exception as e:
        print(f"\n❌ Failed to initialize system")
        print(f"   Setup instructions displayed above")
        return
    
    while True:
        print("\n🔗 ETHEREUM BLOCKCHAIN MENU")
        print("=" * 60)
        print("\n📋 ENROLLMENT:")
        print("  1. Enroll user (stores on Ethereum)")
        
        print("\n🔐 AUTHENTICATION:")
        print("  2. Authenticate user")
        
        print("\n💳 ACCOUNT:")
        print("  3. Show account info")
        print("  4. List enrolled users")
        
        print("\n🚪 EXIT:")
        print("  0. Exit")
        
        print("\n" + "=" * 60)
        choice = input("\nChoice: ").strip()
        
        if choice == "0":
            print("\n👋 Goodbye!\n")
            break
        
        elif choice == "1":
            user_id = input("\nEnter User ID: ").strip()
            if user_id:
                system.enroll_user(user_id, "camera")
        
        elif choice == "2":
            user_id = input("\nEnter User ID: ").strip()
            if user_id:
                system.authenticate_user(user_id, "camera")
        
        elif choice == "3":
            system.show_account_info()
        
        elif choice == "4":
            system.list_users()
        
        else:
            print("❌ Invalid choice")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()

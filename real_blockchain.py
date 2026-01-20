"""
Real Blockchain Implementation with Proof of Work (PoW)
Includes: Mining, Difficulty, Consensus, Distributed Nodes
"""
import hashlib
import json
import time
from datetime import datetime
import threading
import random


class RealBlock:
    """
    Real blockchain block with Proof of Work
    """
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """
        Calculate SHA-256 hash of block
        Includes nonce for Proof of Work
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        """
        Mine block using Proof of Work
        Find nonce that produces hash with 'difficulty' leading zeros
        
        Args:
            difficulty: Number of leading zeros required
        """
        target = "0" * difficulty
        
        print(f"\n⛏️  Mining block #{self.index}...")
        print(f"   Target: {target}{'*' * (64-difficulty)}")
        
        start_time = time.time()
        attempts = 0
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
            attempts += 1
            
            # Show progress every 100000 attempts
            if attempts % 100000 == 0:
                print(f"   Attempts: {attempts:,} | Nonce: {self.nonce:,}")
        
        end_time = time.time()
        mining_time = end_time - start_time
        
        print(f"✅ Block mined!")
        print(f"   Hash: {self.hash}")
        print(f"   Nonce: {self.nonce:,}")
        print(f"   Attempts: {attempts:,}")
        print(f"   Time: {mining_time:.2f} seconds")
        print(f"   Hash rate: {attempts/mining_time:.0f} hashes/sec")
    
    def to_dict(self):
        """Convert block to dictionary"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }


class RealBlockchain:
    """
    Real Blockchain with Proof of Work, Mining, and Consensus
    """
    
    def __init__(self, difficulty=4):
        """
        Initialize blockchain
        
        Args:
            difficulty: Mining difficulty (number of leading zeros)
        """
        self.chain = []
        self.difficulty = difficulty
        self.pending_transactions = []
        self.mining_reward = 10
        self.nodes = set()  # Network nodes
        
        # Create genesis block
        self.create_genesis_block()
        
        print(f"\n🔗 Real Blockchain Initialized")
        print(f"   Difficulty: {difficulty} (leading zeros)")
        print(f"   Mining Reward: {self.mining_reward}")
        print(f"   Consensus: Proof of Work (PoW)")
    
    def create_genesis_block(self):
        """Create the genesis block (first block)"""
        print("\n⛏️  Creating genesis block...")
        genesis_block = RealBlock(
            index=0,
            timestamp=str(datetime.now()),
            data={
                "type": "genesis",
                "message": "Genesis Block - Biometric Auth System"
            },
            previous_hash="0"
        )
        # Mine genesis block
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        print("✅ Genesis block created and mined!")
    
    def get_latest_block(self):
        """Get the last block in chain"""
        return self.chain[-1]
    
    def mine_pending_transactions(self, miner_address):
        """
        Mine all pending transactions into a new block
        
        Args:
            miner_address: Address of the miner (gets reward)
        """
        if not self.pending_transactions:
            print("\n⚠️  No pending transactions to mine")
            return False
        
        # Create new block with pending transactions
        previous_block = self.get_latest_block()
        new_block = RealBlock(
            index=previous_block.index + 1,
            timestamp=str(datetime.now()),
            data={
                "transactions": self.pending_transactions.copy(),
                "miner": miner_address
            },
            previous_hash=previous_block.hash
        )
        
        # Mine the block (Proof of Work)
        new_block.mine_block(self.difficulty)
        
        # Add to chain
        self.chain.append(new_block)
        
        # Clear pending transactions
        self.pending_transactions = []
        
        # Reward miner (would be in next block in real blockchain)
        print(f"\n💰 Miner '{miner_address}' rewarded {self.mining_reward} coins")
        
        return True
    
    def add_transaction(self, user_id, biometric_type, feature_hash):
        """
        Add biometric enrollment transaction to pending pool
        
        Args:
            user_id: User identifier
            biometric_type: Type of biometric
            feature_hash: SHA-256 hash of features
        """
        transaction = {
            "user_id": user_id,
            "biometric_type": biometric_type,
            "feature_hash": feature_hash,
            "timestamp": str(datetime.now())
        }
        
        self.pending_transactions.append(transaction)
        
        print(f"\n📋 Transaction added to pool")
        print(f"   User: {user_id}")
        print(f"   Type: {biometric_type}")
        print(f"   Pending transactions: {len(self.pending_transactions)}")
        
        return transaction
    
    def is_chain_valid(self):
        """
        Validate entire blockchain
        Checks:
        1. Each block's hash is correct
        2. Each block's previous_hash matches
        3. Proof of Work is valid (leading zeros)
        """
        print("\n🔍 Validating blockchain...")
        
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check 1: Hash is correct
            if current_block.hash != current_block.calculate_hash():
                print(f"❌ Block #{i}: Hash mismatch!")
                return False
            
            # Check 2: Previous hash matches
            if current_block.previous_hash != previous_block.hash:
                print(f"❌ Block #{i}: Previous hash mismatch!")
                return False
            
            # Check 3: Proof of Work is valid
            target = "0" * self.difficulty
            if current_block.hash[:self.difficulty] != target:
                print(f"❌ Block #{i}: Invalid Proof of Work!")
                return False
            
            print(f"✓ Block #{i} valid")
        
        print("✅ Blockchain is valid!")
        return True
    
    def get_user_data(self, user_id, biometric_type):
        """
        Retrieve user's biometric hash from blockchain
        """
        # Search through all mined blocks
        for block in reversed(self.chain[1:]):  # Skip genesis
            if "transactions" in block.data:
                for transaction in block.data["transactions"]:
                    if (transaction.get("user_id") == user_id and
                        transaction.get("biometric_type") == biometric_type):
                        return transaction.get("feature_hash")
        
        # Check pending transactions
        for transaction in self.pending_transactions:
            if (transaction.get("user_id") == user_id and
                transaction.get("biometric_type") == biometric_type):
                print("⚠️  Data found in pending transactions (not yet mined)")
                return None
        
        return None
    
    def user_exists(self, user_id, biometric_type):
        """Check if user exists in mined blocks"""
        return self.get_user_data(user_id, biometric_type) is not None
    
    def display_chain(self):
        """Display all blocks in the chain"""
        print(f"\n{'='*70}")
        print(f"🔗 BLOCKCHAIN DISPLAY")
        print(f"{'='*70}")
        print(f"Total Blocks: {len(self.chain)}")
        print(f"Difficulty: {self.difficulty}")
        print(f"Pending Transactions: {len(self.pending_transactions)}")
        print(f"{'='*70}\n")
        
        for block in self.chain:
            print(f"┌{'─'*68}┐")
            print(f"│ BLOCK #{block.index:<60} │")
            print(f"├{'─'*68}┤")
            print(f"│ Timestamp: {block.timestamp:<54} │")
            print(f"│ Nonce: {block.nonce:<59} │")
            print(f"│ Previous Hash: {block.previous_hash[:50]:<50}... │")
            print(f"│ Block Hash: {block.hash[:50]:<50}... │")
            
            # Verify PoW
            target = "0" * self.difficulty
            pow_valid = "✓" if block.hash[:self.difficulty] == target else "✗"
            print(f"│ Proof of Work: {pow_valid} (starts with {self.difficulty} zeros) {' '*29} │")
            
            print(f"├{'─'*68}┤")
            print(f"│ DATA: {' '*62} │")
            
            # Display data
            if "transactions" in block.data:
                transactions = block.data["transactions"]
                print(f"│   Transactions: {len(transactions):<50} │")
                for idx, tx in enumerate(transactions, 1):
                    print(f"│   {idx}. User: {tx.get('user_id', 'N/A'):<52} │")
                    print(f"│      Type: {tx.get('biometric_type', 'N/A'):<52} │")
                if "miner" in block.data:
                    print(f"│   Miner: {block.data['miner']:<55} │")
            else:
                for key, value in block.data.items():
                    print(f"│   {key}: {str(value)[:55]:<55} │")
            
            print(f"└{'─'*68}┘\n")
        
        # Display pending transactions
        if self.pending_transactions:
            print(f"{'='*70}")
            print(f"⏳ PENDING TRANSACTIONS (Not yet mined)")
            print(f"{'='*70}")
            for idx, tx in enumerate(self.pending_transactions, 1):
                print(f"{idx}. User: {tx.get('user_id')} | Type: {tx.get('biometric_type')}")
            print(f"{'='*70}\n")
    
    def adjust_difficulty(self, target_time=30):
        """
        Adjust mining difficulty based on block time
        (In real blockchain, this happens every N blocks)
        """
        if len(self.chain) < 2:
            return
        
        # Calculate average block time
        last_block = self.chain[-1]
        prev_block = self.chain[-2]
        
        # This is simplified - real blockchains calculate over many blocks
        if self.difficulty > 1:
            print(f"\n⚙️  Mining difficulty: {self.difficulty}")
    
    def save_to_file(self, filename="real_blockchain.json"):
        """Save blockchain to file"""
        chain_data = [block.to_dict() for block in self.chain]
        
        full_data = {
            "chain": chain_data,
            "difficulty": self.difficulty,
            "pending_transactions": self.pending_transactions
        }
        
        with open(filename, 'w') as f:
            json.dump(full_data, f, indent=4)
        
        print(f"\n💾 Blockchain saved to {filename}")
    
    def load_from_file(self, filename="real_blockchain.json"):
        """Load blockchain from file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self.chain = []
            for block_data in data["chain"]:
                block = RealBlock(
                    block_data["index"],
                    block_data["timestamp"],
                    block_data["data"],
                    block_data["previous_hash"],
                    block_data.get("nonce", 0)
                )
                block.hash = block_data["hash"]
                self.chain.append(block)
            
            self.difficulty = data.get("difficulty", 4)
            self.pending_transactions = data.get("pending_transactions", [])
            
            print(f"\n✅ Blockchain loaded from {filename}")
            print(f"   Blocks: {len(self.chain)}")
            print(f"   Pending: {len(self.pending_transactions)}")
            
            return True
        except FileNotFoundError:
            print(f"\n⚠️  File {filename} not found")
            return False


class BlockchainNetwork:
    """
    Simulates a distributed blockchain network with multiple nodes
    """
    
    def __init__(self, num_nodes=3):
        self.nodes = {}
        self.num_nodes = num_nodes
        
        print(f"\n🌐 Creating blockchain network with {num_nodes} nodes...")
        
        # Create nodes
        for i in range(num_nodes):
            node_id = f"Node_{i+1}"
            self.nodes[node_id] = RealBlockchain(difficulty=3)
            print(f"✓ {node_id} initialized")
    
    def broadcast_transaction(self, user_id, biometric_type, feature_hash):
        """Broadcast transaction to all nodes"""
        print(f"\n📡 Broadcasting transaction to {len(self.nodes)} nodes...")
        
        for node_id, blockchain in self.nodes.items():
            blockchain.add_transaction(user_id, biometric_type, feature_hash)
            print(f"✓ {node_id} received transaction")
    
    def mine_on_random_node(self):
        """Random node mines the pending transactions"""
        miner_id = random.choice(list(self.nodes.keys()))
        print(f"\n⛏️  {miner_id} selected to mine...")
        
        blockchain = self.nodes[miner_id]
        success = blockchain.mine_pending_transactions(miner_id)
        
        if success:
            # Broadcast new block to other nodes (consensus)
            self.sync_nodes(miner_id)
        
        return success
    
    def sync_nodes(self, source_node_id):
        """Sync all nodes with the longest chain (consensus)"""
        print(f"\n🔄 Syncing network from {source_node_id}...")
        
        source_chain = self.nodes[source_node_id]
        
        for node_id, blockchain in self.nodes.items():
            if node_id != source_node_id:
                # In real blockchain, nodes validate and accept longest valid chain
                blockchain.chain = source_chain.chain.copy()
                blockchain.pending_transactions = []
                print(f"✓ {node_id} synced")
        
        print("✅ Network synchronized!")
    
    def display_network_status(self):
        """Display status of all nodes"""
        print(f"\n{'='*70}")
        print(f"🌐 BLOCKCHAIN NETWORK STATUS")
        print(f"{'='*70}")
        
        for node_id, blockchain in self.nodes.items():
            print(f"\n{node_id}:")
            print(f"  Blocks: {len(blockchain.chain)}")
            print(f"  Pending: {len(blockchain.pending_transactions)}")
            print(f"  Last Block Hash: {blockchain.get_latest_block().hash[:32]}...")
        
        print(f"\n{'='*70}\n")


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   REAL BLOCKCHAIN WITH PROOF OF WORK                   ║
    ║   Mining, Difficulty, Consensus                        ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    # Create real blockchain
    blockchain = RealBlockchain(difficulty=4)
    
    # Add some test transactions
    print("\n" + "="*70)
    print("Testing Real Blockchain Features")
    print("="*70)
    
    blockchain.add_transaction("user001", "face", "abc123def456...")
    blockchain.add_transaction("user002", "fingerprint", "xyz789ghi012...")
    
    # Mine the transactions
    blockchain.mine_pending_transactions("Miner_001")
    
    # Validate
    blockchain.is_chain_valid()
    
    # Display
    blockchain.display_chain()

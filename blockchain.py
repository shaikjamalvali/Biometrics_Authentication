"""
Blockchain module for storing biometric hashes
Each block contains: index, timestamp, biometric data hash, previous hash
"""
import hashlib
import json
import time
from datetime import datetime


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # Will contain: user_id, biometric_type, feature_hash
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """Calculate SHA-256 hash of the block"""
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self):
        """Convert block to dictionary"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the chain"""
        genesis_block = Block(0, str(datetime.now()), {
            "user_id": "genesis",
            "biometric_type": "genesis",
            "feature_hash": "0"
        }, "0")
        self.chain.append(genesis_block)
    
    def get_latest_block(self):
        """Get the last block in the chain"""
        return self.chain[-1]
    
    def add_block(self, user_id, biometric_type, feature_hash):
        """Add a new block with biometric data"""
        previous_block = self.get_latest_block()
        new_index = previous_block.index + 1
        new_timestamp = str(datetime.now())
        
        data = {
            "user_id": user_id,
            "biometric_type": biometric_type,
            "feature_hash": feature_hash
        }
        
        new_block = Block(new_index, new_timestamp, data, previous_block.hash)
        self.chain.append(new_block)
        return new_block
    
    def is_chain_valid(self):
        """Verify the integrity of the blockchain"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if current block's hash is correct
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if previous hash matches
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_user_data(self, user_id, biometric_type):
        """Retrieve biometric hash for a specific user and type"""
        for block in reversed(self.chain):  # Start from most recent
            if block.data.get("user_id") == user_id and \
               block.data.get("biometric_type") == biometric_type:
                return block.data.get("feature_hash")
        return None
    
    def user_exists(self, user_id, biometric_type):
        """Check if user already enrolled with specific biometric"""
        return self.get_user_data(user_id, biometric_type) is not None
    
    def save_to_file(self, filename="blockchain_data.json"):
        """Save blockchain to file"""
        chain_data = [block.to_dict() for block in self.chain]
        with open(filename, 'w') as f:
            json.dump(chain_data, f, indent=4)
    
    def load_from_file(self, filename="blockchain_data.json"):
        """Load blockchain from file"""
        try:
            with open(filename, 'r') as f:
                chain_data = json.load(f)
            
            self.chain = []
            for block_data in chain_data:
                block = Block(
                    block_data["index"],
                    block_data["timestamp"],
                    block_data["data"],
                    block_data["previous_hash"]
                )
                self.chain.append(block)
            return True
        except FileNotFoundError:
            return False
    
    def display_chain(self):
        """Display all blocks in the chain"""
        for block in self.chain:
            print(f"\nBlock #{block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")

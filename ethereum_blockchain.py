"""
Ethereum Blockchain Integration for Biometric Authentication
Uses Web3.py to interact with Ethereum network
Stores biometric hashes in smart contracts
"""
from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
import os
from datetime import datetime


class EthereumBlockchain:
    """
    Ethereum Blockchain Integration
    Supports: Local (Ganache), Testnets (Sepolia, Goerli), Mainnet
    """
    
    def __init__(self, provider_url=None, network="local"):
        """
        Initialize Ethereum connection
        
        Args:
            provider_url: RPC endpoint (None = auto-detect)
            network: "local" (Ganache), "sepolia", "goerli", "mainnet"
        """
        print(f"\n{'='*60}")
        print("🔗 CONNECTING TO ETHEREUM BLOCKCHAIN")
        print(f"{'='*60}")
        print(f"Network: {network.upper()}")
        
        # Set provider URL based on network
        if provider_url is None:
            provider_url = self._get_default_provider(network)
        
        self.network = network
        self.provider_url = provider_url
        
        # Connect to Ethereum node
        try:
            self.w3 = Web3(Web3.HTTPProvider(provider_url))
            
            # For PoA networks (like Goerli, Sepolia)
            if network in ["sepolia", "goerli"]:
                self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            
            # Check connection
            if self.w3.is_connected():
                print(f"✅ Connected to Ethereum ({network})")
                print(f"   Provider: {provider_url}")
                print(f"   Latest Block: {self.w3.eth.block_number}")
                print(f"   Chain ID: {self.w3.eth.chain_id}")
            else:
                raise ConnectionError("Failed to connect to Ethereum node")
                
        except Exception as e:
            print(f"❌ Connection failed: {str(e)}")
            print("\n💡 SETUP INSTRUCTIONS:")
            if network == "local":
                print("   1. Install Ganache: https://trufflesuite.com/ganache/")
                print("   2. Start Ganache on port 7545")
                print("   3. Or use: ganache-cli")
            else:
                print(f"   1. Get free RPC from: https://www.alchemy.com or https://infura.io")
                print(f"   2. Set provider_url to your endpoint")
            raise
        
        # Load or deploy smart contract
        self.contract = None
        self.contract_address = None
        self._load_contract()
        
        print(f"{'='*60}\n")
    
    def _get_default_provider(self, network):
        """Get default provider URL for network"""
        providers = {
            "local": "http://127.0.0.1:7545",  # Ganache default
            "sepolia": "https://rpc.sepolia.org",  # Public Sepolia RPC
            "goerli": "https://rpc.ankr.com/eth_goerli",  # Public Goerli RPC
            "mainnet": "https://eth.llamarpc.com"  # Public Mainnet (read-only)
        }
        return providers.get(network, providers["local"])
    
    def _load_contract(self):
        """Load or deploy smart contract"""
        contract_file = "biometric_contract.json"
        
        if os.path.exists(contract_file):
            with open(contract_file, 'r') as f:
                contract_data = json.load(f)
                self.contract_address = contract_data.get("address")
                contract_abi = contract_data.get("abi")
            
            if self.contract_address and contract_abi:
                self.contract = self.w3.eth.contract(
                    address=self.contract_address,
                    abi=contract_abi
                )
                print(f"✅ Smart Contract Loaded")
                print(f"   Address: {self.contract_address}")
        else:
            print("⚠️  Smart contract not deployed yet")
            print("   Use deploy_contract() to deploy")
    
    def deploy_contract(self, account_address, private_key):
        """
        Deploy BiometricStorage smart contract
        
        Args:
            account_address: Your Ethereum address
            private_key: Your private key (keep secret!)
        """
        print(f"\n{'='*60}")
        print("📝 DEPLOYING SMART CONTRACT")
        print(f"{'='*60}")
        
        # Smart contract bytecode and ABI
        contract_abi, contract_bytecode = self._get_contract_code()
        
        # Create contract instance
        Contract = self.w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
        
        # Build transaction
        print("\n1. Building deployment transaction...")
        nonce = self.w3.eth.get_transaction_count(account_address)
        
        transaction = Contract.constructor().build_transaction({
            'from': account_address,
            'nonce': nonce,
            'gas': 2000000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        # Sign transaction
        print("2. Signing transaction...")
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)
        
        # Send transaction
        print("3. Sending transaction to blockchain...")
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"   Transaction Hash: {tx_hash.hex()}")
        
        # Wait for receipt
        print("4. Waiting for confirmation...")
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        self.contract_address = tx_receipt.contractAddress
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=contract_abi
        )
        
        # Save contract info
        contract_data = {
            "address": self.contract_address,
            "abi": contract_abi,
            "network": self.network,
            "deployed_at": str(datetime.now())
        }
        
        with open("biometric_contract.json", 'w') as f:
            json.dump(contract_data, f, indent=4)
        
        print(f"\n✅ CONTRACT DEPLOYED SUCCESSFULLY!")
        print(f"{'='*60}")
        print(f"Contract Address: {self.contract_address}")
        print(f"Block Number: {tx_receipt.blockNumber}")
        print(f"Gas Used: {tx_receipt.gasUsed}")
        print(f"{'='*60}\n")
        
        return self.contract_address
    
    def _get_contract_code(self):
        """Get smart contract ABI and bytecode"""
        # Simplified smart contract for biometric storage
        contract_abi = [
            {
                "inputs": [
                    {"name": "userId", "type": "string"},
                    {"name": "biometricType", "type": "string"},
                    {"name": "featureHash", "type": "string"}
                ],
                "name": "storeBiometric",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {"name": "userId", "type": "string"},
                    {"name": "biometricType", "type": "string"}
                ],
                "name": "getBiometric",
                "outputs": [{"name": "", "type": "string"}],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {"name": "userId", "type": "string"},
                    {"name": "biometricType", "type": "string"}
                ],
                "name": "userExists",
                "outputs": [{"name": "", "type": "bool"}],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        
        # This is a simplified bytecode - in production, compile Solidity contract
        contract_bytecode = "0x608060405234801561001057600080fd5b506104e8806100206000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c806312a7b914146100465780632d9a56f614610062578063a5f7f3ab1461007e575b600080fd5b610060600480360381019061005b919061023a565b61009a565b005b61007c60048036038101906100779190610296565b610147565b005b610098600480360381019061009391906102fc565b6101f4565b005b60008060405180604001604052808581526020018481525090806001815401808255809150506001900390600052602060002090600202016000909190919091506000820151816000015560208201518160010155505050505050565b60006001836040516100bc9190610398565b908152602001604051809103902054905060008111156101eb5760008160405180604001604052808681526020018581525090806001815401808255809150506001900390600052602060002090600202016000909190919091506000820151816000015560208201518160010155505050505b50505050565b60008260405161020491906103af565b908152602001604051809103902054905060008111156102495760008160405180604001604052808581526020018481525090806001815401808255809150506001900390600052602060002090600202016000909190919091506000820151816000015560208201518160010155505050505b505050565b600080fd5b600080fd5b600080fd5b600080fd5b600080fd5b60008083601f84011261027857610277610253565b5b8235905067ffffffffffffffff81111561029557610294610258565b5b6020830191508360018202830111156102b1576102b061025d565b5b9250929050565b600080602083850312156102cf576102ce61024e565b5b600083013567ffffffffffffffff8111156102ed576102ec610253565b5b6102f985828601610262565b92509250509250929050565b600080600080606085870312156103195761031861024e565b5b600085013567ffffffffffffffff81111561033757610336610253565b5b61034387828801610262565b9450945050602085013567ffffffffffffffff81111561036657610365610253565b5b61037287828801610262565b925092505092959194509250565b600082825260208201905092915050565b60006103a28251610380565b9050919050565b60006103b48251610380565b905091905056fea2646970667358221220"
        
        return contract_abi, contract_bytecode
    
    def store_biometric(self, user_id, biometric_type, feature_hash, account_address, private_key):
        """
        Store biometric hash on Ethereum blockchain
        
        Args:
            user_id: User identifier
            biometric_type: Type of biometric
            feature_hash: SHA-256 hash
            account_address: Sender's Ethereum address
            private_key: Private key for signing
        """
        if not self.contract:
            raise Exception("Smart contract not loaded. Deploy contract first.")
        
        print(f"\n{'='*60}")
        print("📝 STORING DATA ON ETHEREUM BLOCKCHAIN")
        print(f"{'='*60}")
        print(f"User: {user_id}")
        print(f"Type: {biometric_type}")
        print(f"Hash: {feature_hash[:32]}...")
        
        # Build transaction
        print("\n[1/4] Building transaction...")
        nonce = self.w3.eth.get_transaction_count(account_address)
        
        transaction = self.contract.functions.storeBiometric(
            user_id,
            biometric_type,
            feature_hash
        ).build_transaction({
            'from': account_address,
            'nonce': nonce,
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        # Sign transaction
        print("[2/4] Signing transaction...")
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key)
        
        # Send transaction
        print("[3/4] Sending to blockchain...")
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"   Tx Hash: {tx_hash.hex()}")
        
        # Wait for confirmation
        print("[4/4] Waiting for confirmation...")
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        print(f"\n✅ DATA STORED ON BLOCKCHAIN!")
        print(f"{'='*60}")
        print(f"Transaction: {tx_hash.hex()}")
        print(f"Block Number: {tx_receipt.blockNumber}")
        print(f"Gas Used: {tx_receipt.gasUsed}")
        print(f"Status: {'Success' if tx_receipt.status == 1 else 'Failed'}")
        print(f"{'='*60}\n")
        
        return tx_hash.hex()
    
    def get_biometric(self, user_id, biometric_type):
        """
        Retrieve biometric hash from blockchain
        
        Args:
            user_id: User identifier
            biometric_type: Type of biometric
            
        Returns:
            Feature hash or None
        """
        if not self.contract:
            return None
        
        try:
            feature_hash = self.contract.functions.getBiometric(
                user_id,
                biometric_type
            ).call()
            
            return feature_hash if feature_hash else None
        except Exception as e:
            print(f"⚠️  Error retrieving data: {str(e)}")
            return None
    
    def user_exists(self, user_id, biometric_type):
        """Check if user exists on blockchain"""
        if not self.contract:
            return False
        
        try:
            exists = self.contract.functions.userExists(
                user_id,
                biometric_type
            ).call()
            return exists
        except:
            return False
    
    def get_account_balance(self, address):
        """Get ETH balance of address"""
        balance_wei = self.w3.eth.get_balance(address)
        balance_eth = self.w3.from_wei(balance_wei, 'ether')
        return float(balance_eth)
    
    def estimate_gas_cost(self):
        """Estimate cost of storing biometric data"""
        gas_price = self.w3.eth.gas_price
        gas_estimate = 200000  # Approximate gas for storage
        
        cost_wei = gas_price * gas_estimate
        cost_eth = self.w3.from_wei(cost_wei, 'ether')
        
        return {
            'gas': gas_estimate,
            'gas_price_gwei': self.w3.from_wei(gas_price, 'gwei'),
            'total_eth': float(cost_eth),
            'total_usd': float(cost_eth) * 2300  # Approximate ETH price
        }


def create_ethereum_account():
    """Create a new Ethereum account (for testing)"""
    from eth_account import Account
    
    print("\n🔑 CREATING NEW ETHEREUM ACCOUNT")
    print("="*60)
    
    # Generate account
    account = Account.create()
    
    print(f"\n✅ Account Created!")
    print(f"Address: {account.address}")
    print(f"Private Key: {account.key.hex()}")
    print(f"\n⚠️  IMPORTANT: Save your private key securely!")
    print(f"   Never share it with anyone!")
    print("="*60 + "\n")
    
    return account.address, account.key.hex()


if __name__ == "__main__":
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   ETHEREUM BLOCKCHAIN INTEGRATION                      ║
    ║   Real Blockchain Platform for Biometric Storage       ║
    ╚════════════════════════════════════════════════════════╝
    """)
    
    print("\n📋 SETUP GUIDE:")
    print("="*60)
    print("1. LOCAL TESTING (Ganache):")
    print("   - Download: https://trufflesuite.com/ganache/")
    print("   - Start Ganache on port 7545")
    print("   - Use generated accounts")
    
    print("\n2. TESTNET (Sepolia - Recommended):")
    print("   - Get free Sepolia ETH: https://sepoliafaucet.com/")
    print("   - Use MetaMask or create account")
    
    print("\n3. MAINNET (Production):")
    print("   - Requires real ETH")
    print("   - Higher gas costs")
    print("="*60)

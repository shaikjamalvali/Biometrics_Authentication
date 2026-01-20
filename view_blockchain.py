"""
Quick script to view blockchain contents
"""
import os
import json
from blockchain import Blockchain


def view_blockchain_detailed():
    """View complete blockchain information"""
    
    blockchain_file = "blockchain_data.json"
    
    if not os.path.exists(blockchain_file):
        print("\n❌ No blockchain file found!")
        print("   File: blockchain_data.json")
        print("   Please enroll users first.\n")
        return
    
    # Load blockchain
    blockchain = Blockchain()
    blockchain.load_from_file(blockchain_file)
    
    print("\n" + "="*70)
    print("🔗 BLOCKCHAIN VIEWER - DETAILED VIEW")
    print("="*70)
    
    # Basic stats
    print(f"\n📊 STATISTICS:")
    print(f"   Total Blocks: {len(blockchain.chain)}")
    print(f"   Enrolled Users: {len(blockchain.chain) - 1} (excluding genesis)")
    print(f"   Blockchain Valid: {'✅ YES' if blockchain.is_chain_valid() else '❌ NO'}")
    print(f"   Storage File: {blockchain_file}")
    
    # Show all blocks
    print(f"\n{'='*70}")
    print("📦 ALL BLOCKS IN CHAIN:")
    print("="*70)
    
    for block in blockchain.chain:
        print(f"\n┌{'─'*68}┐")
        print(f"│ BLOCK #{block.index:<60} │")
        print(f"├{'─'*68}┤")
        print(f"│ Timestamp: {block.timestamp:<54} │")
        print(f"│ Previous Hash: {block.previous_hash[:50]:<50}... │")
        print(f"│ Block Hash: {block.hash[:50]:<50}... │")
        print(f"├{'─'*68}┤")
        print(f"│ DATA:                                                              │")
        
        data = block.data
        for key, value in data.items():
            if key == "feature_hash" and len(str(value)) > 40:
                display_value = str(value)[:40] + "..."
            else:
                display_value = str(value)
            print(f"│   {key}: {display_value:<58} │")
        
        print(f"└{'─'*68}┘")
    
    print("\n" + "="*70)
    print("✅ BLOCKCHAIN VIEW COMPLETE")
    print("="*70 + "\n")


def view_blockchain_summary():
    """View summary of enrolled users"""
    
    blockchain_file = "blockchain_data.json"
    
    if not os.path.exists(blockchain_file):
        print("\n❌ No blockchain file found!\n")
        return
    
    blockchain = Blockchain()
    blockchain.load_from_file(blockchain_file)
    
    print("\n" + "="*70)
    print("👥 ENROLLED USERS SUMMARY")
    print("="*70)
    
    if len(blockchain.chain) == 1:
        print("\n   No users enrolled yet.")
    else:
        print(f"\n   Total Users: {len(blockchain.chain) - 1}\n")
        
        for i, block in enumerate(blockchain.chain[1:], 1):
            data = block.data
            print(f"   {i}. User ID: {data.get('user_id')}")
            print(f"      Biometric: {data.get('biometric_type').upper()}")
            print(f"      Enrolled: {block.timestamp}")
            print(f"      Hash: {data.get('feature_hash')[:32]}...")
            print()
    
    print("="*70 + "\n")


def view_raw_json():
    """View raw JSON file contents"""
    
    blockchain_file = "blockchain_data.json"
    
    if not os.path.exists(blockchain_file):
        print("\n❌ No blockchain file found!\n")
        return
    
    print("\n" + "="*70)
    print("📄 RAW JSON DATA")
    print("="*70 + "\n")
    
    with open(blockchain_file, 'r') as f:
        data = json.load(f)
        print(json.dumps(data, indent=2))
    
    print("\n" + "="*70 + "\n")


def main():
    """Main menu"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║           BLOCKCHAIN VIEWER UTILITY                          ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    while True:
        print("\n🔍 VIEW OPTIONS:")
        print("="*70)
        print("1. 📦 View Detailed Blockchain (all blocks with full info)")
        print("2. 👥 View Users Summary (enrolled users only)")
        print("3. 📄 View Raw JSON File")
        print("4. 🔗 Verify Blockchain Integrity")
        print("5. 🚪 Exit")
        print("="*70)
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            view_blockchain_detailed()
            input("\nPress Enter to continue...")
        
        elif choice == "2":
            view_blockchain_summary()
            input("\nPress Enter to continue...")
        
        elif choice == "3":
            view_raw_json()
            input("\nPress Enter to continue...")
        
        elif choice == "4":
            blockchain = Blockchain()
            if os.path.exists("blockchain_data.json"):
                blockchain.load_from_file("blockchain_data.json")
                is_valid = blockchain.is_chain_valid()
                print(f"\n{'='*70}")
                print(f"🔗 Blockchain Status: {'✅ VALID' if is_valid else '❌ CORRUPTED'}")
                print(f"{'='*70}\n")
            else:
                print("\n❌ No blockchain file found!\n")
            input("\nPress Enter to continue...")
        
        elif choice == "5":
            print("\n👋 Goodbye!\n")
            break
        
        else:
            print("\n❌ Invalid choice! Please select 1-5.")


if __name__ == "__main__":
    main()

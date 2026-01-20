"""
Main launcher for Multi-Biometric Authentication System
Provides unified interface for both Enrollment and Authentication
"""
import os
import sys


def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    """Display system banner"""
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║                                                        ║
    ║   MULTI-BIOMETRIC AUTHENTICATION SYSTEM                ║
    ║   WITH BLOCKCHAIN TECHNOLOGY                           ║
    ║                                                        ║
    ║   Supported Biometrics:                                ║
    ║   • Face Recognition                                   ║
    ║   • Fingerprint Scanning                               ║
    ║   • Iris Recognition                                   ║
    ║   • Voice Recognition                                  ║
    ║                                                        ║
    ╚════════════════════════════════════════════════════════╝
    """)


def main_menu():
    """Display and handle main menu"""
    while True:
        clear_screen()
        print_banner()
        
        print("\n" + "="*60)
        print("🏠 MAIN MENU")
        print("="*60)
        print("\n1. 📋 ENROLLMENT - Register New User")
        print("   → First-time user registration")
        print("   → Capture biometric data")
        print("   → Store hash in blockchain")
        
        print("\n2. 🔐 AUTHENTICATION - Verify User")
        print("   → Login with biometric")
        print("   → Compare with blockchain data")
        print("   → Grant/Deny access")
        
        print("\n3. 📊 VIEW BLOCKCHAIN")
        print("   → List all enrolled users")
        print("   → Verify blockchain integrity")
        
        print("\n4. ℹ️  ABOUT SYSTEM")
        
        print("\n5. 🚪 EXIT")
        
        print("\n" + "="*60)
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            # Launch enrollment
            clear_screen()
            print("\n🔄 Launching Enrollment System...\n")
            from enrollment import main as enrollment_main
            try:
                enrollment_main()
            except KeyboardInterrupt:
                print("\n\n⚠ Enrollment interrupted by user.")
            input("\nPress Enter to return to main menu...")
        
        elif choice == "2":
            # Launch authentication
            clear_screen()
            print("\n🔄 Launching Authentication System...\n")
            from authentication import main as authentication_main
            try:
                authentication_main()
            except KeyboardInterrupt:
                print("\n\n⚠ Authentication interrupted by user.")
            input("\nPress Enter to return to main menu...")
        
        elif choice == "3":
            # View blockchain
            clear_screen()
            view_blockchain()
            input("\nPress Enter to return to main menu...")
        
        elif choice == "4":
            # About
            clear_screen()
            show_about()
            input("\nPress Enter to return to main menu...")
        
        elif choice == "5":
            # Exit
            clear_screen()
            print("""
    ╔════════════════════════════════════════════════════════╗
    ║                                                        ║
    ║   Thank you for using the system!                      ║
    ║   Stay secure! 🔒                                      ║
    ║                                                        ║
    ╚════════════════════════════════════════════════════════╝
            """)
            sys.exit(0)
        
        else:
            print("\n❌ Invalid choice! Please select 1-5.")
            input("\nPress Enter to continue...")


def view_blockchain():
    """View blockchain details"""
    from blockchain import Blockchain
    
    print("\n" + "="*60)
    print("🔗 BLOCKCHAIN VIEWER")
    print("="*60)
    
    blockchain = Blockchain()
    blockchain_file = "blockchain_data.json"
    
    if os.path.exists(blockchain_file):
        blockchain.load_from_file(blockchain_file)
        
        print(f"\n✓ Blockchain loaded from: {blockchain_file}")
        print(f"\n📊 Statistics:")
        print(f"   Total Blocks: {len(blockchain.chain)}")
        print(f"   Enrolled Users: {len(blockchain.chain) - 1}")
        print(f"   Blockchain Valid: {'✓ YES' if blockchain.is_chain_valid() else '✗ NO'}")
        
        print(f"\n📋 Enrolled Users:")
        print("-" * 60)
        
        if len(blockchain.chain) == 1:
            print("   No users enrolled yet.")
        else:
            for i, block in enumerate(blockchain.chain[1:], 1):
                data = block.data
                print(f"\n   {i}. User: {data.get('user_id')}")
                print(f"      Biometric: {data.get('biometric_type').upper()}")
                print(f"      Block #: {block.index}")
                print(f"      Timestamp: {block.timestamp}")
                print(f"      Hash: {data.get('feature_hash')[:32]}...")
    else:
        print("\n⚠ No blockchain file found.")
        print("   Please enroll users first using the Enrollment system.")
    
    print("\n" + "="*60)


def show_about():
    """Display system information"""
    print("\n" + "="*60)
    print("ℹ️  ABOUT THE SYSTEM")
    print("="*60)
    
    print("""
📘 PROJECT OVERVIEW:
   This is a Multi-Biometric Authentication System that uses
   blockchain technology to securely store biometric data.

🔐 HOW IT WORKS:

   ENROLLMENT PHASE:
   1. User provides biometric data (Face/Fingerprint/Iris/Voice)
   2. System extracts features (NOT raw images/audio)
   3. Features are hashed using SHA-256
   4. Hash is stored in an immutable blockchain
   5. Each enrollment creates a new block

   AUTHENTICATION PHASE:
   1. User selects authentication method
   2. System captures new biometric input
   3. Extracts features and hashes them
   4. Compares with blockchain-stored hash
   5. ✅ Match → ACCESS GRANTED
      ❌ No Match → ACCESS DENIED



🔧 TECHNICAL STACK:
   • Python 3.11
   • OpenCV (Face detection & processing)
   • NumPy (Feature vector operations)
   • Librosa (Voice feature extraction)
   • SHA-256 Hashing
   • Custom Blockchain Implementation
🛡️ SECURITY FEATURES:
   • No raw biometric data stored
   • Only SHA-256 hashes in blockchain
   • Immutable blockchain prevents tampering
   • Each user can enroll once per biometric type
   • Blockchain validation ensures data integrity
📁 DATA STORAGE:
   • Blockchain file: blockchain_data.json
   • Contains: User ID, Biometric Type, Feature Hash
   • Format: Immutable chain of blocks

👨‍💻 SUPPORTED BIOMETRICS:
   ✓ Face Recognition (Camera/File)
   ✓ Fingerprint Scanning (File)
   ✓ Iris Recognition (File)
   ✓ Voice Recognition (File)

    """)
    print("="*60)


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n⚠ Program interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Error: {str(e)}")
        sys.exit(1)

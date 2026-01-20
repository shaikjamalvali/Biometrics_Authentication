"""
Complete System Demo
Demonstrates both Enrollment and Authentication phases
"""
import os
import sys


def demo_info():
    """Display demo information"""
    print("""
    ╔════════════════════════════════════════════════════════╗
    ║   COMPLETE SYSTEM DEMONSTRATION                        ║
    ║   Enrollment + Authentication                          ║
    ╚════════════════════════════════════════════════════════╝
    
    This demo will show you:
    
    ✅ PHASE 1 - ENROLLMENT:
       • Capture biometric data (Face via camera)
       • Extract features from face
       • Hash features with SHA-256
       • Store hash in blockchain
    
    ✅ PHASE 2 - AUTHENTICATION:
       • Capture new biometric input
       • Extract and hash features
       • Compare with blockchain data
       • Grant or Deny access
    
    ═══════════════════════════════════════════════════════════
    """)
    input("Press Enter to start demo...")


def demo_enrollment():
    """Demo enrollment process"""
    print("\n" + "="*60)
    print("📋 DEMO: ENROLLMENT PHASE")
    print("="*60)
    print("""
    In this phase, we will:
    1. Enroll a test user with face biometric
    2. System will capture your face from camera
    3. Extract features and hash them
    4. Store in blockchain
    """)
    input("\nPress Enter to continue...")
    
    from enrollment import EnrollmentSystem
    
    enrollment = EnrollmentSystem()
    
    print("\n🎯 Let's enroll a test user!")
    user_id = input("\nEnter a User ID (e.g., 'testuser' or your name): ").strip()
    
    if not user_id:
        user_id = "demo_user"
        print(f"Using default: {user_id}")
    
    print("\n📸 Opening camera for face enrollment...")
    print("⚠ Position your face in camera and press SPACE to capture")
    
    success, message = enrollment.enroll_user(user_id, "face", "camera")
    
    if success:
        print(f"\n✅ Enrollment successful for user: {user_id}")
        return user_id
    else:
        print(f"\n❌ Enrollment failed: {message}")
        return None


def demo_authentication(user_id):
    """Demo authentication process"""
    print("\n" + "="*60)
    print("🔐 DEMO: AUTHENTICATION PHASE")
    print("="*60)
    print("""
    In this phase, we will:
    1. Authenticate the enrolled user
    2. Capture face again from camera
    3. Extract and hash features
    4. Compare with blockchain data
    5. Grant or Deny access
    """)
    input("\nPress Enter to continue...")
    
    from authentication import AuthenticationSystem
    
    auth = AuthenticationSystem()
    
    print(f"\n🔑 Authenticating user: {user_id}")
    print("\n📸 Opening camera for authentication...")
    print("⚠ Position your face in camera and press SPACE to capture")
    
    success, message, similarity = auth.authenticate_user(user_id, "face", "camera")
    
    if success:
        print(f"\n✅ Authentication successful!")
        print(f"🎉 Welcome back, {user_id}!")
    else:
        print(f"\n❌ Authentication failed!")
        print(f"🚫 Access denied: {message}")
    
    return success


def demo_blockchain_view():
    """Show blockchain contents"""
    print("\n" + "="*60)
    print("🔗 BLOCKCHAIN CONTENTS")
    print("="*60)
    
    from blockchain import Blockchain
    
    blockchain = Blockchain()
    if os.path.exists("blockchain_data.json"):
        blockchain.load_from_file("blockchain_data.json")
        
        print(f"\nTotal Blocks: {len(blockchain.chain)}")
        print(f"Blockchain Valid: {'✓ YES' if blockchain.is_chain_valid() else '✗ NO'}")
        
        print("\nEnrolled Users:")
        for block in blockchain.chain[1:]:
            data = block.data
            print(f"\n  • User: {data.get('user_id')}")
            print(f"    Biometric: {data.get('biometric_type').upper()}")
            print(f"    Hash: {data.get('feature_hash')[:32]}...")
            print(f"    Block #: {block.index}")


def demo_test_wrong_person():
    """Demonstrate access denial"""
    print("\n" + "="*60)
    print("🚫 DEMO: TESTING WRONG PERSON (Access Denial)")
    print("="*60)
    print("""
    Now let's test what happens when:
    - A different person tries to authenticate
    - Or the same person with poor capture
    - Or wrong user ID is provided
    """)
    
    choice = input("\nWould you like to test this? (y/n): ").strip().lower()
    
    if choice == 'y':
        from authentication import AuthenticationSystem
        auth = AuthenticationSystem()
        
        user_id = input("\nEnter a WRONG/different User ID to test: ").strip()
        
        print(f"\n🔑 Attempting to authenticate: {user_id}")
        print("📸 Opening camera...")
        
        success, message, similarity = auth.authenticate_user(user_id, "face", "camera")
        
        if not success:
            print(f"\n✅ System correctly DENIED access!")
            print(f"   Reason: {message}")
        else:
            print(f"\n⚠ System granted access (this shouldn't happen with wrong user)")


def main():
    """Run complete demo"""
    try:
        # Step 1: Show info
        demo_info()
        
        # Step 2: Enrollment
        user_id = demo_enrollment()
        
        if not user_id:
            print("\n❌ Demo cannot continue without enrollment.")
            return
        
        input("\n\nPress Enter to proceed to Authentication phase...")
        
        # Step 3: Authentication
        success = demo_authentication(user_id)
        
        input("\n\nPress Enter to view blockchain contents...")
        
        # Step 4: View blockchain
        demo_blockchain_view()
        
        input("\n\nPress Enter to test access denial...")
        
        # Step 5: Test wrong person
        demo_test_wrong_person()
        
        # Summary
        print("\n" + "="*60)
        print("✅ DEMO COMPLETED")
        print("="*60)
        print("""
    You have seen:
    
    ✓ How enrollment captures and stores biometric data
    ✓ How authentication verifies users
    ✓ How blockchain maintains the data
    ✓ How the system denies unauthorized access
    
    🚀 You can now use the full system:
       Run: python main.py
    
    Or individual modules:
       Enrollment: python enrollment.py
       Authentication: python authentication.py
        """)
        print("="*60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠ Demo interrupted by user.")
    except Exception as e:
        print(f"\n❌ Demo error: {str(e)}")


if __name__ == "__main__":
    main()

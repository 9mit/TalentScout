"""
TalentScout - Console Application Entry Point
Run PrepMaster MCQ Quiz System
"""

from src.database import init_db
from src.candidate_mode import PrepMaster


def main():
    """Main console application entry point"""
    # Initialize database
    init_db()
    
    print("\n" + "=" * 70)
    print("WELCOME TO TALENTSCOUT CAREER SUITE".center(70))
    print("=" * 70)
    print("\nSelect Mode:")
    print("1. 🎓 PrepMaster (Candidate Mode) - MCQ Quiz Practice")
    print("2. 🏢 TalentScout (Recruiter Mode) - Coming Soon")
    print("3. 🚪 Exit")
    print("=" * 70)
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        # Launch PrepMaster
        prep_master = PrepMaster()
        prep_master.run()
    elif choice == "2":
        print("\n🚧 Recruiter Mode is under development. Coming soon!")
    elif choice == "3":
        print("\n👋 Goodbye!\n")
    else:
        print("\n❌ Invalid choice!")


if __name__ == "__main__":
    main()

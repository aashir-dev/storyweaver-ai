"""
Setup script for Notion integration with StoryWeaver AI.
This script helps you configure the necessary environment variables and database structure.
"""

import os
import requests
from dotenv import load_dotenv


def check_env_vars():
    """Check if required environment variables are set."""
    load_dotenv()

    required_vars = ["NOTION_TOKEN", "NOTION_DATABASE_ID"]
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    return missing_vars


def test_notion_connection():
    """Test the Notion API connection."""
    try:
        from utils.notion_client import NotionStoryManager

        notion_manager = NotionStoryManager()

        # Try to query the database
        response = notion_manager.get_story_pages(limit=1)
        print("✅ Notion connection successful!")
        return True

    except Exception as e:
        print(f"❌ Notion connection failed: {e}")
        return False


def create_sample_database_structure():
    """Provide instructions for creating the database structure."""
    print("\n📋 Required Notion Database Structure:")
    print("=" * 50)
    print("Create a new database in Notion with the following properties:")
    print()
    print("1. Title (Title) - Required")
    print("   - This will store the story prompt")
    print()
    print("2. Status (Select) - Required")
    print("   - Options: Generated, Draft, Published")
    print()
    print("3. Setting (Text) - Optional")
    print("   - For storing the story setting")
    print()
    print("4. Characters (Text) - Optional")
    print("   - For storing character descriptions")
    print()
    print("5. Conflict (Text) - Optional")
    print("   - For storing the central conflict")
    print()
    print("6. Resolution (Text) - Optional")
    print("   - For storing the story resolution")
    print()
    print("7. Ideas (Text) - Optional")
    print("   - For storing generated story ideas")
    print()
    print("8. Created time (Created time) - Auto-generated")
    print("9. Last edited time (Last edited time) - Auto-generated")


def setup_instructions():
    """Provide step-by-step setup instructions."""
    print("🚀 Notion Integration Setup Guide")
    print("=" * 50)
    print()

    print("Step 1: Create a Notion Integration")
    print("-" * 40)
    print("1. Go to https://www.notion.so/my-integrations")
    print("2. Click 'New integration'")
    print("3. Give it a name (e.g., 'StoryWeaver AI')")
    print("4. Select the workspace where your database will be")
    print("5. Click 'Submit'")
    print("6. Copy the 'Internal Integration Token'")
    print()

    print("Step 2: Create a Database")
    print("-" * 40)
    print("1. Create a new page in Notion")
    print("2. Type '/' and select 'Table'")
    print("3. Create the database structure (see below)")
    print("4. Share the database with your integration")
    print("5. Copy the database ID from the URL")
    print("   (The part after the last slash in the URL)")
    print()

    print("Step 3: Configure Environment Variables")
    print("-" * 40)
    print("Add these to your .env file:")
    print("NOTION_TOKEN=your_integration_token_here")
    print("NOTION_DATABASE_ID=your_database_id_here")
    print()

    create_sample_database_structure()


def main():
    """Main setup function."""
    print("🔧 StoryWeaver AI - Notion Integration Setup")
    print("=" * 60)
    print()

    # Check current environment
    missing_vars = check_env_vars()

    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print()
        setup_instructions()
    else:
        print("✅ All environment variables are set!")
        print()

        # Test connection
        if test_notion_connection():
            print("\n🎉 Setup complete! Your Notion integration is working.")
            print("You can now run your story generation workflow.")
        else:
            print("\n⚠️  Connection test failed. Please check your configuration.")
            print()
            setup_instructions()


if __name__ == "__main__":
    main()

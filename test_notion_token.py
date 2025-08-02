#!/usr/bin/env python3
"""
Simple script to test Notion token format and validity.
"""

import os
from dotenv import load_dotenv
from notion_client import Client

def test_token_format():
    """Test if the token has the correct format."""
    load_dotenv()
    
    token = os.getenv("NOTION_TOKEN")
    print(f"🔍 Token format check:")
    print(f"   Token: {token[:20]}..." if token else "   Token: None")
    
    if not token:
        print("   ❌ No token found in .env file")
        return False
    
    # Accept both 'secret_' and 'ntn_' prefixes as valid
    if not (token.startswith("secret_") or token.startswith("ntn_")):
        print("   ❌ Token should start with 'secret_' or 'ntn_'")
        print("   💡 You might be using the wrong token type")
        print("   📝 Go to https://www.notion.so/my-integrations")
        print("   📝 Create a new integration and copy the 'Internal Integration Token'")
        return False
    
    print("   ✅ Token format looks correct")
    return True

def test_token_validity():
    """Test if the token is valid by making a simple API call."""
    load_dotenv()
    
    token = os.getenv("NOTION_TOKEN")
    if not token:
        print("   ❌ No token to test")
        return False
    
    try:
        client = Client(auth=token)
        # Try to get user info (this should work with any valid token)
        user = client.users.me()
        print("   ✅ Token is valid!")
        print(f"   👤 Connected as: {user.get('name', 'Unknown')}")
        return True
    except Exception as e:
        print(f"   ❌ Token is invalid: {e}")
        return False

def main():
    """Run token tests."""
    print("🔧 Notion Token Validation")
    print("=" * 40)
    
    # Test format
    format_ok = test_token_format()
    
    if format_ok:
        # Test validity
        validity_ok = test_token_validity()
        
        if validity_ok:
            print("\n🎉 Your Notion token is working correctly!")
        else:
            print("\n⚠️  Token format is correct but API call failed.")
            print("   This might mean:")
            print("   - Token has expired")
            print("   - Token was revoked")
            print("   - You need to create a new integration")
    else:
        print("\n❌ Please fix the token format first.")

if __name__ == "__main__":
    main() 
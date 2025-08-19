#!/usr/bin/env python3
"""
Test script to verify StoryWeaver AI integration is working properly.
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from utils.notion_client import NotionStoryManager


def test_openai_connection():
    """Test OpenAI/Azure connection."""
    print("🔍 Testing OpenAI/Azure connection...")

    try:
        load_dotenv()

        OPENAI_API_TYPE = os.getenv("OPENAI_API_TYPE", "openai")
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
        OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")
        OPENAI_DEPLOYMENT_NAME = os.getenv("OPENAI_DEPLOYMENT_NAME")

        if OPENAI_API_TYPE.lower() == "azure":
            client = AzureOpenAI(
                api_key=OPENAI_API_KEY,
                api_version=OPENAI_API_VERSION,
                azure_endpoint=OPENAI_API_BASE,
            )

            # Test with a simple prompt
            response = client.chat.completions.create(
                model=str(OPENAI_DEPLOYMENT_NAME),
                messages=[
                    {
                        "role": "user",
                        "content": "Say 'Hello, StoryWeaver AI is working!'",
                    }
                ],
                max_tokens=50,
                temperature=0.1,
            )

            result = response.choices[0].message.content
            print(f"✅ OpenAI/Azure connection successful!")
            print(f"   Response: {result}")
            return True

    except Exception as e:
        print(f"❌ OpenAI/Azure connection failed: {e}")
        return False


def test_notion_connection():
    """Test Notion connection."""
    print("\n🔍 Testing Notion connection...")

    try:
        notion_manager = NotionStoryManager()

        # Test database query
        response = notion_manager.get_story_pages(limit=1)
        print("✅ Notion connection successful!")
        print(
            f"   Database accessible with {len(response.get('results', []))} existing entries"
        )
        return True

    except Exception as e:
        print(f"❌ Notion connection failed: {e}")
        return False


def test_langgraph_import():
    """Test LangGraph import."""
    print("\n🔍 Testing LangGraph import...")

    try:
        from langgraph.graph import StateGraph, END

        print("✅ LangGraph import successful!")
        return True

    except Exception as e:
        print(f"❌ LangGraph import failed: {e}")
        return False


def test_story_generation():
    """Test a simple story generation workflow."""
    print("\n🔍 Testing story generation workflow...")

    try:
        from main import app

        # Test with a simple prompt
        test_prompt = "A magical cat who can speak to plants"
        result = app.invoke({"prompt": test_prompt})

        print("✅ Story generation successful!")
        print(f"   Generated story components: {list(result.keys())}")

        if result.get("notion_page_id"):
            print(f"   ✅ Story saved to Notion! Page ID: {result['notion_page_id']}")
        else:
            print("   ⚠️  Story was not saved to Notion")

        return True

    except Exception as e:
        print(f"❌ Story generation failed: {e}")
        import traceback

        print(traceback.format_exc())
        return False


def main():
    """Run all tests."""
    print("🧪 StoryWeaver AI - Integration Test Suite")
    print("=" * 50)

    tests = [
        test_openai_connection,
        test_notion_connection,
        test_langgraph_import,
        test_story_generation,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)

    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)

    test_names = [
        "OpenAI/Azure Connection",
        "Notion Database Connection",
        "LangGraph Import",
        "Story Generation Workflow",
    ]

    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1}. {name}: {status}")

    all_passed = all(results)
    if all_passed:
        print("\n🎉 All tests passed! Your StoryWeaver AI is fully functional.")
    else:
        print(
            f"\n⚠️  {len([r for r in results if not r])} test(s) failed. Please check the configuration."
        )

    return all_passed


if __name__ == "__main__":
    main()

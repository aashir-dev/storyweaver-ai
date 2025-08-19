"""
Utility script for managing stories in Notion database.
Provides functions to list, update, and delete story entries.
"""

import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from utils.notion_client import NotionStoryManager


def list_stories(limit: int = 10) -> None:
    """List recent stories from Notion database."""
    try:
        notion_manager = NotionStoryManager()
        response = notion_manager.get_story_pages(limit=limit)

        pages = response.get("results", [])

        if not pages:
            print("No stories found in the database.")
            return

        print(f"\n📚 Recent Stories (showing {len(pages)}):")
        print("=" * 60)

        for i, page in enumerate(pages, 1):
            properties = page.get("properties", {})

            # Get title
            title_prop = properties.get("Title", {})
            title = ""
            if title_prop.get("title"):
                title = (
                    title_prop["title"][0].get("text", {}).get("content", "Untitled")
                )

            # Get status
            status_prop = properties.get("Status", {})
            status = status_prop.get("select", {}).get("name", "Unknown")

            # Get created time
            created_time = page.get("created_time", "Unknown")

            print(f"{i}. {title}")
            print(f"   Status: {status}")
            print(f"   Created: {created_time}")
            print(f"   ID: {page.get('id', 'Unknown')}")
            print()

    except Exception as e:
        print(f"Error listing stories: {e}")


def view_story_details(page_id: str) -> None:
    """View detailed information about a specific story."""
    try:
        notion_manager = NotionStoryManager()

        # Get the page details
        page_response = notion_manager.client.pages.retrieve(page_id)
        # Handle async response
        if hasattr(page_response, "__dict__"):
            page = page_response.__dict__
        elif isinstance(page_response, dict):
            page = page_response
        else:
            page = {"properties": {}}
        properties = page.get("properties", {})

        print(f"\n📖 Story Details:")
        print("=" * 60)

        # Title
        title_prop = properties.get("Title", {})
        title = ""
        if title_prop.get("title"):
            title = title_prop["title"][0].get("text", {}).get("content", "Untitled")
        print(f"Title: {title}")

        # Status
        status_prop = properties.get("Status", {})
        status = status_prop.get("select", {}).get("name", "Unknown")
        print(f"Status: {status}")

        # Story components
        for component in ["Setting", "Characters", "Conflict", "Resolution"]:
            component_prop = properties.get(component, {})
            content = ""
            if component_prop.get("rich_text"):
                content = (
                    component_prop["rich_text"][0].get("text", {}).get("content", "")
                )

            if content:
                print(f"\n{component}:")
                print(f"{content}")

        # Get the full story content from blocks
        blocks_response = notion_manager.client.blocks.children.list(page_id)
        # Handle async response
        if hasattr(blocks_response, "__dict__"):
            blocks = blocks_response.__dict__
        elif isinstance(blocks_response, dict):
            blocks = blocks_response
        else:
            blocks = {"results": []}
        print(f"\nComplete Story:")
        print("-" * 40)

        for block in blocks.get("results", []):
            if block.get("type") == "paragraph":
                paragraph = block.get("paragraph", {})
                if paragraph.get("rich_text"):
                    text = paragraph["rich_text"][0].get("text", {}).get("content", "")
                    if text:
                        print(text)
            elif block.get("type") == "heading_1":
                heading = block.get("heading_1", {})
                if heading.get("rich_text"):
                    text = heading["rich_text"][0].get("text", {}).get("content", "")
                    if text:
                        print(f"\n{text}")
                        print("=" * len(text))

    except Exception as e:
        print(f"Error viewing story details: {e}")


def update_story_status(page_id: str, new_status: str) -> None:
    """Update the status of a story."""
    try:
        notion_manager = NotionStoryManager()

        # Update the status
        notion_manager.client.pages.update(
            page_id=page_id, properties={"Status": {"select": {"name": new_status}}}
        )

        print(f"✅ Story status updated to '{new_status}'")

    except Exception as e:
        print(f"Error updating story status: {e}")


def delete_story(page_id: str) -> None:
    """Delete (archive) a story from the database."""
    try:
        notion_manager = NotionStoryManager()

        # Archive the page
        notion_manager.delete_story_page(page_id)

        print("✅ Story deleted (archived) successfully")

    except Exception as e:
        print(f"Error deleting story: {e}")


def search_stories(query: str, limit: int = 10) -> None:
    """Search for stories by title or content."""
    try:
        notion_manager = NotionStoryManager()

        # Query the database with a filter
        if not notion_manager.database_id:
            raise ValueError("Database ID is required")
        response_raw = notion_manager.client.databases.query(
            database_id=notion_manager.database_id,
            filter={
                "or": [
                    {"property": "Title", "title": {"contains": query}},
                    {"property": "Setting", "rich_text": {"contains": query}},
                    {"property": "Characters", "rich_text": {"contains": query}},
                ]
            },
            page_size=limit,
        )

        # Handle async response
        if hasattr(response_raw, "__dict__"):
            response = response_raw.__dict__
        elif isinstance(response_raw, dict):
            response = response_raw
        else:
            response = {"results": []}

        pages = response.get("results", [])

        if not pages:
            print(f"No stories found matching '{query}'")
            return

        print(f"\n🔍 Search Results for '{query}' (showing {len(pages)}):")
        print("=" * 60)

        for i, page in enumerate(pages, 1):
            properties = page.get("properties", {})

            # Get title
            title_prop = properties.get("Title", {})
            title = ""
            if title_prop.get("title"):
                title = (
                    title_prop["title"][0].get("text", {}).get("content", "Untitled")
                )

            print(f"{i}. {title}")
            print(f"   ID: {page.get('id', 'Unknown')}")
            print()

    except Exception as e:
        print(f"Error searching stories: {e}")


def main():
    """Main function with interactive menu."""
    load_dotenv()

    # Check if environment variables are set
    if not os.getenv("NOTION_TOKEN") or not os.getenv("NOTION_DATABASE_ID"):
        print("❌ Missing environment variables. Please run setup_notion.py first.")
        return

    while True:
        print("\n📚 Notion Story Manager")
        print("=" * 30)
        print("1. List recent stories")
        print("2. View story details")
        print("3. Update story status")
        print("4. Delete story")
        print("5. Search stories")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            limit = input("How many stories to show? (default: 10): ").strip()
            limit = int(limit) if limit.isdigit() else 10
            list_stories(limit)

        elif choice == "2":
            page_id = input("Enter story page ID: ").strip()
            if page_id:
                view_story_details(page_id)
            else:
                print("❌ Please provide a valid page ID")

        elif choice == "3":
            page_id = input("Enter story page ID: ").strip()
            if page_id:
                print("Available statuses: Generated, Draft, Published")
                new_status = input("Enter new status: ").strip()
                if new_status:
                    update_story_status(page_id, new_status)
                else:
                    print("❌ Please provide a valid status")
            else:
                print("❌ Please provide a valid page ID")

        elif choice == "4":
            page_id = input("Enter story page ID: ").strip()
            if page_id:
                confirm = (
                    input("Are you sure you want to delete this story? (y/N): ")
                    .strip()
                    .lower()
                )
                if confirm == "y":
                    delete_story(page_id)
                else:
                    print("Deletion cancelled")
            else:
                print("❌ Please provide a valid page ID")

        elif choice == "5":
            query = input("Enter search query: ").strip()
            if query:
                limit = input("How many results to show? (default: 10): ").strip()
                limit = int(limit) if limit.isdigit() else 10
                search_stories(query, limit)
            else:
                print("❌ Please provide a search query")

        elif choice == "6":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please enter a number between 1-6.")


if __name__ == "__main__":
    main()

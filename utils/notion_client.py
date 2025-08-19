"""
Fixed Notion client for storing AI-generated story data in a Notion database.
Handles async/sync issues and proper type annotations.
"""

import os
from typing import Dict, Any, Optional, Union
from notion_client import Client
from notion_client.errors import APIResponseError


class NotionStoryManager:
    """Manages story data storage in Notion database."""

    def __init__(self, database_id: Optional[str] = None):
        """
        Initialize Notion client.

        Args:
            database_id: Notion database ID. If not provided, will try to get from env.
        """
        self.notion_token = os.getenv("NOTION_TOKEN")
        if not self.notion_token:
            raise ValueError("NOTION_TOKEN environment variable is required")

        self.client = Client(auth=self.notion_token)
        self.database_id = database_id or os.getenv("NOTION_DATABASE_ID")
        if not self.database_id:
            raise ValueError(
                "NOTION_DATABASE_ID environment variable or parameter is required"
            )

    def _truncate_text(self, text: str, max_length: int = 1900) -> str:
        """
        Truncate text to fit Notion's character limit with ellipsis.

        Args:
            text: Text to truncate
            max_length: Maximum length (default 1900 to be safe)

        Returns:
            Truncated text
        """
        if len(text) <= max_length:
            return text
        return text[: max_length - 3] + "..."

    def create_story_page(self, story_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new story page in the Notion database.

        Args:
            story_data: Dictionary containing story information

        Returns:
            Created page data
        """
        try:
            # Prepare the page properties based on your database structure
            properties = {
                "Title": {
                    "title": [
                        {
                            "text": {
                                "content": story_data.get("prompt", "Untitled Story")[
                                    :100
                                ]
                            }
                        }
                    ]
                },
                "Status": {"select": {"name": "Generated"}},
            }

            # Add custom properties if they exist in your database
            if "setting" in story_data:
                properties["Setting"] = {
                    "rich_text": [
                        {
                            "text": {
                                "content": self._truncate_text(story_data["setting"])
                            }
                        }
                    ]
                }

            if "characters" in story_data:
                properties["Characters"] = {
                    "rich_text": [
                        {
                            "text": {
                                "content": self._truncate_text(story_data["characters"])
                            }
                        }
                    ]
                }

            if "conflict" in story_data:
                properties["Conflict"] = {
                    "rich_text": [
                        {
                            "text": {
                                "content": self._truncate_text(story_data["conflict"])
                            }
                        }
                    ]
                }

            if "resolution" in story_data:
                properties["Resolution"] = {
                    "rich_text": [
                        {
                            "text": {
                                "content": self._truncate_text(story_data["resolution"])
                            }
                        }
                    ]
                }

            # Store ideas in the page content instead of as a property
            # since the database doesn't have an Ideas property yet

            # Create page content blocks
            children = [
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [
                            {"type": "text", "text": {"content": "Generated Ideas"}}
                        ]
                    },
                }
            ]

            # Add ideas if available
            if "ideas" in story_data and story_data["ideas"]:
                children.append(
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": self._truncate_text(
                                            story_data.get("ideas", "")
                                        )
                                    },
                                }
                            ]
                        },
                    }
                )

            # Add complete story heading and content
            children.extend(
                [
                    {
                        "object": "block",
                        "type": "heading_1",
                        "heading_1": {
                            "rich_text": [
                                {"type": "text", "text": {"content": "Complete Story"}}
                            ]
                        },
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": self._truncate_text(
                                            story_data.get("story", "")
                                        )
                                    },
                                }
                            ]
                        },
                    },
                ]
            )

            # Create the page
            response = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties,
                children=children,
            )

            # Convert response to dict if it's not already
            if hasattr(response, "__dict__"):
                return response.__dict__
            elif isinstance(response, dict):
                return response
            else:
                return {"id": str(response)}

        except APIResponseError as e:
            print(f"Notion API error: {e}")
            raise
        except Exception as e:
            print(f"Error creating story page: {e}")
            raise

    def get_story_pages(self, limit: int = 10) -> Dict[str, Any]:
        """
        Retrieve story pages from the database.

        Args:
            limit: Maximum number of pages to retrieve

        Returns:
            Database query response
        """
        try:
            if not self.database_id:
                raise ValueError("Database ID is required")
            response = self.client.databases.query(
                database_id=self.database_id, page_size=limit
            )

            # Convert response to dict if it's not already
            if hasattr(response, "__dict__"):
                return response.__dict__
            elif isinstance(response, dict):
                return response
            else:
                return {"results": []}

        except APIResponseError as e:
            print(f"Notion API error: {e}")
            raise
        except Exception as e:
            print(f"Error retrieving story pages: {e}")
            raise

    def update_story_page(
        self, page_id: str, story_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update an existing story page.

        Args:
            page_id: Notion page ID
            story_data: Updated story data

        Returns:
            Updated page data
        """
        try:
            properties = {}

            # Update properties based on provided data
            if "prompt" in story_data:
                properties["Title"] = {
                    "title": [{"text": {"content": story_data["prompt"][:100]}}]
                }

            if "setting" in story_data:
                properties["Setting"] = {
                    "rich_text": [{"text": {"content": story_data["setting"]}}]
                }

            if "characters" in story_data:
                properties["Characters"] = {
                    "rich_text": [{"text": {"content": story_data["characters"]}}]
                }

            if "conflict" in story_data:
                properties["Conflict"] = {
                    "rich_text": [{"text": {"content": story_data["conflict"]}}]
                }

            if "resolution" in story_data:
                properties["Resolution"] = {
                    "rich_text": [{"text": {"content": story_data["resolution"]}}]
                }

            response = self.client.pages.update(page_id=page_id, properties=properties)

            # Convert response to dict if it's not already
            if hasattr(response, "__dict__"):
                return response.__dict__
            elif isinstance(response, dict):
                return response
            else:
                return {"id": str(response)}

        except APIResponseError as e:
            print(f"Notion API error: {e}")
            raise
        except Exception as e:
            print(f"Error updating story page: {e}")
            raise

    def delete_story_page(self, page_id: str) -> bool:
        """
        Delete a story page.

        Args:
            page_id: Notion page ID

        Returns:
            True if successful
        """
        try:
            self.client.pages.update(page_id=page_id, archived=True)
            return True

        except APIResponseError as e:
            print(f"Notion API error: {e}")
            raise
        except Exception as e:
            print(f"Error deleting story page: {e}")
            raise

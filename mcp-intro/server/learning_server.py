#!/usr/bin/env python3
"""Learning MCP server exposing topic-search tools.

This module defines a small MCP server that provides the `search_topics`
tool for searching programming topics stored in `data/topics.json`.

The server is runnable as a script: `python3 server/learning_server.py`.
"""

import json
from pathlib import Path


from fastmcp import FastMCP

mcp = FastMCP("Programming Learning Server")


@mcp.tool
def search_topics(query: str) -> list[dict]:
    """Search programming topics by title or keyword.

    Args:
        query: The search string to match against topic titles and key concepts.

    Returns:
        A list of matching topic dictionaries. Each dictionary contains the
        keys: `id`, `title`, `summary`, and `key_concepts`.
    """

    search_query = query.lower().strip()

    if not search_query:
        return []
    TOPICS_FILE = Path(__file__).parent.parent / "data" / "topics.json"
    with open(TOPICS_FILE, "r", encoding="utf-8") as file:
        topics = json.load(file)

    matching_topics = []

    for topic in topics:
        is_match = False
        if search_query in topic["title"].lower():
            is_match = True
        for key_concept in topic["key_concepts"]:
            if search_query in key_concept.lower():
                is_match = True
        if is_match:
            matching_topics.append({
                "id": topic["id"],
                "title": topic["title"],
                "summary": topic["summary"],
                "key_concepts": topic["key_concepts"]
            })
    return matching_topics


@mcp.tool
def get_topic_details(topic_id: str) -> dict:
    """Return full information for a topic by id."""

    normalized_topic_id = topic_id.strip()

    if not normalized_topic_id:
        return {"error": "A topic id is required."}
    TOPICS_FILE = Path(__file__).parent.parent / "data" / "topics.json"
    with open(TOPICS_FILE, "r", encoding="utf-8") as file:
        topics = json.load(file)

    for topic in topics:
        if topic["id"] == normalized_topic_id:
            return topic
    return {"error": "Topic not found."}


if __name__ == "__main__":
    mcp.run()

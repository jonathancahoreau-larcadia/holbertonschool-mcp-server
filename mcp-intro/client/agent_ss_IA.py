#!/usr/bin/env python3

"""Simple MCP client agent script.

This module provides a small CLI agent that queries the learning MCP
server for topics and prints topic details. It expects a topic or query
string as command-line arguments.
"""

import sys
import asyncio

from fastmcp import Client


async def main():
    """Run the CLI agent.

    Reads the command-line arguments to form a question, calls the
    `search_topics` tool, and if a topic is found, retrieves and prints
    the topic details using `get_topic_details`.
    """

    if len(sys.argv) < 2:
        print('Usage: python3 -m client.agent "topic or question"')
        return

    question = " ".join(sys.argv[1:])

    client = Client("server/learning_server.py")

    async with client:
        search_result = await client.call_tool(
            "search_topics",
            {"query": question}
        )
        topics = search_result.data
        if not topics:
            print("No matching topic found.")
            return

        topic_id = topics[0].get("id")

        detail_result = await client.call_tool(
            "get_topic_details",
            {"topic_id": topic_id}
        )
        details = detail_result.data

        title = details.get("title")
        summary = details.get("summary")
        prerequisites = "\n".join(
            f"- {item}" for item in details["prerequisites"]
        )
        key_concepts = "\n".join(
            f"- {item}" for item in details["key_concepts"]
        )
        common_mistakes = "\n".join(
            f"- {item}" for item in details["common_mistakes"]
        )
        practice_idea = details["practice_idea"]

        response = f"""# Study Recommendation: {title}

## Why This Topic Is Relevant

{summary}

## Prerequisites

{prerequisites}

## Key Concepts

{key_concepts}

## Practice Idea

{practice_idea}

## Common Mistakes to Avoid

{common_mistakes}
"""
    with open(
        "output/sample_agent_response.md",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(response)

    print(response)
    print("Response saved to output/sample_agent_response.md")


if __name__ == "__main__":
    asyncio.run(main())

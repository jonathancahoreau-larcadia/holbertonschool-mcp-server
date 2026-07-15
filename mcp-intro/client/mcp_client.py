#!/usr/bin/env python3
"""MCP client example.

This module demonstrates a simple FastMCP client that calls the
`search_topics` tool to query topics (example: "decorators").

Note: This is an example script; adjust configuration before use.
"""
import asyncio

from fastmcp import Client
from server.learning_server import mcp

client = Client(mcp)


async def test_client():
    """Run a simple client call to the `search_topics` tool.

    Opens the `client` context, invokes `call_tool` with a query string,
    and prints the returned result.
    """
    async with client:
        tools = await client.list_tools()
        content = await client.read_resource("topics://catalog")
        result = await client.call_tool(
            "get_topic_details",
            {"topic_id": "python-decorators"},
        )
        print(tools)



if __name__ == "__main__":
    asyncio.run(test_client())

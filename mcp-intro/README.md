## MCP Architecture Summary

The Model Context Protocol, or MCP, is a standard protocol that allows AI applications to connect to external tools and data sources in a structured way.

The MCP host is the main AI application used by the user. It receives the user's request, manages the AI model, and decides which MCP server may be useful.

The MCP client is the communication component between the host and a specific MCP server. It connects to the server, discovers its available capabilities, sends tool calls or resource requests, and returns the results to the host. A host can connect to several MCP servers by using one MCP client for each server.

The MCP server is the program that exposes tools and resources. In this project, the server reads programming study information from `data/topics.json` and makes that information available to the client.

MCP tools are functions that perform specific actions. For example, a tool can search for a programming topic, retrieve topic details, or suggest a practice activity.

MCP resources are read-only data exposed by the server. For example, the complete programming topic catalog can be exposed as a resource.

A server should expose only the capabilities that are necessary for its purpose. This reduces security risks, prevents unwanted actions, and makes the server easier to understand, test, and maintain.

For example, when a user asks what they should review before studying Python decorators, the MCP host can use its MCP client to call a tool on the learning server. The server reads the relevant information from `topics.json`, returns it to the client, and the host uses it to generate a student-friendly response.

## Run the MCP Server

FastMCP requires Python 3.10 or newer.

Create a virtual environment from the root of the project:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

Start the MCP server from the root of the `mcp-intro` directory:

```bash
python server/learning_server.py
```

The server starts with the following name:

```text
Programming Learning Server
```

The server uses the `stdio` transport and waits for an MCP client connection.

To stop the server, press:

```text
Ctrl + C
```

When the server is stopped manually, Python may display a `KeyboardInterrupt` message. This is expected and does not mean that the server failed to start.

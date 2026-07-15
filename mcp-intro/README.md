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

## Testing the MCP Server

The MCP server was tested with a local FastMCP client before being connected to an agent.

The tests were executed from the root of the `mcp-intro` directory with:

```bash
python3 -m client.mcp_client
```

The client successfully connected to the server and discovered the following MCP tools:

```text
search_topics
get_topic_details
```

The `search_topics` tool was tested with a valid search query:

```text
decorators
```

The server returned the matching `Python Decorators` topic.

The `get_topic_details` tool was tested with the following valid topic identifier:

```text
python-decorators
```

The server returned the complete information associated with the topic.

An invalid topic identifier was also tested to verify error handling. The server returned an understandable error instead of stopping unexpectedly.

The read-only catalog resource was tested with the following URI:

```text
topics://catalog
```

The resource returned the available topic catalog, including topic identifiers and titles.

Example catalog response:

```json
[
  {
    "id": "python-decorators",
    "title": "Python Decorators"
  },
  {
    "id": "python-async",
    "title": "Python Async Programming"
  },
  {
    "id": "python-list-comprehensions",
    "title": "Python List Comprehensions"
  },
  {
    "id": "python-oop",
    "title": "Python Object-Oriented Programming"
  },
  {
    "id": "rest-apis",
    "title": "REST APIs"
  }
]
```

These tests confirmed that:

* the MCP server starts successfully;
* the client can connect to the server;
* the MCP tools are visible;
* `search_topics` works with a valid query;
* `get_topic_details` works with a valid topic identifier;
* invalid inputs are handled correctly;
* the catalog resource can be read successfully.

## Run the MCP Agent

The project includes a simple deterministic agent-like client in:

```text
client/agent.py
```

The agent receives a programming topic or student question from the command line. It then starts the MCP server through the `stdio` transport and calls the server tools through MCP.

The agent follows these steps:

1. Receives the student's question or topic.
2. Calls the `search_topics` MCP tool.
3. Retrieves the identifier of the first matching topic.
4. Calls the `get_topic_details` MCP tool.
5. Formats the returned data as a student-friendly Markdown response.
6. Saves the response in `output/sample_agent_response.md`.

The agent does not call the server functions directly. It connects to `server/learning_server.py` through a FastMCP client.

Run the agent from the root of the `mcp-intro` directory:

```bash
python3 -m client.agent "python decorators"
```

A complete question may also be provided:

```bash
python3 -m client.agent \
  "I want to study Python decorators. What should I review first?"
```

The MCP server is started automatically as a local subprocess using the `stdio` transport. It is not necessary to start the server manually before running the agent.

The generated response includes, when available:

* the recommended topic;
* an explanation of why the topic is relevant;
* the required prerequisites;
* the key concepts to review;
* a small practice idea;
* common mistakes to avoid.

Example response:

```markdown
# Study Recommendation: Python Decorators

## Why This Topic Is Relevant

Python decorators wrap a function to add or modify its behavior without changing the original function.

## Prerequisites

- Functions
- Scope

## Key Concepts

- Higher-order functions
- Wrapper functions

## Practice Idea

Create a decorator that logs function calls.

## Common Mistakes to Avoid

- Forgetting to return the wrapper function
- Calling the decorated function instead of returning it
```

The response is printed in the terminal and saved automatically in:

```text
output/sample_agent_response.md
```

The saved response can be inspected with:

```bash
cat output/sample_agent_response.md
```

If no matching topic is found, the agent displays:

```text
No matching topic found.
```

This agent is intentionally simple. It does not use memory, autonomous planning, multiple agents, or an LLM. Its purpose is to demonstrate that the learning server can be consumed as an external MCP capability.

# MCP Servers in Python

## Description

This project implements a local **Programming Learning MCP Server** using Python and FastMCP.

The server exposes programming study information stored in a local JSON file. An MCP client or agent can connect to the server to:

* Search for programming topics.
* Retrieve detailed information about a specific topic.
* Read the complete topic catalog as a read-only resource.
* Generate a student-friendly study response.

The project demonstrates how an MCP host, client, and server communicate using the Model Context Protocol.

The server uses the `stdio` transport, meaning that the MCP client starts the server as a subprocess and communicates with it through standard input and standard output.

---

## MCP Architecture Summary

The Model Context Protocol, or MCP, is a standard protocol that allows AI applications to connect to external tools and data sources in a structured way.

The **MCP host** is the main AI application used by the user. It receives the user's request, manages the AI model or agent logic, and decides which MCP server may be useful.

The **MCP client** is the communication component between the host and a specific MCP server. It connects to the server, discovers its available capabilities, sends tool calls or resource requests, and returns the results to the host. A host can connect to several MCP servers by using one MCP client for each server.

The **MCP server** is the program that exposes tools and resources. In this project, the server reads programming study information from `data/topics.json` and makes that information available to the client.

MCP tools are functions that perform specific actions. In this project, tools can search for programming topics and retrieve detailed information about a topic.

MCP resources are read-only data exposed by the server. In this project, the complete programming topic catalog is exposed as a resource.

A server should expose only the capabilities that are necessary for its purpose. This reduces security risks, prevents unwanted actions, and makes the server easier to understand and maintain.

---

## Requirements

The project requires:

* Python 3.10 or later.
* `pip`.
* Python virtual environments.
* The dependencies listed in `requirements.txt`.
* Node.js and `npx` for MCP Inspector and the third-party Filesystem MCP Server review.

FastMCP requires Python 3.10 or later.

No API key, password, token, or external model provider is required for the local implementation.

---

## Setup

Clone the repository and move into the project directory:

```bash
cd mcp-intro
```

Create a Python virtual environment:

```bash
python3 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

The `.env.example` file is included as a configuration template. This local implementation does not require a secret or API key.

Secrets must never be committed to the repository. A local `.env` file should remain excluded by `.gitignore`.

---

## How to Run the Server

From the root of the `mcp-intro` directory, activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the server with:

```bash
python server/learning_server.py
```

The MCP server is named:

```text
Programming Learning Server
```

It uses the `stdio` transport.

When launched directly, the server waits for an MCP client to communicate with it through standard input and standard output.

Stop the server with:

```text
Ctrl + C
```

A `KeyboardInterrupt` message may appear after manually stopping the server. This is expected and does not mean that the MCP server failed.

---

## How to Test the Server

The project includes a FastMCP test client in `client/mcp_client.py`.

Run it from the project root:

```bash
python3 -m client.mcp_client
```

The client starts the MCP server and connects to it using `stdio`.

It can be used to verify that:

* The server starts correctly.
* The tools are available.
* `search_topics` returns matching topics.
* `get_topic_details` returns detailed topic information.
* The `topics://catalog` resource can be read.
* MCP responses do not contain an error.

A successful call to `get_topic_details` returns information such as:

```text
id
title
summary
prerequisites
key_concepts
common_mistakes
practice_idea
```

The `get_topic_details` tool requires an exact topic identifier.

For example:

```text
python-decorators
```

is a valid identifier, while:

```text
python decorators
```

is not an exact identifier.

---

## How to Run the Agent

The simple agent is implemented in:

```text
client/agent.py
```

Run the agent from the project root:

```bash
python3 -m client.agent "python decorators"
```

It can also receive a complete question:

```bash
python3 -m client.agent \
  "I want to study Python decorators. What should I review first?"
```

The agent performs the following workflow:

1. Receives the user's topic or question.
2. Starts the MCP server using `stdio`.
3. Calls the `search_topics` tool.
4. Retrieves the identifier of the first matching topic.
5. Calls `get_topic_details` with the exact identifier.
6. Formats the returned data as a student-friendly Markdown response.
7. Prints the response in the terminal.
8. Saves the response to:

```text
output/sample_agent_response.md
```

The agent is deterministic and does not require a language model or an external API.

When no matching topic is found, it displays:

```text
No matching topic found.
```

---

## Available Tools

### `search_topics`

Searches the local programming topic dataset.

The tool accepts a text query and compares it with topic identifiers and titles.

Example search:

```text
python decorators
```

The tool may return the topic:

```text
python-decorators
```

This tool is useful when the user knows the topic name but not its exact identifier.

### `get_topic_details`

Retrieves the complete information for one programming topic.

The tool requires the exact topic identifier.

Example identifier:

```text
python-decorators
```

The returned data includes:

* `id`
* `title`
* `summary`
* `prerequisites`
* `key_concepts`
* `common_mistakes`
* `practice_idea`

The tool does not perform a partial search. The client should normally call `search_topics` first and then use the returned identifier with `get_topic_details`.

---

## Available Resources

### `topics://catalog`

The server exposes the programming topic catalog as a read-only MCP resource.

The resource contains the identifiers and titles of the available programming topics.

Example resource content:

```json
[
  {
    "id": "python-decorators",
    "title": "Python Decorators"
  },
  {
    "id": "python-async",
    "title": "Python Async Programming"
  }
]
```

The resource does not modify the JSON dataset.

Connecting to the server does not automatically return the resource content. The MCP client must explicitly send a resource read request for:

```text
topics://catalog
```

A resource is appropriate here because the catalog is read-only information rather than an action.

---

## Third-Party MCP Server Review

A third-party **Filesystem MCP Server** was inspected using MCP Inspector.

A small test directory was created:

```bash
mkdir -p /home/palms/mcp-test
```

The server was launched through MCP Inspector with:

```bash
npx -y @modelcontextprotocol/inspector \
  npx @modelcontextprotocol/server-filesystem \
  /home/palms/mcp-test
```

The server was only allowed to access:

```text
/home/palms/mcp-test
```

The connection was successfully established, and MCP Inspector displayed the allowed directory.

A Filesystem MCP Server may expose operations that can:

* List directories.
* Read files.
* Create files or directories.
* Modify files.
* Move files.
* Delete files or directories.

These capabilities can be useful, but they can also be destructive.

Before using a third-party MCP server, the following elements should be reviewed:

* The identity and reputation of the developer.
* The source code of the server when available.
* The installation command.
* The dependencies installed by the package.
* The tools and resources exposed by the server.
* The files and directories the server can access.
* Whether the server can modify or delete data.
* Whether it requires tokens, passwords, or API keys.
* Whether it communicates with an external network service.
* Whether its permissions are larger than necessary.
* Whether its returned data can be trusted.

The Filesystem MCP Server did not require an API key. However, it required a list of directories it was allowed to access.

Giving it access to the complete home directory would expose more personal and project files than necessary. Restricting it to `/home/palms/mcp-test` applies the principle of least privilege and limits the possible damage caused by an incorrect or unwanted tool call.

A third-party MCP server should never be trusted only because it successfully connects.

---

## Example Output

The following is a shortened example of the response produced for Python decorators:

```markdown
# Python Decorators

## Summary

Python decorators allow a function to modify or extend the behavior of
another function without directly changing its implementation.

## What to Review First

- Functions as objects
- Nested functions
- Closures
- `*args` and `**kwargs`

## Key Concepts

- Passing a function as an argument
- Returning a function
- Wrapper functions
- The `@decorator` syntax

## Practice Activity

Create a decorator that prints a message before and after a function is
executed.
```

The complete generated response is saved in:

```text
output/sample_agent_response.md
```

---

## Known Limitations

The implementation has the following limitations:

* The server only uses a small local JSON dataset.
* New topics must be added manually to `data/topics.json`.
* The search is based on text matching and does not understand synonyms or semantic meaning.
* `get_topic_details` requires an exact topic identifier.
* The agent automatically selects the first search result.
* The agent does not ask the user to choose when several topics match.
* The agent is deterministic and does not use a language model to reformulate complex questions.
* The server only uses local `stdio` communication.
* It is not exposed through HTTP or a remote network.
* The server does not implement authentication or authorization.
* The implementation does not include a database.
* The server does not validate information from an external source because all data comes from the local JSON file.

One observed limitation was that a human-readable topic such as `python decorators` could not be passed directly to `get_topic_details`. The client first had to call `search_topics` and retrieve the exact identifier `python-decorators`.

---

## Reflection

### What problem does MCP solve?

MCP solves the problem of connecting AI applications to external tools and data sources in a standard and reusable way.

Without MCP, every AI application would need a custom integration for every API, database, file system, or external program.

With MCP, a developer can create a server that exposes clearly defined capabilities. Compatible MCP clients can discover and use these capabilities without needing a completely different communication system for every integration.

### What is the difference between an MCP tool and an MCP resource?

An MCP tool is a callable function that performs an action or computation.

For example, `search_topics` receives a search query and performs a search in the topic dataset.

An MCP resource provides read-only information identified by a URI.

For example, `topics://catalog` provides the complete list of available topics without modifying the data.

A tool represents something the client can ask the server to do, while a resource represents information the client can ask the server to read.

### What does your MCP server expose?

The server exposes two tools:

* `search_topics`
* `get_topic_details`

It also exposes one read-only resource:

* `topics://catalog`

The information is loaded from the local file:

```text
data/topics.json
```

### How does your agent use the MCP server?

The agent connects to the server through an MCP client using `stdio`.

It first calls `search_topics` with the user's request. It retrieves the identifier of the first matching topic and then calls `get_topic_details`.

The agent uses the returned structured data to create a readable Markdown study response.

The response is displayed in the terminal and saved to:

```text
output/sample_agent_response.md
```

### What should you check before using a third-party MCP server?

Before using a third-party MCP server, I should check:

* Who developed it.
* Whether its source code can be reviewed.
* Which dependencies it installs.
* Which tools and resources it exposes.
* Which local files or directories it can access.
* Whether it can modify or delete data.
* Whether it connects to an external service.
* Whether it requires secrets or API keys.
* Whether its permissions can be restricted.
* Whether it follows the principle of least privilege.

I should test it in an isolated directory before giving it access to important data.

### What limitation did you observe in your implementation?

The main limitation is that the server uses a small static JSON dataset and a simple text search.

The agent cannot understand every possible way a user may describe a topic. It also selects the first matching result automatically.

Additionally, `get_topic_details` requires an exact identifier. The client must therefore call `search_topics` before requesting the full details of a topic.

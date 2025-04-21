# MCP Agent Creation Tutorial
This repository provides the base project needed for the Model Context Protocol (MCP) Agentic Tool Creation Turtorial on Confluence.  The demonstration goes through the SErven Sent Events (SSE) approach to MCP Server implementation.  This example showcases how to create an interactive AI application that can dynamically access external tools and data sources.

Please follow ![this tutorial](https://skywarditsolutions.atlassian.net/wiki/x/AgA_WQ?atlOrigin=eyJpIjoiNjUyMjRiNTljODk1NDAxN2I4YTFmMmJkNTE4YjZiNDQiLCJwIjoiYyJ9) to complete this project.

## Prerequistes

- Ubuntu operating system or wsl
- Python 3.12.3
- pip (Python package installer)

## Setup

1. Clone this specific repository:

```
 git clone https://github.com/yimam-skyward/MCP_Agent_Tutorial.git
```
```
cd MCP_Agent_Tutorial
```

2. Create a new environment and install the required dependencies (need to be using Ubuntu OS or WSL)

```
python3 -m venv .venv
source .venv/bin/activate
```

```
pip install -r requirements.txt
```

WSL was giving me problems so i had to do `pip install --break-system-packages -r requirements.txt`

Set up your environment variables:
```
cp .env.example .env
```

Open the `.env` file and add your Bedrock API keys from AWS

## To Run
1. In one terminal, start the server:

```
python sse_server.py
```

2. In another terminal, start the client:

```
python sse_client.py
```

The client and server are configured to connect over `localhost:5553`.


## What is happening / Technical Details

The script has 3 major parties in play: The LLM/Client, the MCP Server, and the User. These components interact with each other to get the User’s prompt answered.  The MCP Server is only called if the LLM says one of the Tool functions will be needed.  

### Model Context Protocol Flow

1. User sends a message through the client interface
    - Where it says `Input:` 
2. The language model (Claude) receives the message and evaluates whether it needs external data or tools
3. If a tool is needed, the model sends a structured request to the MCP Server
4. The MCP Server processes the request and returns results
5. The model incorporates the tool results into its final response
6. The client displays the final response to the user

# Message Delivery Agent

A small HTTP service that wraps an AI agent. You send it a query, the agent
decides whether and how to deliver a message, and it returns a reply. The agent
runs entirely on a local model through Ollama (Gemma 4), orchestrated by the
OpenAI Agents SDK. No cloud calls, no API keys.

## What it does

The agent has one job: deliver messages to people over various channels.

Anything that is not "send a message to someone" kinda request is treated as out of scope.
The agent loop finishes when either a message was delivered, or there was not enough information to send one.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed.
- Ollama running locally with Gemma 4 pulled:

  ```bash
  ollama pull gemma4
  ```

  The default `gemma4` tag resolves to the E4B size. To use a different size,
  pull it (for example `ollama pull gemma4:12b`) and set `OLLAMA_MODEL`
  accordingly (see Configuration).

## Setup

From the project root:

```bash
uv sync
```

That creates a virtual environment and installs the dependencies listed in
`pyproject.toml` (`openai-agents`, `fastapi`, `uvicorn`).

## Run

```bash
uv run uvicorn app.server:app --reload
```

The server listens on http://localhost:8000.

If you are interested in the interaction with the model, you can enable HTTP trace logging for the client.

```bash
HTTP_TRACE=true uv run uvicorn app.server:app --reload
```

## Use

Send a query as a POST with a JSON body of the form `{"query": "..."}`:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Send a WhatsApp to Alice Johnson saying the meeting moved to 3pm"}'
```

You get back:

```json
{"reply": "Message delivered to Alice Johnson (+1-202-555-0101)."}
```

Try these to see the different end states:

- Happy path: `"Tell Bob Smith I am running late"`
- Unknown contact: `"Message Zoe Miller that the package arrived"`
- Missing information: `"Send a message"`
- Out of scope: `"What is the capital of France?"`

The contact book contains: Alice Johnson, Bob Smith, Carol White,
David Brown, Erin Davis. Edit `app/tools.py` to change it.

## Configuration

Both values are read from environment variables, with sensible defaults:

| Variable          | Default                        | Purpose                          |
| ----------------- | ------------------------------ | -------------------------------- |
| `OLLAMA_MODEL`    | `gemma4`                       | Which Ollama model the agent uses |
| `OLLAMA_BASE_URL` | `http://localhost:11434/v1`    | Ollama's OpenAI-compatible URL    |

Example:

```bash
OLLAMA_MODEL=gemma4:12b uv run uvicorn app.server:app --reload
```

## Project layout

```
learning-agent-development-with-python/
├── pyproject.toml      # dependencies and project metadata (uv)
├── README.md
└── app/
    ├── tools.py        # the two tool functions + the contact book
    ├── agent.py        # local model setup + agent definition + run helper
    └── server.py       # FastAPI app and the /query endpoint
```

## How it fits together

`server.py` receives the HTTP request and calls `run_agent(query)` from
`agent.py`. `run_agent` calls `Runner.run`, which drives the agent loop: the
model reads the query, may call the tools in `tools.py`, observes their
results, and loops until it produces a final text answer. That final answer
becomes the `reply` in the HTTP response.

## Notes

- Tracing is disabled (`set_tracing_disabled(True)`) so nothing is sent to
  OpenAI; the setup is fully local.
- The agent uses the async `Runner.run`, since the synchronous variant is not
  available for non-OpenAI models. FastAPI endpoints are async, so this is a
  natural fit.
- Local models are less reliable at tool-calling than frontier cloud models.
  If the agent misbehaves (skips a tool, invents a number), tightening the
  instructions in `app/agent.py` or trying a larger `gemma4` tag usually helps.

# Message Delivery Agent

A small HTTP service that wraps an AI agent. You send it a query, the agent decides whether and how to deliver a
message, and it returns a reply. The agent runs entirely on a local model through, orchestrated by the OpenAI Agents
SDK. No cloud calls, no API keys.

## What the demo does

The agent has one job: deliver messages to people over various channels.

Anything that is not "send a message to someone" kinda request is treated as out of scope.
The agent loop finishes when either a message was delivered, or there was not enough information to send one.

## Prerequisites

- [uv](https://github.com/astral-sh/uv) installed.
- [llama.cpp](https://github.com/ggml-org/llama.cpp) installed.
- [hugging face CLI](https://huggingface.co/docs/huggingface_hub/en/guides/cli) installed

## Setup

From the project root:

```bash
uv sync
```

That creates a virtual environment and installs the dependencies listed in
`pyproject.toml` (`openai-agents`, `fastapi`, `uvicorn`).

## Run

### Model

Start the model using `llama.cpp`.

```bash
./start-model.sh
```

or something like this

```bash
llama-server -hf ggml-org/gemma-4-E4B-it-GGUF --jinja --ctx-size 65536 --port 9000 --alias gemma-4
```

### Agent

Start the agent application.

```bash
./start-agent.sh
```

or something like this

```bash
uv run uvicorn app.server:app --reload
```

The server listens on http://localhost:8000.

## Use

Send a query as a POST with a JSON body of the form `{"query": "..."}`:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Send a WhatsApp to Alice Johnson saying the meeting moved to 3pm"}'
```

You get back:

```json
{
  "reply": "Message delivered to Alice Johnson via WhatsApp."
}
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

| Variable         | Default                    | Purpose                            |
|------------------|----------------------------|------------------------------------|
| `MODEL_NAME`     | `gemma-4`                  | Which model the agent uses.        |
| `MODEL_BASE_URL` | `http://localhost:9000/v1` | A OpenAI-compatible URL.           |
| `HTTP_TRACE`     | `false`                    | Enables client HTTP trace logging. |

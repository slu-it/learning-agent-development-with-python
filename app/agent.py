"""The message delivery agent, wired up to a local model.

This module configures the OpenAI Agents SDK to talk to a local model instead of OpenAI.
"""

import os

import httpx
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from openai import AsyncOpenAI

from app.http import _log_exchange
from app.tools import get_phone_number_of_contact, send_whatsapp_message, send_sms_message, \
    get_email_address_of_contact, send_email_message

# Local model configuration

MODEL_BASE_URL = os.getenv("MODEL_BASE_URL", "http://localhost:9000/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gemma-4")

# HTTP client with optional logging setup
_http_client = None
if os.getenv("HTTP_TRACE") == "true":
    _http_client = httpx.AsyncClient(event_hooks={"response": [_log_exchange]})

# Local models gnore the API key, but the OpenAI client requires a non-empty value.
_client = AsyncOpenAI(base_url=MODEL_BASE_URL, api_key="local-model", http_client=_http_client)

# Tracing tries to send data to OpenAI's servers. Disable it for a fully local,
# offline setup (otherwise the SDK looks for an OPENAI_API_KEY).
set_tracing_disabled(True)

_model = OpenAIChatCompletionsModel(model=MODEL_NAME, openai_client=_client)

# What each tool does and what arguments it takes lives in the tool docstrings
# in app/tools.py; the SDK sends that to the model automatically. These
# instructions only cover behavior: when to use the tools, when to stop, and
# what is out of scope.
INSTRUCTIONS = """\
You are a message delivery agent for an organisation.
Your only job is to deliver messages to people.

If no specific messaging channel is stated by the user, assume SMS with a phone number.
 
End the task and give a final answer in exactly one of these two cases:
- The message was delivered successfully. Confirm it and say who it went to and by what channel.
- You cannot proceed because information is missing. State clearly what is missing, for example an unknown recipient,
  no phone number on file, or an empty message.
 
You only deliver messages to people. Treat anything else (answering general
questions, looking things up, performing other tasks) as out of scope, and say
briefly that it is outside what you do.
"""

message_delivery_agent = Agent(
    name="Message Delivery Agent",
    instructions=INSTRUCTIONS,
    model=_model,
    tools=[
        get_email_address_of_contact,
        get_phone_number_of_contact,
        send_email_message,
        send_sms_message,
        send_whatsapp_message
    ],
)


async def run_agent(query: str) -> str:
    """Run the agent loop on a single query and return its final reply.

    Runner.run drives the loop: the model may call tools, observe their
    results, and call more tools, until it produces a final text answer. That
    final answer is returned here as the reply.
    """
    result = await Runner.run(message_delivery_agent, query)
    return result.final_output

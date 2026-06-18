"""Tool functions the message delivery agent is allowed to call.

Each function is decorated with @function_tool, which turns it into a tool the
agent can invoke. The OpenAI Agents SDK builds the tool's input schema from the
function signature and docstring, so type hints and a clear docstring matter.
"""

import logging

from agents import function_tool

logger = logging.getLogger(__name__)

# A small, hard-coded contact book for the demo.
# Keys are stored lowercase so that lookups can be case-insensitive.
_CONTACT_PHONE_NUMBERS: dict[str, str] = {
    "alice johnson": "+1-202-555-0101",
    "bob smith": "+1-202-555-0142",
    "carol white": "+1-202-555-0173",
    "david brown": "+1-202-555-0188",
    "erin davis": "+1-202-555-0199",
}

# A small, hard-coded contact book for the demo.
# Keys are stored lowercase so that lookups can be case-insensitive.
_CONTACT_EMAIL_ADDRESSES: dict[str, str] = {
    "alice johnson": "alice.johnson@example.com",
    "bob smith": "bobbysmith@cool.io",
    "carol white": "carol@white-family.com",
    "david brown": "david.brown@example.com",
    "erin davis": "davis_erin@example.org",
}


@function_tool
def get_phone_number_of_contact(name: str) -> str | None:
    """Look up the phone number for a contact by their name.

    The match is case-insensitive.
    Returns the phone number as a string, or None if the name is not found in the contact book.

    Args:
        name: The full name of the contact to look up.
    """
    phone = _CONTACT_PHONE_NUMBERS.get(name.strip().lower())
    logger.info("get_phone_number_of_contact(name=%r) -> %r", name, phone)
    return phone


@function_tool
def get_email_address_of_contact(name: str) -> str | None:
    """Look up the email address for a contact by their name.

    The match is case-insensitive.
    Returns the email address as a string, or None if the name is not found in the contact book.

    Args:
        name: The full name of the contact to look up.
    """
    phone = _CONTACT_EMAIL_ADDRESSES.get(name.strip().lower())
    logger.info("get_email_address_of_contact(name=%r) -> %r", name, phone)
    return phone


@function_tool
def send_email_message(email_address: str, message: str) -> str:
    """Send an email message to a contact.

    Args:
        email_address: The recipient's email address.
        message: The body of the message to deliver.
    """
    logger.info(
        "send_email_message(email_address=%r, message=%r) [SIMULATED, no real message sent]",
        email_address,
        message,
    )
    return f"Message delivered to {email_address}."


@function_tool
def send_sms_message(phone_number: str, message: str) -> str:
    """Send an SMS message to a contact.

    Args:
        phone_number: The recipient's phone number in international format.
        message: The body of the message to deliver.
    """
    logger.info(
        "send_sms_message(phone_number=%r, message=%r) [SIMULATED, no real message sent]",
        phone_number,
        message,
    )
    return f"Message delivered to {phone_number}."


@function_tool
def send_whatsapp_message(phone_number: str, message: str) -> str:
    """Send a WhatsApp message to a contact.

    Args:
        phone_number: The recipient's phone number in international format.
        message: The body of the message to deliver.
    """
    logger.info(
        "send_whatsapp_message(phone_number=%r, message=%r) [SIMULATED, no real message sent]",
        phone_number,
        message,
    )
    return f"Message delivered to {phone_number}."

import json
import logging

def handle_api_error(response):
    """ Handle API errors and log them.
    """
    try:
        error = json.loads(response.text)
    except json.decoder.JSONDecodeError:
        error = response.text
    logging.error(f"API Error: {response.status_code} - {error}")

def log_info(message):
    """Log the provided message as info.
    """
    logging.info(message)

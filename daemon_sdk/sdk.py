"""Daemon SDK - Minimal API for MVP Webhook-to-Slack Workflow

This module defines the basic functions that AI-generated workflows can use.
These function signatures provide the contract between the Backend API and
the AI-generated code that will eventually run on Cloud Run.

For MVP, we support three core operations:
1. Getting incoming webhook data
2. Retrieving secrets (e.g., Slack tokens)
3. Posting messages to Slack
"""

from typing import Dict, Any, Optional


def get_trigger_data() -> Dict[str, Any]:
    """Gets the incoming webhook payload.
    
    This function will be implemented by the Execution Worker to read
    the webhook data from the request context or environment.
    
    Returns:
        Dict containing the webhook payload data
        
    Example:
        ```python
        data = get_trigger_data()
        user_name = data.get('user_name')
        message = data.get('text')
        ```
    """
    # Implementation will read from environment/context
    pass


def get_secret(secret_name: str) -> str:
    """Gets a secret value (e.g., Slack token).
    
    This function will be implemented by the Execution Worker to call
    Google Cloud Secret Manager and retrieve the secret value.
    
    Args:
        secret_name: Name of the secret to retrieve
        
    Returns:
        The secret value as a string
        
    Example:
        ```python
        slack_token = get_secret('slack_bot_token')
        ```
    """
    # Implementation will call Secret Manager
    pass


def post_slack_message(token: str, channel: str, text: str) -> Dict[str, Any]:
    """Helper to post a message to Slack.
    
    This function will be implemented by the Execution Worker to use
    the 'requests' library to post to Slack's API.
    
    Args:
        token: Slack bot token
        channel: Slack channel ID or name  
        text: Message text to post
        
    Returns:
        Response from Slack API
        
    Example:
        ```python
        token = get_secret('slack_bot_token')
        response = post_slack_message(token, '#general', 'Hello from Daemon!')
        ```
    """
    # Implementation uses 'requests' library
    pass

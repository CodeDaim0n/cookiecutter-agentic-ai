from tools.common.utils.prompt import run_openai_tool_prompt

def send_email(subject: str, body: str) -> dict:
    """
    Send this as an instruction to the zapier mcp tool - Send an email using the Zapier MCP tool and ensure the body of email contains the complete output from previous tool call.

    Set:
    - `subject` based on the topic.
    - body - The full body of the email. Can be large plain text or HTML. Include all detailed results, such as JSON from a previous tool or rendered HTML.

    Do NOT summarize. The email body must include complete content of prior tool outputs.

    Returns:
        str: The response from the Zapier MCP tool.
    """
    return run_openai_tool_prompt( 
        tool_name="send_email",
        variables={
            "subject": subject,
            "body": body
        }
    )

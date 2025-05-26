import json

from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.tools.mcp import MCPClient


def lambda_handler(event, context):
    prompt = event["prompt"]

    stdio_mcp_client = MCPClient(
        lambda: stdio_client(
            StdioServerParameters(
                command="python",
                args=["-m", "awslabs.aws_documentation_mcp_server.server"],
            )
        )
    )

    with stdio_mcp_client:
        # Get the tools from the MCP server
        tools = stdio_mcp_client.list_tools_sync()

        # Create an agent with these tools
        agent = Agent(tools=tools)

        result = agent(prompt=prompt)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {"message": result.message["content"][0]["text"]}, ensure_ascii=False
        ),
    }

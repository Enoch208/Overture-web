from mcp.types import CallToolResult, TextContent


def create_text_response(text: str, is_error: bool = False) -> CallToolResult:
    return CallToolResult(content=[TextContent(type="text", text=text)], isError=is_error)

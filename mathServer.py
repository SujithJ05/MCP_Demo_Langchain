from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Math") # Initialized the mcp and given the server name as 'Math'

@mcp.tool()
def divide(a:int, b:int) -> int:
    """Divide two numbers together"""
    return a / b;

@mcp.tool()
def multiply(a:int, b:int) -> int:
    """Multiply two numbers together"""
    return a * b;

@mcp.tool()
def add(a:int, b:int) -> int:
    """Add two numbers together"""
    return a + b

@mcp.tool()
def subtract(a:int, b:int) -> int:
    """Subtract two numbers together"""
    return a - b;

# stdio -> it follows standard input output where the user would be able to give the input in the cmd line and get the output there itself
# Best to perform testing locally or when the server is instantiated locally
if __name__ == "__main__":
    mcp.run(transport="stdio");



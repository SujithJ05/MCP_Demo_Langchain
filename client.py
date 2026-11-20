from langchain_mcp_adapters.client import MultiServerMCPClient
# from langchain.agents import create_agent
from langchain.agents import create_agent
from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

import asyncio

async def main():
    client=MultiServerMCPClient(
        {
            "math":{
                "command":"python", # Tells the client how to start the server
                "args":["mathServer.py"],
                "transport":"stdio"
            },
            "weather":{
                "url":"http://localhost:8000/mcp/", # No need of command here since the server is already running
                "transport":"streamable-http"
            }
        }
    )


    import os
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

    tools = await client.get_tools() # Gets the tools from the client that has been assigned for multiple servers MCP Client
    
    model = ChatGroq(
        model="openai/gpt-oss-20b"
    )
    
    agent = create_agent(
    model,
    tools,
    system_prompt=(
        "You must use the mcp tools to answer the user's question. "
    )
)

    math_response = await agent.ainvoke(
        {
            "messages":
            [
                {
                    "role":"user",
                    "content":"What is (3+2)*5?"
                }
            ]
        }
    )

    final_message = math_response["messages"][-1]
    print("Agent's math response:", final_message.content)

if __name__ == "__main__":
    asyncio.run(main())
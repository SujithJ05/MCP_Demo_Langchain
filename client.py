from langchain_mcp_adapters.client import MultiServerMCPClient
# from langchain.agents import create_agent
from langchain.agents import create_agent
from langchain_groq import ChatGroq
import os
import asyncio

from dotenv import load_dotenv
load_dotenv()

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
            },
            "database":{
                "command":"python",
                "args":["databaseServer.py"],
                "transport":"stdio"
            }
        }
    )

    tools = await client.get_tools() # Gets the tools from the client that has been assigned for multiple servers MCP Client
    
    model = ChatGroq(
        model="openai/gpt-oss-20b"
    )
    
    agent = create_agent(
    model,
    tools,
    system_prompt=(
        "You must use the mcp tools to answer the user's question."
    )
)

    # database_response = await agent.ainvoke(
    #     {
    #         "messages":
    #         [
    #             {
    #                 "role":"user",
    #                 "content":"How many employees are there in the database?"
    #             }
    #         ]
    #     }
    # )

    # final_message = database_response["messages"][-1]
    # print("Agent's database response:", final_message.content)

    try:
        while True:
            user_input = input("\nYou: ")

            if user_input.lower() in ["exit", "quit"]:
                print("Exiting the chat loop")
                break
            
            print("\nAgent: ", end="", flush=True)

            try:
                response = await agent.ainvoke(
                    {
                        "messages":
                        [
                            {
                                "role":"user",
                                "content":user_input
                            }
                        ]
                    }
                )
            except Exception as e:
                print(f"\nError: {e}")
                continue
            
            final_message = response["messages"][-1]
            print(final_message.content, end="", flush=True) # Put end = "" and flush as true to test
            print("\n")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) # Runs the main function
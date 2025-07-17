import asyncio
 
from mcp import ClientSession
from mcp.client.sse import sse_client
 

async def main():
  
    async with sse_client("http://localhost:8010/sse") as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
           
            await session.initialize()
          
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

           


if __name__ == "__main__":
    asyncio.run(main())

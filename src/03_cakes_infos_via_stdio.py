import asyncio
 
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

 


async def main():
    
    server_params = StdioServerParameters(
        command="python",  
        args=["02_cakes_infos_server.py"],   
    )

     
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:            
            await session.initialize() 
            tools_result = await session.list_tools()
            
            #print("Available tools:")
            #for tool in tools_result.tools:
            #    print(f"  - {tool.name}: {tool.description}") 
            
            
            result = await session.call_tool("get_total_cakes_count")
            print(f"Nombre total  = {result.content[0].text}")
            
           
            result = await session.call_tool("get_cakes_by_sugar_threshold", arguments={"threshold": 15})
            print(f"Liste des gâteaux avec le taux du succre 15 :")
            for r in result.content:
                print(f"{r.text}")
            

if __name__ == "__main__":
    asyncio.run(main())
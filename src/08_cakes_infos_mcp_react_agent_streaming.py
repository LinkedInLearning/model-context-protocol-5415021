import asyncio
import uuid
 
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from langchain_openai.chat_models import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage,SystemMessage 
from langchain_mcp_adapters.tools import load_mcp_tools  
 

model = ChatOpenAI(
    temperature=0.1,
    model='gpt-4o'
)

system_prompt = SystemMessage("""
    You are a professional chatbot specializing in answering questions about the cakes sold by your company.
    To provide accurate responses, you will exclusively rely on the available tools and not your own memory.
    For small talk and greetings, you will maintain a professional and courteous tone in your replies.
    """
)


checkpointer=MemorySaver()

 
 
async def main():
   
     
    async with streamablehttp_client("http://localhost:8010/mcp") as (
        read_stream,
        write_stream,
        get_session_id,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()             
            tools = await  load_mcp_tools(session)                         
            cake_QnA_agent=   create_react_agent(
                                model=model,  
                                tools=tools,
                                prompt=system_prompt, 
                                debug=False,  
                                checkpointer=checkpointer)          
 
            config = {"configurable": {"thread_id": uuid.uuid4()}}
            inputs = {"messages":[HumanMessage("Suggest five cakes with a sugar content below 40%. Your answer should include the five cakes along with their sugar content")]}

            '''
            response = await  cake_QnA_agent.ainvoke(inputs, config)
            print("Step by Step execution : ")
            for message in response['messages']:
                print(message.pretty_repr())
            '''
            print("Step by Step execution (streaming):")
            async for event in cake_QnA_agent.astream(inputs, config):
                print("New event received:", event)

            

if __name__ == "__main__":
    asyncio.run(main())
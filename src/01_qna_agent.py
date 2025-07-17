
from typing import Optional
from langchain_openai.chat_models import ChatOpenAI
import pandas as pd
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage,SystemMessage 

 
model = ChatOpenAI( 
    
    temperature=1,
    max_tokens=1000,
    model='gpt-4o'
)
 
cakes_df = pd.read_csv("../Data/cakes_data.csv")

 
@tool
def get_cake_price(cake_name:str) -> Optional[float] :
    """
    This function retrieves the price of a cake based on a given name.  
    It searches for a partial match between the input name and the available cake names.  
    If a matching cake is found, its price is returned.  
    If no match is detected, the function returns None.
    """

   
    match_df = cakes_df[cakes_df["Nom-du-gâteau"].str.contains("^" + cake_name, case=False)]
    
    if len(match_df) == 0 : 
        return None
    else:
        return match_df["Prix"].iloc[0]
    


@tool
def get_cake_sugar(cake_name:str) -> Optional[float] :
    """
    This function retrieves the sugar content of a cake based on a given name.  
    It searches for a partial match between the input name and the available cake names.  
    If a matching cake is found, its sugar percentage is returned.  
    If no match is detected, the function returns None.
    """

   
    match_df = cakes_df[cakes_df["Nom-du-gâteau"].str.contains("^" + cake_name, case=False)]
    
    if len(match_df) == 0 : 
        return None
    else:
        return match_df["Taux-de-sucre-(%)"].iloc[0]
   
@tool
def get_cake_names(n:int) -> list[str] :
    """
    This function returns a list of available cake names, limited to a specified number.  
    It retrieves the names from the available data source.  
    The function takes an integer parameter representing the maximum number of cake names to return.  
    If the requested number exceeds the total available cakes, it returns all available names.
    """
    return cakes_df["Nom-du-gâteau"].sample(n=min(n, len(cakes_df))).tolist()

@tool
def get_cakes_by_sugar_threshold(threshold:float) -> list[str] :
    """
    This function returns a list of cake names where the sugar content is below a specified threshold.  
    It filters the cakes based on the given sugar percentage and retrieves only those that meet the criteria.  
    The function takes a numerical parameter representing the maximum allowed sugar percentage.  
    If no cakes meet the condition, it returns an empty list.
    """
    return cakes_df[cakes_df["Taux-de-sucre-(%)"] <= threshold]["Nom-du-gâteau"].tolist()

@tool
def get_total_cakes_count() -> int :
    """
    This function returns the total number of available cakes.  
    It counts all unique cake names from the available data source.  
    The function takes no parameters and returns an integer representing the total number of cakes.  
    """
    return cakes_df["Nom-du-gâteau"].nunique()

tools = [get_cake_price, get_cake_sugar, get_cake_names, get_cakes_by_sugar_threshold,get_total_cakes_count]


system_prompt = SystemMessage("""
    You are a professional chatbot specializing in answering questions about the cakes sold by your company.
    To provide accurate responses, you will exclusively rely on the available tools and not your own memory.
    For small talk and greetings, you will maintain a professional and courteous tone in your replies..
    """
)

checkpointer=MemorySaver()

cake_QnA_agent=create_react_agent(
                                model=model,  
                                tools=tools,  
                                prompt=system_prompt,  
                                debug=False,  
                                checkpointer=checkpointer 
)



import uuid
 
config = {"configurable": {"thread_id": uuid.uuid4()}}
 
inputs = {"messages":[HumanMessage("Suggest five cakes with a sugar content below 40%. Your answer should include the five cakes along with their sugar content")]}
 

response = cake_QnA_agent.invoke(inputs, config)
print("Step by Step execution : ")
for message in response['messages']:
    print(message.pretty_repr())
 
 
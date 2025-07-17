from typing import Optional
from mcp.server.fastmcp import FastMCP
import pandas as pd
 

 


cakes_df = pd.read_csv("../Data/cakes_data.csv")

# MCP server
mcp = FastMCP(
    name="Cakes_information",
    host="0.0.0.0",  
    port=8010,  
    stateless_http=True,
)

@mcp.tool()
def get_cake_names(n:int) -> list[str] :
    """
    This function returns a list of available cake names, limited to a specified number.  
    It retrieves the names from the available data source.  
    The function takes an integer parameter representing the maximum number of cake names to return.  
    If the requested number exceeds the total available cakes, it returns all available names.
    """
    return cakes_df["Nom-du-gâteau"].sample(n=min(n, len(cakes_df))).tolist()


@mcp.tool()
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
    


@mcp.tool()
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
    


@mcp.tool()
def get_cakes_by_sugar_threshold(threshold:float) -> list[str] :
    """
    This function returns a list of cake names where the sugar content is below a specified threshold.  
    It filters the cakes based on the given sugar percentage and retrieves only those that meet the criteria.  
    The function takes a numerical parameter representing the maximum allowed sugar percentage.  
    If no cakes meet the condition, it returns an empty list.
    """
    return cakes_df[cakes_df["Taux-de-sucre-(%)"] <= threshold]["Nom-du-gâteau"].tolist()


@mcp.tool()
def get_total_cakes_count() -> int :
    """
    This function returns the total number of available cakes.  
    It counts all unique cake names from the available data source.  
    The function takes no parameters and returns an integer representing the total number of cakes.  
    """
    return cakes_df["Nom-du-gâteau"].nunique()



 
if __name__ == "__main__":
    transport = "streamable-http"
    if transport == "stdio":
        print("Running MCP server in your local machine")
        mcp.run(transport="stdio")
        
    elif transport == "sse":
        print("Running MCP server as a Server-Sent Event (SSE) server")
        mcp.run(transport="sse")

    elif transport == "streamable-http":
        print("Running MCP server : [Streamable HTTP transport]")
        mcp.run(transport="streamable-http")
    
    else:
        raise ValueError(f"Error transport mode: {transport}")

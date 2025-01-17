import os
import google.generativeai as genai
from serpapi.google_search import GoogleSearch
from dotenv import load_dotenv
from typing import Annotated, Dict, List, TypedDict
from langgraph.graph import Graph, StateGraph
import json

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv('gemini_api_key'))
serpapi_api_key = os.getenv('serpapi_api_key')

# Define state structure
class AgentState(TypedDict):
    messages: List[Dict] # Stores conversation history
    current_query: str # Current user input
    search_results: List[str] # Search results from SerpAPI
    final_response: str # Final response to user
    next_step: str # Controls workflow routing

# Initialize Gemini model
generation_config = {
    "temperature": 0.9,  # Controls randomness (1 = more creative)
    "top_p": 0.95, # Nucleus sampling parameter
    "top_k": 64, # Limits token selection
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def create_chat_session():
    return model.start_chat(history=[])

def parse_json_response(text: str) -> Dict:
    """Safely parse JSON from model response"""
    try:
        # Try to find JSON-like structure in the response
        start_idx = text.find('{')
        end_idx = text.rfind('}') + 1
        if start_idx != -1 and end_idx != 0:
            json_str = text[start_idx:end_idx]
            return json.loads(json_str)
    except:
        pass
    
    # Return default structure if parsing fails
    return {
        "needs_search": True,
        "reasoning": "Failed to parse response, defaulting to search"
    }

# Tool definitions
def search_tool(query: str) -> Dict[str, str]:
    """Web search tool using SerpApi"""
    try:
        search_params = {
            "q": query,
            "api_key": serpapi_api_key
        }
        search_results = GoogleSearch(search_params).get_dict()
        organic_results = search_results.get("organic_results", [])
        
        if not organic_results:
            return {"result": "[]"}
        
        snippets = [result.get("snippet", "") for result in organic_results[:2]]
        return {"result": json.dumps(snippets)}
    except Exception as e:
        print(f"Search error: {str(e)}")
        return {"result": "[]"}

def query_analyzer(state: AgentState) -> Dict:
    """Analyzes the query and determines if search is needed"""
    chat = create_chat_session()
    
    system_prompt = """You are an AI assistant that analyzes user queries to determine if web search is needed.
    You must respond in valid JSON format with exactly this structure:
    {
        "needs_search": boolean,
        "reasoning": "your reasoning here"
    }
    Consider a query needs search if it:
    - Asks about current events or news
    - Requires factual or statistical information
    - Mentions specific details that need verification
    - Asks about real-world entities or events
    
    Respond only with the JSON, no additional text."""
    
    user_prompt = f"Query to analyze: {state['current_query']}"
    
    # First message sets the context
    chat.send_message(system_prompt)
    # Second message gets the analysis
    response = chat.send_message(user_prompt)
    
    # Parse the response
    analysis = parse_json_response(response.text)
    
    # Update state
    state["messages"].append({
        "role": "system",
        "content": f"Analysis: {analysis['reasoning']}"
    })
    
    # Determine next step based on analysis
    state["next_step"] = "search" if analysis["needs_search"] else "respond"
    
    return state

def search_executor(state: AgentState) -> Dict:
    """Executes search if needed"""
    if state["next_step"] == "search":
        search_result = search_tool(state["current_query"])
        try:
            state["search_results"] = json.loads(search_result["result"])
        except json.JSONDecodeError:
            state["search_results"] = []
    
    state["next_step"] = "respond"
    return state

def response_generator(state: AgentState) -> Dict:
    """Generates final response using Gemini"""
    chat = create_chat_session()
    
    # Create system prompt for consistent responses
    system_prompt = """You are a helpful AI assistant. Use the provided information 
    (if any) to give a comprehensive but concise answer to the user's query. 
    If search results are provided, incorporate that information naturally into your response."""
    
    chat.send_message(system_prompt)
    
    if state["search_results"]:
        context = f"Based on search results: {state['search_results']}\n"
    else:
        context = "No search results available. Providing response based on my knowledge.\n"
    
    prompt = f"{context}User query: {state['current_query']}"
    response = chat.send_message(prompt)
    
    state["final_response"] = response.text
    return state

def should_search(state: AgentState) -> bool:
    """Conditional routing based on analysis"""
    return state["next_step"] == "search"

def create_agent_graph() -> Graph:
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("analyze", query_analyzer)
    workflow.add_node("search", search_executor)
    workflow.add_node("respond", response_generator)
    
    # Define conditional edges
    workflow.add_conditional_edges(
        "analyze",
        should_search,
        {
            True: "search",
            False: "respond"
        }
    )
    
    # Add edge from search to respond
    workflow.add_edge("search", "respond")
    
    # Set entry and exit points
    workflow.set_entry_point("analyze")
    workflow.set_finish_point("respond")
    
    return workflow.compile()

def main():
    # Initialize the graph
    agent_graph = create_agent_graph()
    
    print("Bot: Hello! I'm ready to help. You can ask me anything, and I'll search the web if needed.")
    print("(Type 'exit', 'quit', or 'bye' to end the conversation)\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Bot: Goodbye!")
            break
        
        # Initialize state
        state = AgentState(
            messages=[], 
            current_query=user_input,
            search_results=[],
            final_response="",
            next_step="analyze"
        )
        
        try:
            # Run the graph
            final_state = agent_graph.invoke(state)
            print(f"Bot: {final_state['final_response']}\n")
        except Exception as e:
            print(f"Bot: I encountered an error while processing your request. Let me try to provide a simple response.\n")
            # Fallback response using just the model
            chat = create_chat_session()
            response = chat.send_message(user_input)
            print(f"Bot: {response.text}\n")

if __name__ == "__main__":
    main()
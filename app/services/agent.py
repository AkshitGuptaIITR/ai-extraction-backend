from typing import List, Any
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_openai import ChatOpenAI
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from core.config import settings
from services.data import load_data
import pandas as pd
from typing import TypedDict, Annotated
import operator

# State Definition
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    dataframe_details: str

# Config & Setup
df = load_data()  # Load data at module level for now (or cache it)
# We might want to pass 'df' efficiently, but for local agent, memory is fine.

# Tools
# We will use PythonAstREPLTool to allow the agent to run pandas operations
python_tool = PythonAstREPLTool(locals={"df": df})

tools = [python_tool]

# LLM - DeepSeek
llm = ChatOpenAI(
    model="deepseek-chat", 
    api_key=settings.DEEPSEEK_API_KEY,
    base_url=settings.DEEPSEEK_BASE_URL
)
llm_with_tools = llm.bind_tools(tools)

# Nodes
def agent_node(state: AgentState):
    messages = state["messages"]
    
    # Add a system prompt context if it's the first message or we want to enforce it
    # Ideally, we prepend a system message about the dataset
    
    # We can inspect columns here to inject into prompt
    if "dataframe_details" not in state or not state["dataframe_details"]:
        columns = df.columns.tolist()
        columns_str = ", ".join(columns)
        # Inject context. For efficiency, we might just do this once.
        # But this node runs every step.
        pass

    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# Graph
workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)
workflow.add_node("tools", ToolNode(tools))

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    tools_condition,
)
workflow.add_edge("tools", "agent")

compiled_graph = workflow.compile()

from fastapi import APIRouter, HTTPException
from schemas.chat import ChatRequest, ChatResponse
from services.agent import workflow
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Compile the graph once at startup/module level if possible, 
# or ensure it's lightweight enough.
app = workflow.compile()

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Initialize state with the user message
        initial_state = {
            "messages": [("user", request.message)],
            "dataframe_details": "" # Can be populated if needed
        }
        
        # Invoke the agent
        result = app.invoke(initial_state)
        
        # Extract the last AI message
        messages = result["messages"]
        last_message = messages[-1]
        
        return ChatResponse(response=last_message.content)
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

"""
FastAPI Backend for AI Agent
Main application file with /ask endpoint
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import os
from dotenv import load_dotenv
import logging
from agent import AIAgent

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Agent API",
    description="An intelligent AI agent that combines LLM reasoning with external API tools",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API keys from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
USE_GROQ = os.getenv("USE_GROQ", "false").lower() == "true"
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# Determine which LLM to use
if USE_GROQ and GROQ_API_KEY:
    logger.info("🚀 Using Groq API (FREE and FAST!)")
    llm_key = GROQ_API_KEY
    use_groq = True
elif OPENAI_API_KEY:
    logger.info("Using OpenAI API")
    llm_key = OPENAI_API_KEY
    use_groq = False
else:
    logger.error("No LLM API key found! Set either OPENAI_API_KEY or GROQ_API_KEY")
    llm_key = None
    use_groq = False

# Validate API keys
if not llm_key:
    logger.error("LLM API key not found in environment variables")
if not OPENWEATHER_API_KEY:
    logger.warning("OPENWEATHER_API_KEY not found - weather queries will fail")
if not NEWS_API_KEY:
    logger.warning("NEWS_API_KEY not found - news queries will fail")

# Initialize AI Agent
try:
    agent = AIAgent(
        openai_api_key=llm_key or "",
        weather_api_key=OPENWEATHER_API_KEY or "",
        news_api_key=NEWS_API_KEY or "",
        use_groq=use_groq,
        groq_api_key=GROQ_API_KEY if use_groq else None
    )
    logger.info("AI Agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize AI Agent: {str(e)}")
    agent = None


# Request and Response models
class QueryRequest(BaseModel):
    """Request model for the /ask endpoint"""
    query: str = Field(..., description="User query to process", min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is the weather in Paris today?"
            }
        }


class QueryResponse(BaseModel):
    """Response model for the /ask endpoint"""
    reasoning: str = Field(..., description="Explanation of how the agent processed the query")
    answer: str = Field(..., description="Final answer to the user's query")
    tool_used: Optional[str] = Field(None, description="Name of the external tool used (if any)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "reasoning": "The user asked about weather, so I fetched data from OpenWeather API and combined it with reasoning from GPT.",
                "answer": "It's 21°C and partly cloudy in Paris today.",
                "tool_used": "weather"
            }
        }


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI Agent API - Backend Developer Assignment",
        "version": "1.0.0",
        "endpoints": {
            "/ask": "POST - Submit a query to the AI agent",
            "/docs": "GET - Interactive API documentation"
        }
    }


@app.post("/ask", response_model=QueryResponse)
async def ask(request: QueryRequest):
    """
    Main endpoint to process user queries
    
    The agent will:
    1. Analyze the query to determine if external tools are needed
    2. Fetch data from appropriate APIs (Weather, News) if required
    3. Use LLM to generate a coherent, natural response
    4. Return both the reasoning process and the final answer
    
    Args:
        request: QueryRequest object containing the user's query
        
    Returns:
        QueryResponse with reasoning, answer, and tool information
    """
    if agent is None:
        raise HTTPException(
            status_code=503, 
            detail="AI Agent not initialized. Please check API keys in .env file."
        )
    
    if not request.query or not request.query.strip():
        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty"
        )
    
    try:
        # Process the query using the AI agent
        logger.info(f"Received query: {request.query}")
        result = agent.process_query(request.query)
        
        response = QueryResponse(
            reasoning=result["reasoning"],
            answer=result["answer"],
            tool_used=result["tool_used"]
        )
        
        logger.info(f"Query processed successfully. Tool used: {result['tool_used']}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your query: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

"""
AI Agent with LLM Reasoning and Tool Integration
This module implements an intelligent agent that decides when to use external tools
vs. relying purely on LLM reasoning.
"""

from openai import OpenAI
import json
import logging
import os
from typing import Dict, List, Optional, Tuple
from tools import WeatherTool, NewsTool

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIAgent:
    """
    Intelligent AI Agent that combines LLM reasoning with external API tools
    Supports both OpenAI and Groq APIs
    """
    
    def __init__(self, openai_api_key: str, weather_api_key: str, news_api_key: str, use_groq: bool = False, groq_api_key: str = None):
        """
        Initialize the AI Agent with API keys
        
        Args:
            openai_api_key: OpenAI API key
            weather_api_key: OpenWeatherMap API key
            news_api_key: News API key
            use_groq: Whether to use Groq instead of OpenAI
            groq_api_key: Groq API key (if using Groq)
        """
        self.use_groq = use_groq
        
        if use_groq and groq_api_key:
            # Use Groq API (FREE!)
            self.openai_client = OpenAI(
                api_key=groq_api_key,
                base_url="https://api.groq.com/openai/v1"
            )
            self.model = "llama-3.1-8b-instant"  # Fast and free Groq model (updated)
            logger.info("Using Groq API (FREE)")
        else:
            # Use OpenAI API
            self.openai_client = OpenAI(api_key=openai_api_key)
            self.model = "gpt-3.5-turbo"
            logger.info("Using OpenAI API")
        self.weather_tool = WeatherTool(weather_api_key)
        self.news_tool = NewsTool(news_api_key)
        
        # Short-term memory to store recent conversations
        self.memory: List[Dict] = []
        self.max_memory_size = 5
        
    def add_to_memory(self, query: str, response: Dict):
        """
        Add a query-response pair to short-term memory
        
        Args:
            query: User query
            response: Agent response
        """
        self.memory.append({
            "query": query,
            "response": response
        })
        
        # Keep only the last N interactions
        if len(self.memory) > self.max_memory_size:
            self.memory.pop(0)
        
        logger.info(f"Added to memory. Current memory size: {len(self.memory)}")
    
    def get_memory_context(self) -> str:
        """
        Get formatted memory context for the LLM
        
        Returns:
            Formatted string with recent conversation history
        """
        if not self.memory:
            return ""
        
        context = "\n\nRecent conversation history:\n"
        for i, item in enumerate(self.memory[-3:], 1):  # Last 3 interactions
            context += f"{i}. User: {item['query']}\n"
            context += f"   Assistant: {item['response']['answer'][:100]}...\n"
        
        return context
    
    def classify_query(self, query: str) -> Tuple[str, Optional[str]]:
        """
        Use LLM to classify the query and determine which tool to use
        
        Args:
            query: User query
            
        Returns:
            Tuple of (tool_name, extracted_parameter)
            tool_name can be: 'weather', 'news', or 'llm_only'
        """
        classification_prompt = f"""You are an AI assistant that classifies user queries to determine which tool to use.

Analyze the following query and determine which tool is most appropriate:
- "weather" if the query asks about current weather, temperature, or weather conditions
- "news" if the query asks about recent news, current events, or latest information about a topic
- "llm_only" if the query is conversational, opinion-based, asks for facts/knowledge, or doesn't need external data

Query: "{query}"

Respond in JSON format:
{{
    "tool": "tool_name",
    "parameter": "extracted parameter (city name, topic, search term, etc.)",
    "reasoning": "brief explanation of why this tool was chosen"
}}"""

        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a precise query classifier. Always respond with valid JSON."},
                    {"role": "user", "content": classification_prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            result = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                classification = json.loads(result)
                tool_name = classification.get("tool", "llm_only")
                parameter = classification.get("parameter", None)
                reasoning = classification.get("reasoning", "")
                
                logger.info(f"Query classified as: {tool_name}, Parameter: {parameter}, Reasoning: {reasoning}")
                return tool_name, parameter
                
            except json.JSONDecodeError:
                logger.warning("Failed to parse classification JSON, defaulting to llm_only")
                return "llm_only", None
                
        except Exception as e:
            logger.error(f"Error in query classification: {str(e)}")
            return "llm_only", None
    
    def use_weather_tool(self, city: str) -> Optional[Dict]:
        """Fetch weather information for a city"""
        return self.weather_tool.get_weather(city)
    
    def use_news_tool(self, topic: str) -> Optional[Dict]:
        """Fetch recent news about a topic"""
        return self.news_tool.get_news(topic)
    
    def generate_final_answer(self, query: str, tool_data: Optional[Dict], tool_name: str) -> Dict:
        """
        Use LLM to generate a coherent final answer combining tool data and reasoning
        
        Args:
            query: Original user query
            tool_data: Data fetched from external tool (if any)
            tool_name: Name of the tool used
            
        Returns:
            Dictionary with reasoning and answer
        """
        memory_context = self.get_memory_context()
        
        if tool_data:
            # Combine tool data with LLM reasoning
            prompt = f"""You are a helpful AI assistant. The user asked: "{query}"

I fetched the following information using the {tool_name} tool:
{json.dumps(tool_data, indent=2)}

Based on this data, provide a natural, conversational answer to the user's question. 
Be concise but informative. Don't just repeat the data - synthesize it into a helpful response.{memory_context}"""
            
            reasoning = f"The user asked about {tool_name}-related information, so I fetched data from the {tool_name.upper()} API and combined it with my reasoning to form a comprehensive answer."
            
        else:
            # LLM-only response
            prompt = f"""You are a helpful AI assistant. Answer the following question naturally and conversationally:

Question: "{query}"{memory_context}

Provide a clear, accurate, and helpful response."""
            
            reasoning = "This query can be answered using my general knowledge without needing external tools."
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful, knowledgeable AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content.strip()
            
            return {
                "reasoning": reasoning,
                "answer": answer,
                "tool_used": tool_name,
                "raw_data": tool_data if tool_data else None
            }
            
        except Exception as e:
            logger.error(f"Error generating final answer: {str(e)}", exc_info=True)
            # Log the full exception for debugging
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return {
                "reasoning": "An error occurred while generating the response.",
                "answer": f"I apologize, but I encountered an error while processing your request. Error: {str(e)}",
                "tool_used": tool_name,
                "raw_data": None
            }
    
    def process_query(self, query: str) -> Dict:
        """
        Main method to process a user query
        
        Args:
            query: User query string
            
        Returns:
            Dictionary with reasoning and answer
        """
        logger.info(f"Processing query: {query}")
        
        # Step 1: Classify the query to determine which tool to use
        tool_name, parameter = self.classify_query(query)
        
        # Step 2: Call the appropriate tool if needed
        tool_data = None
        
        if tool_name == "weather" and parameter:
            tool_data = self.use_weather_tool(parameter)
            if not tool_data:
                logger.warning(f"Weather tool failed for city: {parameter}")
        
        elif tool_name == "news" and parameter:
            tool_data = self.use_news_tool(parameter)
            if not tool_data:
                logger.warning(f"News tool failed for topic: {parameter}")
        
        # Step 3: Generate final answer using LLM
        result = self.generate_final_answer(query, tool_data, tool_name)
        
        # Step 4: Add to memory
        self.add_to_memory(query, result)
        
        return result

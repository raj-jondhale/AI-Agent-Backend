# AI Agent - Backend Developer Assignment

An intelligent backend service that combines LLM reasoning (Groq/OpenAI) with external API tools (Weather, Wikipedia, News) to create a sophisticated AI agent that can think, decide, and act.

## 🎯 Project Overview

This FastAPI backend implements an AI agent that:

- **Intelligently decides** when to use external APIs vs. pure LLM reasoning
- **Supports multiple LLM providers**: Groq (FREE, recommended) or OpenAI
- **Integrates multiple tools**: Weather (OpenWeatherMap), Wikipedia, and News API
- **Maintains short-term memory** of recent conversations
- **Provides detailed reasoning** for every response
- **Handles errors gracefully** with comprehensive logging

## 🏗️ Architecture

```
┌─────────────┐
│   User      │
│   Query     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│        FastAPI Endpoint             │
│          POST /ask                  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│         AI Agent (agent.py)         │
│  ┌───────────────────────────────┐  │
│  │  1. Query Classification      │  │
│  │     (using Groq/OpenAI)      │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│              ▼                       │
│  ┌───────────────────────────────┐  │
│  │  2. Tool Selection            │  │
│  │     - Weather                 │  │
│  │     - Wikipedia               │  │
│  │     - News                    │  │
│  │     - LLM Only                │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│              ▼                       │
│  ┌───────────────────────────────┐  │
│  │  3. Data Fetching             │  │
│  │     (if tool needed)          │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│              ▼                       │
│  ┌───────────────────────────────┐  │
│  │  4. Answer Generation         │  │
│  │     (GPT combines data)       │  │
│  └───────────┬───────────────────┘  │
│              │                       │
│              ▼                       │
│  ┌───────────────────────────────┐  │
│  │  5. Memory Storage            │  │
│  └───────────────────────────────┘  │
└─────────────┬───────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│         JSON Response               │
│  - reasoning                        │
│  - answer                           │
│  - tool_used                        │
└─────────────────────────────────────┘
```

## 📋 Features

✅ **POST /ask endpoint** - Main query processing endpoint
✅ **Intelligent tool selection** - LLM-based classification of queries
✅ **Multi-tool integration**:

- 🌤️ Weather API (OpenWeatherMap)
- 📚 Wikipedia API
- 📰 News API

✅ **LLM reasoning** - Groq (FREE) or OpenAI GPT-3.5/GPT-4 integration
✅ **Detailed reasoning** - Explanations of decision-making process
✅ **Short-term memory** - Remembers last 5 conversations for context
✅ **Error handling** - Comprehensive try-catch blocks and fallbacks
✅ **Logging** - Detailed logging of all operations
✅ **Interactive docs** - Auto-generated Swagger UI

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- API Keys:
  - **Groq API Key (Recommended - FREE!)** OR OpenAI API Key
  - OpenWeatherMap API Key (Optional but recommended)
  - News API Key (Optional but recommended)

### Installation

1. **Clone or download this repository**

2. **Navigate to the project directory**

```powershell
cd "c:\Users\Rajesh Jondhale\OneDrive\Desktop\Assignment"
```

3. **Create a virtual environment** (recommended)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

4. **Install dependencies**

```powershell
pip install -r requirements.txt
```

5. **Set up environment variables**

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and add your API keys:

```env
# Option 1: Use Groq (FREE - Recommended!)
GROQ_API_KEY=your_groq_api_key_here
USE_GROQ=true

# Option 2: Use OpenAI (Requires credits)
# OPENAI_API_KEY=your_openai_api_key_here

# External APIs (Optional but recommended)
OPENWEATHER_API_KEY=your_openweather_api_key_here
NEWS_API_KEY=your_news_api_key_here
```

**Where to get API keys:**

- **Groq (FREE!)**: https://console.groq.com/keys
- **OpenAI**: https://platform.openai.com/api-keys
- **OpenWeatherMap**: https://openweathermap.org/api
- **News API**: https://newsapi.org/register

### Running the Application

Start the server:

```powershell
python main.py
```

Or using uvicorn directly:

```powershell
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

## 📖 API Documentation

### Endpoints

#### 1. **POST /ask** - Main Query Endpoint

Submit a query to the AI agent.

**Request:**

```json
{
  "query": "What is the weather in Paris today?"
}
```

**Response:**

```json
{
  "reasoning": "The user asked about weather, so I fetched data from OpenWeather API and combined it with reasoning from GPT.",
  "answer": "It's 21°C and partly cloudy in Paris today. The humidity is at 65% with a gentle breeze of 3.5 m/s.",
  "tool_used": "weather"
}
```

#### 2. **GET /** - API Information

Get basic API information and available endpoints.

### Interactive Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

### Using the Test Script

A test script is provided to test all example queries:

```powershell
python test_api.py
```

### Manual Testing with cURL

```powershell
# Weather query
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d '{\"query\": \"What is the weather in London today?\"}'

# Wikipedia query
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d '{\"query\": \"Who invented the telephone?\"}'

# News query
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d '{\"query\": \"Latest news about artificial intelligence\"}'

# General knowledge query
curl -X POST "http://localhost:8000/ask" -H "Content-Type: application/json" -d '{\"query\": \"What is the capital of Japan?\"}'
```

### Test Queries

The following queries demonstrate different agent capabilities:

1. **Weather Queries**

   - "What's the weather in London today?"
   - "Is it raining in Tokyo?"
   - "Temperature in New York?"

2. **Wikipedia/Knowledge Queries**

   - "Who invented the telephone?"
   - "What is the capital of Japan?"
   - "Tell me about Albert Einstein"

3. **News Queries**

   - "Summarize the latest news about artificial intelligence"
   - "Recent news about climate change"
   - "What's happening with SpaceX?"

4. **General Queries (LLM Only)**
   - "What are the benefits of meditation?"
   - "Explain quantum computing in simple terms"
   - "How does photosynthesis work?"

## 🛠️ APIs Used

### 1. **Groq LLM API (Recommended - FREE!)**

**Purpose**: LLM reasoning, query classification, and answer generation

**Why chosen**:

- **Completely FREE** with generous rate limits (14,400 requests/day)
- **Very fast** - faster than OpenAI
- State-of-the-art Llama 3.1 model
- OpenAI-compatible API format
- No credit card required

**Usage in project**:

- Classifying user queries to determine tool usage
- Generating natural, conversational responses
- Combining external data with reasoning

**Alternative**: OpenAI GPT-3.5-turbo (requires paid credits)

### 2. **OpenWeatherMap API**

**Purpose**: Real-time weather data

**Why chosen**:

- Free tier available
- Comprehensive weather data
- Reliable and well-documented API

**Data retrieved**:

- Current temperature (Celsius)
- Weather description
- Humidity, wind speed
- "Feels like" temperature

### 3. **Wikipedia API**

**Purpose**: Factual information and general knowledge

**Why chosen**:

- Free and open
- Comprehensive knowledge base
- Multiple access methods (wikipedia-api library + REST API fallback)

**Data retrieved**:

- Article summaries
- Page titles and URLs
- Quick facts and definitions

### 4. **News API**

**Purpose**: Recent news articles and current events

**Why chosen**:

- Up-to-date news coverage
- Multiple sources
- Good search and filtering capabilities

**Data retrieved**:

- Recent articles (last 3)
- Headlines and descriptions
- Publication dates and sources

## 🧠 How It Works

### Decision-Making Process

1. **Query Reception**: User query arrives at `/ask` endpoint

2. **Intelligent Classification**:

   - Agent uses LLM (Groq/OpenAI) to analyze the query
   - Determines intent and required tools
   - Extracts relevant parameters (city names, topics, etc.)

3. **Tool Selection Logic**:

   ```python
   if "weather" related → Use OpenWeatherMap API
   elif "facts/knowledge" → Use Wikipedia API
   elif "news/recent events" → Use News API
   else → Use LLM reasoning only
   ```

4. **Data Fetching**:

   - If tool needed: Fetch data from external API
   - Implement fallbacks for API failures
   - Log all operations

5. **Answer Generation**:

   - Combine external data with LLM reasoning
   - Generate natural, conversational response
   - Include reasoning explanation

6. **Memory Storage**:
   - Store query-response pair
   - Maintain rolling window of last 5 conversations
   - Use in future queries for context

### Example Flow

**Query**: "What's the weather in Paris today?"

```
1. Classification → Tool: "weather", Parameter: "Paris"
2. API Call → OpenWeatherMap API for Paris
3. Data Retrieved → 21°C, partly cloudy, 65% humidity
4. LLM Processing → Combines data into natural answer
5. Response → "It's 21°C and partly cloudy in Paris today..."
6. Memory → Stores conversation for context
```

## 📁 Project Structure

```
Assignment/
│
├── main.py              # FastAPI application and endpoints
├── agent.py             # AI Agent with decision logic
├── tools.py             # External API integrations
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .env                 # Your API keys (not in git)
├── .gitignore          # Git ignore file
├── test_api.py         # Test script
└── README.md           # This file
```

## 🔒 Security Notes

- Never commit `.env` file with real API keys
- Use environment variables for all sensitive data
- API keys are loaded at runtime from `.env`
- CORS is enabled for development (configure for production)

## 🐛 Error Handling

The application includes comprehensive error handling:

- **API failures**: Fallback to alternative methods or graceful degradation
- **Invalid queries**: Returns helpful error messages
- **Missing API keys**: Warns but allows other tools to work
- **Network issues**: Timeout protection and retry logic
- **JSON parsing errors**: Fallback to default behavior

All errors are logged with detailed information for debugging.

## � Troubleshooting

### "Error 429 - Quota exceeded"

**Problem**: OpenAI API quota depleted  
**Solution**: Switch to Groq (FREE)

```env
GROQ_API_KEY=your_groq_key_here
USE_GROQ=true
```

### "Model decommissioned error"

**Status**: ✅ Already fixed!  
The project uses `llama-3.1-8b-instant` (current Groq model)

### "Module not found" errors

**Solution**: Activate virtual environment and install dependencies

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### All queries return errors

**Solution**: Check `.env` file has valid API keys and restart the server

```powershell
# Check if keys are set
cat .env

# Restart server
python main.py
```

## 🎓 Learning Outcomes

This project demonstrates:

- FastAPI backend development
- LLM integration and prompt engineering
- External API integration
- Intelligent decision-making systems
- Error handling and logging
- RESTful API design
- Documentation best practices

## 📝 Future Enhancements

Possible improvements:

- Add more external tools (Calculator, Database, etc.)
- Implement user authentication
- Add caching for API responses
- Implement rate limiting
- Add support for multiple languages
- Create a web frontend
- Add voice input/output (Whisper + ElevenLabs)
- Use LangChain for better orchestration
- Add database for persistent memory
- Implement streaming responses

## 👨‍💻 Author

**Rajesh Jondhale**

- Assignment: Backend Developer Position
- Date: November 2025

## 📄 License

This is an educational project created as part of a technical assignment.

---

## 🚀 Why Groq?

This project uses **Groq** as the recommended LLM provider because:

- ✅ **100% FREE** - No credit card required
- ✅ **Faster responses** - Better performance than OpenAI
- ✅ **14,400 requests/day** - Generous free tier
- ✅ **Same functionality** - OpenAI-compatible API
- ✅ **Great quality** - Llama 3.1 model

Get your FREE Groq API key at: https://console.groq.com/keys

---

**Questions or Issues?**
Please feel free to reach out if you have any questions about the implementation!

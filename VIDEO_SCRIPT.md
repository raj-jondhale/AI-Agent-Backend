# 🎥 Video Demo Script for AI Agent Project

## Duration: 2-3 minutes

---

## 🎬 OPENING (15 seconds)

**[Show your face or screen]**

> "Hi! I'm Rajesh Jondhale, and this is my submission for the Backend Developer assignment. I've built an intelligent AI Agent that combines LLM reasoning with external API tools using FastAPI. Let me walk you through how it works."

**[Action: Open VS Code with project folder visible]**

---

## 📂 PART 1: Project Overview (20 seconds)

**[Show project structure in VS Code]**

> "The project is organized into three main modules:
>
> - **main.py** handles the FastAPI endpoints
> - **agent.py** contains the intelligent decision-making logic
> - **tools.py** integrates Weather, Wikipedia, and News APIs
>
> I've also implemented short-term memory and comprehensive error handling."

**[Action: Quickly scroll through the three files]**

---

## 🧠 PART 2: Key Feature - Intelligent Routing (30 seconds)

**[Open agent.py, show classify_query method]**

> "The most important feature is the intelligent routing system. When a user sends a query, the agent uses Groq's LLM to classify it and decide which tool to use.
>
> For example:
>
> - Weather-related queries go to OpenWeatherMap
> - Factual questions go to Wikipedia
> - News queries go to News API
> - General questions are answered directly by the LLM
>
> This isn't random - it's based on intelligent analysis of the user's intent."

**[Action: Highlight the classify_query function, then show tool selection logic]**

---

## 🚀 PART 3: Live Demo (60 seconds)

**[Split screen or switch to browser]**

> "Let me show you how it works in action. I've started the server, and I'll use the interactive Swagger documentation."

**[Action: Open http://localhost:8000/docs]**

---

### Demo Query 1: Weather

**[Click on POST /ask endpoint, click "Try it out"]**

> "First, let's ask about the weather in London."

**[Action: Type in request body]**

```json
{
  "query": "What's the weather in London today?"
}
```

**[Click Execute, show response]**

> "As you can see, it correctly identified this as a weather query, fetched data from OpenWeatherMap API, and combined it with the LLM's reasoning to give a natural answer."

**[Action: Point to the reasoning, answer, and tool_used fields]**

---

### Demo Query 2: Knowledge/Wikipedia

**[Still in Swagger UI]**

> "Now let's try a factual question."

**[Action: Type in request body]**

```json
{
  "query": "Who invented the telephone?"
}
```

**[Click Execute, show response]**

> "Perfect! It used Wikipedia to fetch accurate information and presented it in a conversational way."

---

### Demo Query 3: General Knowledge (LLM Only)

**[Still in Swagger UI]**

> "And for general questions that don't need external data..."

**[Action: Type in request body]**

```json
{
  "query": "What are the benefits of exercise?"
}
```

**[Click Execute, show response]**

> "The agent recognized this doesn't need an API call and answered directly using the LLM's knowledge."

---

## 💡 PART 4: Why These Choices? (20 seconds)

**[Switch back to VS Code or stay in browser]**

> "I chose to use Groq instead of OpenAI because it's completely free with excellent performance. It uses the Llama 3.1 model and provides 14,400 requests per day on the free tier - perfect for this assignment.
>
> For external APIs, I integrated OpenWeatherMap for real-time weather, Wikipedia for factual knowledge, and News API for current events. Each serves a distinct purpose in making the agent more capable."

**[Action: Optionally show .env file with API keys (hide the actual keys)]**

---

## 🎯 PART 5: Architecture Highlight (15 seconds)

**[Show the architecture diagram in README.md or draw it quickly]**

> "The flow is simple but powerful: Query comes in → Agent classifies it → Selects appropriate tool → Fetches data → LLM generates natural answer → Stores in memory for context.
>
> This demonstrates not just API integration, but intelligent decision-making and context awareness."

---

## 🎓 CLOSING (10 seconds)

**[Back to your face or final screen]**

> "The complete code is on GitHub with detailed documentation, setup instructions, and test scripts. Everything is working perfectly with the free Groq API. Thank you for reviewing my submission, and I'm happy to discuss any part of the implementation!"

**[Action: Show GitHub repo briefly or README.md]**

---

## 📋 CHECKLIST BEFORE RECORDING

- [ ] Server is running (`python main.py`)
- [ ] Browser is open to http://localhost:8000/docs
- [ ] VS Code is open with project files
- [ ] .env file has valid API keys
- [ ] Test queries work (test them once before recording)
- [ ] Close unnecessary tabs/applications
- [ ] Clear desktop clutter
- [ ] Audio is working clearly

---

## 🎬 RECORDING TIPS

### Setup

1. **Screen Resolution**: Use 1920x1080 or 1280x720
2. **Browser Zoom**: Set to 100% or 110% for visibility
3. **VS Code Font**: Increase font size (14-16pt)
4. **Microphone**: Test audio, speak clearly and enthusiastically

### During Recording

1. **Pace**: Speak at moderate speed, not too fast
2. **Cursor**: Move deliberately to highlight what you're discussing
3. **Pauses**: Brief pause between sections
4. **Energy**: Show enthusiasm about your work!

### What to Emphasize

- ⭐ **Intelligent routing** - Not random, actual AI decision-making
- ⭐ **Working demo** - Show actual responses, not just code
- ⭐ **Multi-tool integration** - Weather, Wikipedia, News
- ⭐ **Free solution** - Groq makes it accessible

---

## 🎯 ALTERNATIVE: 90-SECOND QUICK VERSION

If you want a shorter video:

### Quick Script (90 seconds)

**[15s] Introduction:**

> "Hi, I'm Rajesh. I built an AI Agent that intelligently routes queries to different APIs based on context."

**[30s] Quick Code Tour:**

> "The agent classifies queries, selects the right tool from Weather, Wikipedia, or News APIs, and generates natural responses."

**[30s] Live Demo:**

> "Here's a weather query... [Execute] ...fetched from OpenWeatherMap. Here's a factual question... [Execute] ...pulled from Wikipedia. And general questions are answered directly by the LLM."

**[15s] Closing:**

> "I used Groq's free API for the LLM, and everything is documented on GitHub. Thank you!"

---

## 📝 BACKUP QUERIES (If Something Fails)

Have these ready:

1. "What is 10 + 10?" (Simple, always works)
2. "What is the capital of France?" (Wikipedia, reliable)
3. "Tell me about Python programming" (LLM only)

---

## 🎥 FINAL TIPS

1. **Practice once** before final recording
2. **Don't apologize** for anything - be confident!
3. **If you make a mistake**: Just pause, breathe, and continue
4. **Smile** (if showing face) - show you're passionate about the work
5. **Keep it under 3 minutes** - be concise but thorough
6. **End with energy** - leave a good impression

---

## 🔗 After Recording

1. Upload to Loom
2. Set to "Anyone with link can view"
3. Copy the share link
4. Add to README.md under "Video Explanation"
5. Test the link in incognito mode
6. Submit with GitHub repo link

---

**You've got this! Your project is working great - just show it off with confidence!** 🚀

Good luck with your recording! 🎬

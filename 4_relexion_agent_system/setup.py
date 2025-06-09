# llm_setup.py

from dotenv import load_dotenv
load_dotenv()  # ✅ Load environment variables early

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# ✅ LLM instance (Gemini)
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")

# ✅ Tavily search tool (will use TAVILY_API_KEY from .env)
tavily_tool = TavilySearchResults(max_results=5)

# LangGraph Project

A comprehensive collection of LangChain and LangGraph implementations showcasing various AI agent architectures and patterns.

## 🚀 Overview

This project demonstrates different implementations of AI agents using LangChain and LangGraph, ranging from basic reflection systems to complex RAG (Retrieval-Augmented Generation) agents. Each implementation is organized in its own directory, providing a progressive learning path from simple to advanced concepts.

## 📁 Project Structure

The project is organized into several modules, each focusing on different aspects of AI agent development:

1. `1_Introduction/` - Basic concepts and setup
2. `2_basic_reflection_system/` - Simple reflection-based agents
3. `3_structured_outputs/` - Working with structured data
4. `4_relexion_agent_system/` - Advanced reflection systems
5. `5_state_dive/` - State management in agents
6. `6_react_agent/` - ReAct pattern implementations
7. `7_Chatbot/` - Chatbot implementations
8. `8_human-in-the-loop/` - Interactive agent systems
9. `9_RAG_agent/` - Retrieval-Augmented Generation agents

## 🛠️ Prerequisites

- Python 3.8+
- pip (Python package manager)

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/rkuma18/LangChain.git
cd LangChain
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
```

## 📚 Dependencies

- langchain - Core LangChain functionality
- langchain-community - Community-maintained LangChain integrations
- langchain-google-genai - Google AI model integrations
- langchain-openai - OpenAI model integrations
- langchain_groq - Groq model integrations
- langgraph - Graph-based agent orchestration
- python-dotenv - Environment variable management
- pydantic - Data validation
- chromadb - Vector database for RAG implementations
- langgraph-checkpoint-sqlite - State persistence

## 🔧 Usage

Each module contains its own implementation and can be run independently. Navigate to the specific module directory and follow the instructions in its README file.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Security

- Never commit your `.env` file or expose API keys
- Use environment variables for sensitive information
- Follow security best practices when deploying agents

## 📫 Contact

For questions or support, please open an issue in the GitHub repository.

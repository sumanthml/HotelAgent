# 🏨 HotelGuest: Advanced Multi-Agent Intelligence Engine
> **Autonomous Travel Discovery & Market Analytics Platform**

[![Live App](https://img.shields.io/badge/LIVE_DEMO-Launch_Application-brightgreen?style=for-the-badge&logo=streamlit)](https://hotelguest.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-LangGraph-orange?style=for-the-badge)](https://github.com/langchain-ai/langgraph)
[![Model](https://img.shields.io/badge/LLM-Gemini_1.5_Flash-red?style=for-the-badge&logo=google-gemini)](https://ai.google.dev/)

---

## 🚀 Experience the Future of Travel
### 🔗 **[ACCESS HOTELGUEST PRODUCTION ENVIRONMENT](https://hotelguest.streamlit.app/)**
*Precision research. Zero friction. Curated intelligence.*

---

## 📖 Overview
**HotelGuest** is an industrial-grade travel research agent that replaces traditional manual searching with **Autonomous Multi-Agent Orchestration**. Built on top of Google's Gemini 1.5 Flash and the LangGraph framework, it executes a complex, cyclic workflow to retrieve, filter, and rank global hotel data in real-time.

While traditional platforms show you thousands of sponsored results, **HotelGuest** acts as a digital concierge, utilizing a "State Machine" to ensure every recommendation is mathematically and contextually aligned with your specific requirements.

---

## 🏗️ System Architecture & Logic Flow
The core of HotelGuest is a **Directed Acyclic Graph (DAG)** that manages the lifecycle of a search request.

### 🧩 The Agentic Nodes
1. **The Architect (Requirements Processor):** - Uses NLP to transform vague human desires into structured JSON payloads.
   - **Logic:** Identifies intent, extracts budget caps, and synthesizes optimized search queries.
2. **The Researcher (Live Hotel Searcher):** - Interfaces directly with the **SerpApi Google Hotels Engine**.
   - **Logic:** Handles dynamic date injection and geo-location targeting.
3. **The Analyst (Expert Reviewer):** - Performs a "Deep Scan" of the top 10 results.
   - **Logic:** Filters by budget, analyzes amenities, and selects the **Top 5 Properties** based on a value-density algorithm.

### 🔄 State Management
The system utilizes a `TypedDict` state to maintain "Memory" across nodes:
- `hotels`: An annotated list that accumulates data.
- `loop_count`: A safety mechanism to prevent infinite API calls.
- `max_budget`: A persistent constraint that guides the Analyst node.

---

## 🛠️ Technical Deep Dive

### 🔐 Security & Operations
- **Secret Masking:** Utilizes Streamlit TOML secrets for secure API key injection (Environment Isolation).
- **Concurrency:** Built to handle high-concurrency requests using FastAPI-style logic within the Streamlit lifecycle.

### 📊 Performance Analytics
| Feature | Implementation | Benefit |
| :--- | :--- | :--- |
| **Search Engine** | Google Hotels via SerpApi | Access to 100% live inventory. |
| **Decision Engine** | LangGraph State Machine | Deterministic, reliable AI behavior. |
| **Language Model** | Gemini 1.5 Flash | Sub-second inference latency for real-time chat. |

---

## 💻 Developer Guide (Local Deployment)

### Prerequisites
- Python 3.11 or higher
- Google Gemini API Key
- SerpApi Key

### Installation
```bash
# Clone the repository
git clone [https://github.com/sumanthml/HotelAgent.git](https://github.com/sumanthml/HotelAgent.git)

# Navigate to directory
cd HotelAgent

# Install dependencies (Optimized)
pip install streamlit langgraph langchain-google-genai google-search-results python-dotenv

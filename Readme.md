# LATOKEN Bot Project
@Ahsan_latoken_bot
- Need openai key to work Ragsystem
## Overview
This project implements a Telegram bot for LATOKEN, enabling users to interact with the LATOKEN platform's principles, vision, and hackathon information. The bot supports:

1. **Answering questions** about LATOKEN, its culture, and its hackathon.
2. **Administering tests** to assess user understanding of LATOKEN's principles and vision.

The bot leverages a Retrieval-Augmented Generation (RAG) system for intelligent query processing and response generation, powered by OpenAI's GPT and FAISS for efficient vector search.

---

## Features

### 1. Ask a Question
- Users can ask questions about LATOKEN.
- The bot retrieves relevant data from the provided dataset (`latoken_data.json`) and generates a response using OpenAI's GPT model.

### 2. Take a Test
- Users can test their understanding by answering questions about LATOKEN's principles and goals.
- Follow-up questions are presented based on the RAG system's suggestions.

---

## File Descriptions

### `bot.py`
- Main script for the Telegram bot.
- Features:
  - Handles commands like `/start` and `/reset`.
  - Provides menu options to ask questions or take tests.
  - Uses the RAG system for intelligent interactions.

### `rag.py`
- Implements the RAG system:
  - Utilizes SentenceTransformers to create embeddings.
  - Uses FAISS for fast vector-based search.
  - Integrates OpenAI's GPT model for generating context-aware responses.

### `requirements.txt`
- Specifies the dependencies required for the project:
  - `python-telegram-bot`: For building and managing the Telegram bot.
  - `openai`: To integrate GPT for response generation.
  - `faiss-cpu`: To perform fast and efficient vector searches.
  - `sentence-transformers`: For creating text embeddings.
  - `numpy`: To handle numerical operations.

### `latoken_data.json`
- A dataset containing LATOKEN-related information:
  - LATOKEN principles and vision.
  - Hackathon details.
  - Cultural and operational insights.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/latoken-bot.git
   cd latoken-bot
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   - Replace the placeholders in `bot.py` with your actual API keys:
     - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
     - `OPENAI_API_KEY`: Your OpenAI API key.

4. **Run the Bot**:
   ```bash
   python bot.py
   ```

---

## Dataset Information
The `latoken_data.json` file contains:
- Hackathon-related information.
- LATOKEN's cultural and operational principles.

The data is used by the RAG system to generate accurate and context-aware responses.

---
- FAISS: Efficiently retrieves relevant data by searching dense embeddings of the text data.
- SentenceTransformer: Generates dense vector embeddings for both the query and the dataset.
- OpenAI GPT: Generates human-like responses using retrieved data as context.


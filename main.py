from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
import logging
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# Replace with your Telegram bot token
TELEGRAM_BOT_TOKEN = "8085545311:AAGF8Ozao7crfEtwk0ep6ikQhf61vlyGmag"

# Replace with your OpenAI API key
OPENAI_API_KEY = "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"

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load a pre-trained sentence transformer model for embeddings
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Load your data (replace this with your actual data)
data = [
    {"text": "LATOKEN is a cryptocurrency exchange that helps people trade digital assets securely.", "source": "LATOKEN Website"},
    {"text": "The LATOKEN Hackathon is an event where developers build innovative projects.", "source": "Hackathon Page"},
    {"text": "The Sugar Cookie Test is a concept from the LATOKEN Culture Deck.", "source": "Culture Deck"},
    # Add more data here
]

# Generate embeddings for your data
data_texts = [item["text"] for item in data]
data_embeddings = embedding_model.encode(data_texts)

# Build a FAISS index for efficient similarity search
dimension = data_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(data_embeddings)

# Define a function to retrieve relevant data
def retrieve_relevant_data(query, top_k=3):
    query_embedding = embedding_model.encode([query])
    distances, indices = index.search(query_embedding, top_k)
    relevant_data = [data[i] for i in indices[0]]
    return relevant_data

# Define a function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I'm the LATOKEN bot. Ask me anything about LATOKEN, the Hackathon, or the Culture Deck!"
    )

# Define a function to handle user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.from_user.id
    logger.info(f"User {user_id} asked: {user_message}")

    # Retrieve relevant data
    relevant_data = retrieve_relevant_data(user_message)
    context_text = "\n".join([item["text"] for item in relevant_data])

    # Use OpenAI to generate a response based on the retrieved data
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions about LATOKEN, the Hackathon, and the Culture Deck."},
                {"role": "user", "content": f"Context:\n{context_text}\n\nQuestion: {user_message}"}
            ]
        )
        bot_response = response.choices[0].message.content
        await update.message.reply_text(bot_response)
    except Exception as e:
        await update.message.reply_text(f"Sorry, I encountered an error: {str(e)}")

# Set up the bot
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# Add handlers for commands and messages
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Run the bot
print("Bot is running...")
app.run_polling()
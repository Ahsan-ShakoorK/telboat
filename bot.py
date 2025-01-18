import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ContextTypes, CallbackContext
)
import logging
from rag import RAGSystem
import json

# Define conversation states
ASKING_QUESTION = 1
TAKING_TEST = 2

# Load tokens from environment variables
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Check if tokens are set
if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Telegram bot token or OpenAI API key is missing!")

# Load your dataset
with open("data/latoken_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Initialize the RAG system
rag_system = RAGSystem(OPENAI_API_KEY, data)

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define a function to handle the /start command
async def start(update: Update, context: CallbackContext):
    context.user_data['state'] = None
    keyboard = [["Ask a Question", "Take a Test"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        "Hello! I'm the LATOKEN bot. What would you like to do?",
        reply_markup=reply_markup
    )

# Define a function to handle user messages
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    user_id = update.message.from_user.id
    state = context.user_data.get('state')

    if state == ASKING_QUESTION:
        try:
            bot_response = rag_system.generate_response(user_message)
            await update.message.reply_text(bot_response)
            # Ask a follow-up question related to the response
            follow_up_question = rag_system.ask_follow_up_question()
            await update.message.reply_text(f"Now, let me test your understanding. {follow_up_question}")
            context.user_data['state'] = None  # Reset state after follow-up
        except Exception as e:
            await update.message.reply_text(f"Sorry, I encountered an error: {str(e)}")
    elif state == TAKING_TEST:
        # Handle test responses here
        # For now, just reset the state
        await update.message.reply_text("Thank you for your response.")
        context.user_data['state'] = None
    else:
        if user_message == "Ask a Question":
            await update.message.reply_text("Sure! What would you like to know about LATOKEN, the Hackathon, or the Culture Deck?")
            context.user_data['state'] = ASKING_QUESTION
        elif user_message == "Take a Test":
            await update.message.reply_text("Let's test your understanding! Here's your first question: Why does LATOKEN help people learn about and buy assets?")
            context.user_data['state'] = TAKING_TEST
        else:
            await update.message.reply_text("Please select an option from the menu.")

# Define a function to reset the conversation state
async def reset(update: Update, context: CallbackContext):
    context.user_data['state'] = None
    await update.message.reply_text("Conversation reset. What would you like to do next?")

# Set up the bot
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# Add handlers for commands and messages
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Run the bot
print("Bot is running...")
app.run_polling()

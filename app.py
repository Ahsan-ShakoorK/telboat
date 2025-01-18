import streamlit as st
import subprocess
import os
import signal

# Initialize state to keep track of the bot process
if "bot_process" not in st.session_state:
    st.session_state.bot_process = None

st.title("LATOKEN Telegram Bot Controller")
st.write("Use this interface to start or stop the LATOKEN Telegram bot.")

# Define the path to the bot script
BOT_SCRIPT = "bot.py"  # Ensure bot.py is in the same directory as this script

# Button to start the bot
if st.button("Run Bot"):
    if st.session_state.bot_process is None:
        try:
            # Start bot.py as a subprocess
            st.session_state.bot_process = subprocess.Popen(
                ["python", BOT_SCRIPT],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            st.success("Bot started successfully!")
        except Exception as e:
            st.error(f"Failed to start the bot: {e}")
    else:
        st.warning("The bot is already running.")

# Button to stop the bot
if st.button("Stop Bot"):
    if st.session_state.bot_process is not None:
        try:
            # Terminate the subprocess
            os.kill(st.session_state.bot_process.pid, signal.SIGTERM)
            st.session_state.bot_process = None
            st.success("Bot stopped successfully!")
        except Exception as e:
            st.error(f"Failed to stop the bot: {e}")
    else:
        st.warning("The bot is not running.")

# Status check
if st.session_state.bot_process is not None:
    st.info("The bot is currently running.")
else:
    st.info("The bot is not running.")

import os
import sys
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Fetch Token from Render Environment Variables
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    logger.critical("FATAL: TELEGRAM_BOT_TOKEN environment variable is missing!")
    sys.exit("Error: TELEGRAM_BOT_TOKEN environment variable is missing.")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a greeting and list available commands."""
    welcome_text = (
        "⚡️ **Welcome to UtilEdge Bot** ⚡️\n\n"
        "Your minimal, high-speed text utility companion. Send me any raw text message, "
        "or use one of the commands below:\n\n"
        "📊 /stats - Word, character, and line count\n"
        "🔠 /upper - Convert text to UPPERCASE\n"
        "🔡 /lower - Convert text to lowercase\n"
        "🔄 /reverse - Reverse your text string\n"
        "ℹ️ /help - Show this information summary"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display the help menu."""
    await start_command(update, context)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Calculate and return string metric statistics."""
    text = " ".join(context.args) if context.args else ""
    if not text and update.message.reply_to_message:
        text = update.message.reply_to_message.text
    
    if not text:
        await update.message.reply_text("❌ Please provide text after the command or reply to a text message.")
        return

    char_count = len(text)
    word_count = len(text.split())
    line_count = len(text.splitlines()) if text else 0

    stats = (
        "📊 **Text Statistics:**\n"
        f"▪️ Characters: {char_count}\n"
        f"▪️ Words: {word_count}\n"
        f"▪️ Lines: {line_count}"
    )
    await update.message.reply_text(stats, parse_mode="Markdown")

async def upper_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Transform string into uppercase."""
    text = " ".join(context.args) if context.args else ""
    if not text and update.message.reply_to_message:
        text = update.message.reply_to_message.text

    if not text:
        await update.message.reply_text("❌ Provide text or reply to a message.")
        return
    await update.message.reply_text(text.upper())

async def lower_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Transform string into lowercase."""
    text = " ".join(context.args) if context.args else ""
    if not text and update.message.reply_to_message:
        text = update.message.reply_to_message.text

    if not text:
        await update.message.reply_text("❌ Provide text or reply to a message.")
        return
    await update.message.reply_text(text.lower())

async def reverse_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reverse text sequence."""
    text = " ".join(context.args) if context.args else ""
    if not text and update.message.reply_to_message:
        text = update.message.reply_to_message.text

    if not text:
        await update.message.reply_text("❌ Provide text or reply to a message.")
        return
    await update.message.reply_text(text[::-1])

async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fallback handler for plain text inputs when no command is specified."""
    text = update.message.text
    char_count = len(text)
    word_count = len(text.split())
    
    quick_reply = (
        f"✨ *Text Received\\!*\n\n"
        f"💡 _Tip: Use commands like /upper or /reverse on this text\\._\n\n"
        f"▪️ *Length:* {char_count} characters\n"
        f"▪️ *Words:* {word_count}"
    )
    await update.message.reply_text(quick_reply, parse_mode="MarkdownV2")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by Updates."""
    logger.error(f"Exception while handling an update: {context.error}")

def main() -> None:
    """Initialize and run the bot application."""
    logger.info("Initializing application setup...")
    
    # Initialize application
    application = Application.builder().token(TOKEN).build()

    # Register Handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("upper", upper_command))
    application.add_handler(CommandHandler("lower", lower_command))
    application.add_handler(CommandHandler("reverse", reverse_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    # Register global error logger
    application.add_error_handler(error_handler)

    logger.info("Starting polling stream...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    # Strict event loop control handling Python 3.11+ environments
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
    
    main()

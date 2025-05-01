from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = 'YOUR_BOT_TOKEN'

# List of audio file paths
AUDIO_FILES = [
    'audios/audio1.mp3', 'audios/audio2.mp3', 'audios/audio3.mp3', 'audios/audio4.mp3',
    'audios/audio5.mp3', 'audios/audio6.mp3', 'audios/audio7.mp3', 'audios/audio8.mp3',
    'audios/audio9.mp3', 'audios/audio10.mp3', 'audios/audio11.mp3', 'audios/audio12.mp3',
    'audios/audio13.mp3', 'audios/audio14.mp3', 'audios/audio15.mp3', 'audios/audio16.mp3',
    'audios/audio17.mp3', 'audios/audio18.mp3', 'audios/audio19.mp3', 'audios/audio20.mp3',
    'audios/audio21.mp3', 'audios/audio22.mp3', 'audios/audio23.mp3', 'audios/audio24.mp3',
    'audios/audio25.mp3', 'audios/audio26.mp3', 'audios/audio27.mp3', 'audios/audio28.mp3',
    'audios/audio29.mp3', 'audios/audio30.mp3', 'audios/audio31.mp3', 'audios/audio32.mp3'
]

# Dictionary to track which audio to send next per user (per context)
user_audio_index = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user_id = update.effective_user.id

    # Make a unique key for each user:
    # - In private chats: key = user_id
    # - In groups: key = chat_id + user_id (per group)
    if chat.type == 'private':
        key = f"private_{user_id}"
    else:
        key = f"group_{chat.id}_{user_id}"
    
    # Get current index or start at 0
    index = user_audio_index.get(key, 0)
    
    # Get audio file path
    audio_file = AUDIO_FILES[index]
    
    # Send the audio (reply in groups, normal in private)
    with open(audio_file, 'rb') as audio:
        if chat.type in ['group', 'supergroup']:
            await context.bot.send_audio(chat_id=chat.id, audio=audio, reply_to_message_id=update.message.message_id)
        else:
            await context.bot.send_audio(chat_id=chat.id, audio=audio)
    
    # Update index for next time (loop back if end reached)
    user_audio_index[key] = (index + 1) % len(AUDIO_FILES)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
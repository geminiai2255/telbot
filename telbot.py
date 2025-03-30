import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

TOKEN = '8130860956:AAEeuIM-BU58IXELUQIrfP6vxF5_moQ5brw'  # Replace with your bot's token

# List of jokes
jokes = [
    "Why don’t skeletons fight each other? They don’t have the guts!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "I told my computer I needed a break, and it froze.",
    "Why do cows have hooves instead of feet? Because they lactose!"
]

# List of trivia questions and answers
questions = {
    "What is the capital of France?": ["Paris", "London", "Rome"],
    "What is 2 + 2?": ["3", "4", "5"],
    "Which planet is known as the Red Planet?": ["Earth", "Mars", "Jupiter"],
}

# Function to start the bot
async def start(update: Update, context):
    # Create quick replies for starting the joke or quiz
    keyboard = [
        [KeyboardButton("Tell me a joke")],
        [KeyboardButton("Start Quiz")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Welcome! Choose an option:", reply_markup=reply_markup)

# Function to tell a random joke
async def tell_joke(update: Update, context):
    joke = random.choice(jokes)  # Pick a random joke
    await update.message.reply_text(joke)

# Function to handle the quiz start button
async def quiz(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Start Quiz", callback_data='start_quiz')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to the trivia bot! Click below to start the quiz:", reply_markup=reply_markup)

# Function to start the trivia quiz
async def start_quiz(update: Update, context):
    question = random.choice(list(questions.keys()))  # Pick a random question
    options = questions[question]
    keyboard = [
        [InlineKeyboardButton(options[0], callback_data='answer_' + options[0])],
        [InlineKeyboardButton(options[1], callback_data='answer_' + options[1])],
        [InlineKeyboardButton(options[2], callback_data='answer_' + options[2])],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(question, reply_markup=reply_markup)

# Function to handle quiz answers
async def handle_answer(update: Update, context):
    query = update.callback_query
    await query.answer()
    answer = query.data.split('_')[1]  # Get the answer choice

    question = query.message.text
    correct_answers = {
        "What is the capital of France?": "Paris",
        "What is 2 + 2?": "4",
        "Which planet is known as the Red Planet?": "Mars",
    }
    if answer == correct_answers.get(question, ""):
        await query.edit_message_text(text=f"Correct! {question} {answer}.")
    else:
        await query.edit_message_text(text=f"Oops! Incorrect. The correct answer was {correct_answers.get(question)}.")

# Function to handle text responses (such as quick replies)
async def handle_message(update: Update, context):
    text = update.message.text.lower()

    if "joke" in text:
        await tell_joke(update, context)
    elif "quiz" in text:
        await quiz(update, context)

# Main function to set up the bot
def main():
    # Create the application using the new Application class
    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(handle_answer))

    # Start polling and keep the bot running
    application.run_polling()

if __name__ == '__main__':
    main()


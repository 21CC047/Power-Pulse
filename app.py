import sqlite3
from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
import random
from textblob import TextBlob  # For sentiment analysis
import datetime

app = Flask(__name__)

# Motivational quotes and stress-relief tips
motivational_quotes = [
    "Believe in yourself! You are stronger than you think.",
    "Don't watch the clock; do what it does. Keep going.",
    "Your potential is endless. Go do what you were born to do!"
]
motivational_stories = [
    {
        "title": "The Elephant Rope",
        "story": "A group of elephants was stopped by a tiny rope tied to their front legs..."
    },
    {
        "title": "The Struggles of a Butterfly",
        "story": "A man saw a butterfly struggling to emerge from its cocoon..."
    }
]
stress_relief_tips = [
    "Take a deep breath, close your eyes, and focus on your breathing for a minute.",
    "Try a 5-minute walk or stretch to relieve tension.",
    "Close your eyes and imagine a peaceful place for a moment."
]


# Function to classify mood based on message sentiment
def classify_mood(message):
    analysis = TextBlob(message)
    polarity = analysis.sentiment.polarity
    if polarity > 0.1:
        return "Happy"
    elif polarity < -0.1:
        return "Sad"
    else:
        return "Neutral"


# SQLite database setup
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# Create necessary tables
def create_tables():
    conn = get_db_connection()
    c = conn.cursor()
    # Interactions table
    c.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Moods table
    c.execute('''
        CREATE TABLE IF NOT EXISTS moods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mood_type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


# Store user questions in the database
def store_question(question):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO interactions (question) VALUES (?)", (question,))
    conn.commit()
    conn.close()


# Store mood in the database
def store_mood(mood):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("INSERT INTO moods (mood_type) VALUES (?)", (mood,))
    conn.commit()
    conn.close()


# Get mood counts
def get_mood_counts():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT mood_type, COUNT(*) FROM moods GROUP BY mood_type")
    mood_data = c.fetchall()
    conn.close()
    return {row["mood_type"]: row[1] for row in mood_data}


# Get total interactions
def get_total_interactions():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM interactions")
    total = c.fetchone()[0]
    conn.close()
    return total


# Routes
@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/chat', methods=['POST'])
# def chat():
#     user_message = request.json.get('message', "").lower()
#     mood = classify_mood(user_message)
#     store_question(user_message)
#     store_mood(mood)
#
#     if "story" in user_message or "motivate" in user_message:
#         story = random.choice(motivational_stories)
#         response = f"{story['title']}:\n{story['story']}"
#     elif "stress" in user_message:
#         response = random.choice(stress_relief_tips)
#     else:
#         response = random.choice(motivational_quotes)
#
#     return jsonify({"response": response})
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', "").lower()
    mood = classify_mood(user_message)
    store_question(user_message)
    store_mood(mood)

    # Define responses for greetings
    greetings = ['hi', 'hey', 'hello', 'good morning', 'good afternoon', 'good evening']
    # Define responses for thanking
    thank_you = ['thanks', 'thank you', 'thanks a lot', 'thank you so much']
    # Define responses for farewells
    farewells = ['goodbye', 'see you', 'take care', 'bye']
    # Define responses for apologies
    apologies = ['sorry', 'my bad', 'i apologize']
    # Define responses for confirmations
    confirmations = ['okay', 'got it', 'sure', 'alright']

    response = ""

    # Greeting response
    if any(greeting in user_message for greeting in greetings):
        response = "Hello! How can I help you today?"
    # Thank you response
    elif any(thanks in user_message for thanks in thank_you):
        response = "You're welcome! Glad I could help."
    # Farewell response
    elif any(farewell in user_message for farewell in farewells):
        response = "Take care! See you next time."
    # Apology response
    elif any(apology in user_message for apology in apologies):
        response = "No problem! It's all good."
    # Confirmation response
    elif any(confirmation in user_message for confirmation in confirmations):
        response = "Awesome! Let me know if you need anything else."
    # Response for motivational stories or stress tips
    elif "story" in user_message or "motivate" in user_message:
        story = random.choice(motivational_stories)
        response = f"{story['title']}:\n{story['story']}"
    elif "stress" in user_message:
        response = random.choice(stress_relief_tips)
    else:
        response = random.choice(motivational_quotes)

    return jsonify({"response": response})

# Dashboard to view total interactions
@app.route('/dashboard')
def dashboard():
    total_interactions = get_total_interactions()
    return render_template('dashboard.html', total_interactions=total_interactions)

@app.route('/api/dashboard-data', methods=['GET'])
def get_dashboard_data():
    # Fetch total interactions
    total_interactions = get_total_interactions()

    # Fetch mood counts
    mood_counts = get_mood_counts()

    # Prepare mood trends for the chart
    mood_trends = [
        mood_counts.get("Happy", 0),
        mood_counts.get("Neutral", 0),
        mood_counts.get("Sad", 0)
    ]

    # Fetch popular stories dynamically (example: count interactions mentioning stories)
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        SELECT
            title,
            COUNT(*) AS interaction_count
        FROM
            interactions
        LEFT JOIN (
            SELECT "The Elephant Rope" AS title
            UNION ALL SELECT "The Struggles of a Butterfly"
        ) stories ON interactions.question LIKE '%' || stories.title || '%'
        GROUP BY title
    ''')
    popular_stories = [{"title": row["title"], "count": row["interaction_count"]} for row in c.fetchall()]
    conn.close()

    # Return the dashboard data
    return jsonify({
        "total_interactions": total_interactions,
        "mood_trends": mood_trends,
        "popular_stories": popular_stories
    })


# Initialize the tables on app start
create_tables()

if __name__ == '__main__':
    app.run(debug=True)

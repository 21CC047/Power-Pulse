PowerPulse - Your Personal AI Assistant

PowerPulse is an interactive chatbot designed to motivate users, relieve stress, and improve focus by providing personalized responses, motivational quotes, stress-relief tips, and short stories. It also tracks user interactions and mood trends dynamically.

Features

Interactive Chatbot

Responds to user messages with motivational quotes, stress-relief tips, and short stories.

Handles basic greetings like "Hi", "Hello", "Good morning", etc.

Classifies user mood using sentiment analysis.

Dashboard

Displays total interactions with the chatbot.

Visualizes user mood trends using a pie chart.

Lists popular motivational stories based on user interaction data.

Dynamic Data Tracking

Tracks and stores user questions and mood in a SQLite database.

Provides real-time updates to the dashboard.

Tech Stack

Backend

Flask: Lightweight web framework for building the backend and API endpoints.

SQLite: Database to store user interactions and mood data.

Flask-Mail: For future email integration.

Frontend

HTML5, CSS3: For structuring and styling the web pages.

Tailwind CSS: Responsive and modern UI design.

JavaScript: Dynamic content handling and asynchronous communication with the backend.

Chart.js: Data visualization library for displaying mood trends.

Libraries & APIs

TextBlob: Used for sentiment analysis to classify user moods.

Random: For selecting random motivational quotes and stories.

Fetch API: To make asynchronous requests between the frontend and backend.

How It Works

Chat Interaction: Users interact with the chatbot by typing messages. The chatbot processes the messages and responds with appropriate content.

Mood Classification: Each user message is analyzed using TextBlob to classify the mood as "Happy", "Neutral", or "Sad".

Data Storage: All user interactions and mood classifications are stored in the SQLite database.

Dashboard Visualization: The dashboard fetches data from the backend to display total interactions, mood trends, and popular stories.

Setup Instructions

Clone the repository:

git clone https://github.com/your-username/powerpulse.git
cd powerpulse

Install dependencies:

pip install -r requirements.txt

Run the application:

python app.py

The application will be accessible at http://127.0.0.1:5000/.

Initialize the database:

The database tables will be automatically created when the app starts.

API Endpoints

POST /chat: Handles user messages and provides appropriate chatbot responses.

GET /dashboard: Renders the dashboard page.

GET /api/dashboard-data: Returns JSON data for total interactions, mood trends, and popular stories.

Future Enhancements

Integration with email services to send daily motivational quotes.

More advanced sentiment analysis with machine learning models.

User authentication and personalized dashboards.

License

This project is licensed under the MIT License.

Feel free to contribute or raise issues on the repository to improve PowerPulse!


import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('leaderboard.db')
c = conn.cursor()

# Create a table to store leaderboard data if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS leaderboard (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        league TEXT,
        points INTEGER
    )
''')
conn.commit()

# List of Cloud Skill IDs
cloud_skill_ids = [
    "",
    "da336c06-602d-44ba-8a39-bcab298ff2d1",
    "52176c0a-5ab8-4071-a023-14a9767e28c7",
    "3ca62c80-b2e2-4a69-90ea-9fafd52c0143",
    "184b686c-c0fb-4572-adc4-10eed8449008"
    # ... (other IDs)
]

def get_profile_data(cloud_skill_id):
    url = f"https://www.cloudskillsboost.google/public_profiles/{cloud_skill_id}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve profile for ID {cloud_skill_id}. Status code: {response.status_code}")
        return None  # Return None for invalid IDs
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extracting the name, league, and points from the HTML structure
    name_tag = soup.find('h1', class_='ql-display-small')
    profile_league = soup.find('h2', class_='ql-headline-medium')
    points_tag = soup.find('strong')

    # Check if the profile data exists
    if name_tag:
        name = name_tag.text.strip()
    else:
        name = "Unknown"
    
    if profile_league:
        league = profile_league.text.strip()
    else:
        league = "No League"
    
    if points_tag:
        points = points_tag.text.strip().replace(' points', '')
    else:
        points = "0"  # Default points

    return name, league, points

# Function to fetch data from the database
def fetch_data_from_db():
    c.execute("SELECT name, league, points FROM leaderboard")
    return c.fetchall()

# Function to insert data into the database
def insert_data_into_db(data):
    c.executemany("INSERT INTO leaderboard (name, league, points) VALUES (?, ?, ?)", data)
    conn.commit()

# Check if the database is empty
c.execute("SELECT COUNT(*) FROM leaderboard")
if c.fetchone()[0] == 0:
    # If empty, scrape data and insert into the database
    leaderboard_data = []
    for cloud_skill_id in cloud_skill_ids:
        profile_data = get_profile_data(cloud_skill_id)
        if profile_data:
            name, league, points = profile_data
            leaderboard_data.append((name, league, int(points)))
    
    insert_data_into_db(leaderboard_data)

# Fetch data from the database
leaderboard_data = fetch_data_from_db()

# Create DataFrame from the leaderboard data
leaderboard_df = pd.DataFrame(leaderboard_data, columns=["Name", "League", "Points"])

# Rank the profiles by points, ensuring unique ranks
leaderboard_df = leaderboard_df.sort_values(by="Points", ascending=False)
leaderboard_df['Rank'] = range(1, len(leaderboard_df) + 1)

# Reset index to avoid showing the default index
leaderboard_df = leaderboard_df.reset_index(drop=True)

# Streamlit app starts here
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

        body {
            background: linear-gradient(to right, #f0f4f8, #d9e2ec); 
            font-family: 'Poppins', sans-serif;
            margin: 0;
            padding: 0;
        }

        /* Header styles */
        .header-left {
            position: absolute;
            top: 20px;
            left: 20px;
            display: flex;
            align-items: center;
        }

        .header-right {
            position: absolute;
            top: 20px;
            right: 20px;
            display: flex;
            gap: 15px;
            align-items: center;
        }

        .header-right a {
            color: #4a90e2;
            font-size: 1.2em;
            text-decoration: none;
            padding: 10px 12px;
            background-color: #ffffff;
            border-radius: 50%;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
            transition: all 0.3s ease;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .header-right a:hover {
            background-color: #e6f0ff;
        }

        h1 {
            text-align: center;
            font-size: 3em;
            color: #1c3d5a; 
            margin: 50px 0 20px 0;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1); 
            animation: fadeInDown 1.5s ease-in-out;
        }

        h2 {
            text-align: center;
            font-size: 2.5em;
            color: #4a90e2; 
            margin: 20px 0;
            font-weight: 400; 
        }

        .sidebar {
            background: linear-gradient(to bottom, #4a90e2, #1c3d5a); 
            color: #ffffff; 
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); 
            transition: all 0.3s ease-in-out;
        }

        .sidebar h2 {
            font-size: 1.8em;
            margin-bottom: 10px;
            border-bottom: 2px solid #66b3ff; 
            padding-bottom: 5px;
        }

        .sidebar p {
            font-size: 1.2em;
            line-height: 1.6;
            margin: 10px 0;
        }

        .sidebar a {
            color: #d9e2ec; 
            text-decoration: none;
            font-weight: bold;
        }

        .sidebar a:hover {
            text-decoration: underline; 
        }

        table {
            width: 90%;
            margin: 30px auto; 
            border-collapse: collapse;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15); 
            background-color: #ffffff; 
            border-radius: 10px; 
            overflow: hidden; 
            animation: fadeInUp 1s ease-in-out;
        }

        th {
            background-color: #4a90e2; 
            color: #ffffff;
            padding: 20px;
            text-align: center;
            border-bottom: 2px solid #e0e0e0;
            font-weight: 700; 
            text-transform: uppercase; 
            font-size: 1.1em;
        }

        td {
            padding: 15px;
            text-align: center;
            border: 1px solid #e0e0e0;
            color: #1c3d5a; 
            font-size: 1.05em;
            transition: background-color 0.3s ease;
        }

        tr:nth-child(even) {
            background-color: #f0f4f8; 
        }

        tr:hover {
            background-color: #d9e2ec; 
            transition: background-color 0.3s ease;
        }

        .success-message {
            text-align: center;
            font-size: 1.2em;
            color: #28a745; 
            margin: 20px 0;
            animation: fadeIn 1s ease-in-out;
        }

        .warning-message {
            text-align: center;
            font-size: 1.2em;
            color: #f0ad4e; 
            margin: 20px 0;
            animation: fadeIn 1s ease-in-out;
        }

        .perks {
            text-align: center;
            margin: 20px 0;
            font-size: 1.1em;
            color: #1c3d5a;
            animation: bounce 2s infinite;
        }

        .perks::before {
            content: "🎉 ";
            font-size: 1.5em;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-10px); }
            60% { transform: translateY(-5px); }
        }
    </style>
    """, unsafe_allow_html=True
)

# Sidebar Content
st.sidebar.markdown("<div class='gdg-organizer'>Khushi Bagga</div>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='organizer-info'>GDG PIET Organizer and Tech Enthusiast, focused on bringing the latest in cloud technology to our community!</div>", unsafe_allow_html=True)

# Mentor Information
st.sidebar.markdown("<p class='mentor-info'>If you need any assistance, feel free to reach out to your assigned mentor.</p>", unsafe_allow_html=True)

# Divider
st.sidebar.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# Labs Information Header
st.sidebar.markdown("<h2 class='subheader'>Labs Information</h2>", unsafe_allow_html=True)
st.sidebar.write("Join us in our interactive labs where you'll get hands-on experience with the latest technologies!")

# Lab List
labs = [
    "The Basics of Google Cloud Compute",
    "Get Started with Cloud Storage",
    "Get Started with API Gateway",
    "Get Started with Looker",
    "Get Started with Dataplex",
    "Get Started with Google Workspace Tools",
    "Cloud Functions: 3 Ways",
    "App Engine: 3 Ways",
    "Cloud API: 3 Ways",
    "Monitoring in Google Cloud",
    "Networking Fundamentals on Google Cloud",
    "Analyze Images with the Cloud Vision API",
    "Prompt Design in Vertex AI",
    "Develop GenAI Apps with Gemini and Streamlit"
]

st.sidebar.markdown("<ul class='lab-list'>" + "".join(f"<li>{lab}</li>" for lab in labs) + "</ul>", unsafe_allow_html=True)

# Divider
st.sidebar.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# More Information
st.sidebar.markdown(
    "For more details about the event and additional resources, visit our [LinkTree](https://linktr.ee/gdsc_piet)."
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

        /* Gradient text color */
        h1 {
            text-align: center;
            font-size: 2.8em;  /* Adjusted font size */
            width: 100%;  /* Ensure it takes full width for centering */
            background: linear-gradient(to right, #4facfe, #00f2fe); /* Blue Gradient */
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 50px 0 20px 0;
            text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.3);
            animation: fadeInDown 1.5s ease-in-out, scaleUp 1s ease-in-out forwards;
            font-family: 'Poppins', sans-serif;
            white-space: nowrap;  /* Prevent wrapping */
        }

        @keyframes scaleUp {
            0% {
                transform: scale(0);
                opacity: 0;
            }
            50% {
                opacity: 1;
            }
            100% {
                transform: scale(1);
            }
        }

        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Card container style */
        .card-container {
            display: flex;
            justify-content: center;
            margin: 30px 0;
            flex-wrap: wrap;  /* Allow wrapping */
        }

        /* Card style */
        .card {
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            margin: 10px;
            padding: 20px;
            width: 250px;  /* Fixed width for cards */
            text-align: center;
            transition: transform 0.3s ease;
            font-family: 'Poppins', sans-serif;
        }

        .card:hover {
            transform: translateY(-5px);
        }

        /* Card title style */
        .card-title {
            font-size: 1.5em;
            color: #003f5c; /* Darker Blue for contrast */
            margin-bottom: 10px;
            background: linear-gradient(to right, #4facfe, #00f2fe);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>

    <h1>🚀 GDG PIET LEADERBOARD 🚀</h1> <!-- Title should fit in one line -->
    <div class="divider"></div>
    
""", unsafe_allow_html=True)

# Prepare a list to hold data for each profile
leaderboard_data = []

for cloud_skill_id in cloud_skill_ids:
    profile_data = get_profile_data(cloud_skill_id)
    if profile_data:
        name, league, points = profile_data
        leaderboard_data.append({
            "Name": name,
            "League": league,
            "Points": int(points) 
        })

# Create DataFrame from the leaderboard data
leaderboard_df = pd.DataFrame(leaderboard_data)

# Rank the profiles by points, ensuring unique ranks
leaderboard_df = leaderboard_df.sort_values(by="Points", ascending=False)
leaderboard_df['Rank'] = range(1, len(leaderboard_df) + 1)

# Reset index to avoid showing the default index
leaderboard_df = leaderboard_df.reset_index(drop=True)

# Display the leaderboard if data is available
if not leaderboard_df.empty:
    st.table(leaderboard_df[['Rank', 'Name', 'League', 'Points']].set_index('Rank')) 

# Display perks for the top 5 users only
st.markdown("""
    <style>
        /* Perks Section Style */
        .perks {
            text-align: center;
            font-size: 1.5em;
            margin: 10px 0;
            padding: 15px;
            border-radius: 10px;
            color: #ffffff;
            background: linear-gradient(135deg, #66b3ff, #4a90e2);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            animation: fadeIn 0.8s ease-in-out;
            transition: transform 0.3s ease, background 0.3s ease;
        }

        .perks:hover {
            transform: translateY(-5px);
            background: linear-gradient(135deg, #4a90e2, #66b3ff);
        }

        h2 {
            text-align: center;
            font-size: 2.5em;
            color: #1c3d5a;
            margin: 40px 0;
            animation: fadeInDown 1.5s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
    <h2>Perks for Top 5 Scorers!</h2>
""", unsafe_allow_html=True)

top_5_scorers = leaderboard_df.head(5)  # Get the top 5 scorers
for index, row in top_5_scorers.iterrows():
    if row['Points'] > 100:  # Example threshold for perks
        st.markdown(f"<div class='perks'>{row['Name']} has unlocked exclusive perks!</div>", unsafe_allow_html=True)

else:
    st.write("No data available for the leaderboard.")

# Save the leaderboard to a CSV file (optional)
leaderboard_df.to_csv('cloud_skill_leaderboard.csv', index=False)
st.success("Leaderboard data has been saved to 'cloud_skill_leaderboard.csv'.")

# Automatic refresh every 24 hours
st.markdown("""
    <script>
        setTimeout(function(){
            window.location.reload(1);
        }, 86400000); // 86400000 milliseconds = 24 hours
    </script>
""", unsafe_allow_html=True)

# Close the database connection
conn.close()

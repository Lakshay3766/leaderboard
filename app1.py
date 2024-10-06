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
    "3ccc8d49-0117-44c5-843d-7f12c0a47a41",
    "ceb77f52-1880-4dd8-ad6f-39dc9237e735",
    "da1dd994-930c-4426-bb4f-49d4b711e3cd",
    "1207555e-52c6-4e86-969e-e130cc7815ed",
    "7c866e32-972b-464b-b02c-176e779e5439",
    "d9172948-4eee-4ea7-983c-5b952c5b3158",
    "c68a2446-b0d6-4055-a915-dfb9e60cc2ce",
    "dc4cd7ed-437d-41bc-9939-96c44bd7c192",
    "a200bed9-ba80-4e52-b8ef-1d6f3e35ef41",
    "dd3fd111-9803-455b-a5d0-2cf2f82b18b6",
    "630bc0ef-4892-4204-90f3-31a3a0fbea48",
    "ac9a11aa-7811-4c17-b7b0-b4db66fd5c36",
    "a92ea3c1-52a4-4f93-a6b8-527bfa6cd91b",
    "66bf4afa-8041-4585-9fd6-d0fc0209a62a",
    "573068ac-a46a-4ee1-91c8-9f574369e300",
    "28cf0272-3bb5-4ff5-8e75-13ccc82f439f",
    "46c0b505-ee2e-42a9-9735-91c2a5d164b5",
    "5ab13272-fefd-44e6-ab43-7ecf663a68dd",
    "7e7f1d38-d3e7-4321-9c7f-95d1c34b656d",
    "640d5bf0-757f-45b8-b1b9-70a9d79aa669",
    "15af74fc-b83f-48ce-9182-2bbd23a83b4b",
    "085a8a58-c4b8-45b3-a395-a9f9d4f832ad",
    "b24b33c8-3e10-4025-ae93-b26eceade979",
    "24d5e91c-c44b-470d-952f-7683b74d7246",
    "ed2c55e3-56f8-4fb8-9eab-9f34659cc970",
    "267b2345-1dfd-45c4-8e60-1f4c8789ec70",
    "e94efe85-98bf-4bcf-afd6-5dd8fe5e7f88",
    "15c532a0-ad80-4bff-8c94-98f6b95a2039",
    "2956f6e1-6a58-4f8f-810a-0ba28a5f0bf5",
    "adf03c65-a5fe-4f48-8393-f3e06765e3b1",
    "1f592127-cdd9-4834-a42f-0f5f8442de92",
    "da336c06-602d-44ba-8a39-bcab298ff2d1",
    "52176c0a-5ab8-4071-a023-14a9767e28c7",
    "184b686c-c0fb-4572-adc4-10eed8449008",
    "efc699ca-9251-41d1-a73d-ab6703fed673",
    "af5c87ad-2530-4216-88f5-2c9cad09ea0c",
    "9a5e703a-40be-4f30-9e15-2c437d2f3a3e",
    "07931846-23d0-4956-b00d-b8a8f3578263",
    "d4d272bd-90ad-402b-aa3a-ca2739c4fbac",
    "df07f692-7514-4fe6-a0a9-c03d915c2f7e",
    "9b5122e3-958b-47d9-8aeb-d280635e7c7e",
    "afa3c028-b551-44c7-a76d-b2999cfa3529",
    "a1bcaadc-8365-4fec-80ae-dc972e9e7e54",
    "29d8d4ae-500c-4464-98b9-3a9ef4351864",
    "f93ae1a1-1f5e-4ea0-b33b-5f051ce5d7b5",
    "3b933ebe-642b-4e27-bf5d-0e89f0dce38d",
    "3ba07357-3e73-45f2-90f3-219aa4a7dcaf",
    "6f6f5691-1e08-4085-a6d9-1a8a324c8408",
    "fed3acc1-46c1-412c-b623-f1cefe3a69e9",
    "de64a194-bd15-4022-b1c3-6929b026456b",
    "e2e11dfe-fa75-45ea-b830-a70f416900b1",
    "6d7c49ef-bf81-4324-b8aa-997d2f5fe73e",
    "7b3d3cde-3d8e-48e9-8f64-1e9ad5f2bf21",
    "6d134471-a1bc-4408-b517-10b711b35324",
    "d0293f22-264c-434c-9dc7-aa0338ef86a5",
    "5503a838-2835-426c-86ae-79a5523cdb9b",
    "98e06896-be74-46e5-939d-eb82df8500f5",
    "49b3c112-e53d-4fb1-910e-3938a004d035",
    "a71e0239-fd46-4fd6-9fa1-f359a95a8879",
    "50f6f833-8f70-4042-ac94-1806f4f84d2e",
    "9d4dca33-288d-4194-9d1f-6cc7dfa8c475",
    "482de034-9c00-4d48-a0be-bec1c79e115e",
    "57b0efeb-16d2-47a1-b68f-44f7d1797df8",
    "d2a90447-173c-4223-8eaa-e9edfce1f8d2",
    "2dd66e03-bd4b-4a76-95b9-c0a22acf9486",
    "8b600348-ba09-4461-828f-69a64172dc2e",
    "f260fe0b-1778-4e35-b8e3-9cd60d8a38ef",
    "6447c4be-a22b-4196-b309-05616dd2b3f8",
    "33c16533-81cc-4619-8318-6d121772a3e7",
    "d7dc9dae-b8f7-49a9-a67f-0930fdc5bc5a",
    "a1bcaadc-8365-4fec-80ae-dc972e9e7e54",
    "3f9d27a5-c8ae-4088-ab9a-5c843237269c",
    "109ce917-27a4-4417-a50d-b6ca5e2f8d16",
    "786aaf5c-50e1-430c-b7a1-28610ea9c58a",
    "f67befe8-4a82-48ef-83f2-5be18028fb05",
    "28cf0272-3bb5-4ff5-8e75-13ccc82f439f",
    "1cc3bf44-38dc-4ffa-951b-9dfda7c16ff5",
    "a16bbe2b-9a5c-481f-b376-1daff3f66753",
    "cdc633da-0bfb-445c-b057-1e312a2b814b",
    "7f60487f-0437-4b09-9d79-e8933eb5e942",
    "30c9cb53-b7f8-4cf6-9541-f9ef439b6c47",
    "7b6b25b9-a7ee-4a3f-8648-70982a72c666",
    "6a9889ba-0a61-4e07-a508-8867ec359779",
    "2a9b0409-9acf-4869-b5df-c53e55f21380",
    "e3e704d6-a5fc-4586-b454-08717cb99a04",
    "ac6fea00-a531-41b6-844b-c108dfbef8a9",
    "2de1bbf0-086e-4bda-b674-e43e1fa9039c",
    "d4a53984-79db-44b9-a5f2-f3421762c9c3",
    "cb89d6aa-b45e-4740-98b7-5d8b9cd3440c",
    #"2be1df16-30cc-4bd0-b6bd-efb6d0e47645",
    "1ae8c3a2-a6f0-42fe-8c0c-7470aa8ff42b",
    "b92cfc4c-d9b2-4ad8-85fe-c9196fe7a1e9",
    "9cf66005-0d14-44b3-a7a9-f767736b2d38",
    "097c6c02-e294-430d-bbe6-ec70dc8c3c9a",
    "0743f688-5c74-49ea-ab4d-421e69a406a5",
    "e2e11dfe-fa75-45ea-b830-a70f416900b1",
    "81c91b98-a0f4-411b-aa32-b6336e1bb741",
    "d8f4ee93-fa30-46cd-be73-848a2b239fa0",
    "07931846-23d0-4956-b00d-b8a8f3578263",
    "b8e50799-874e-474b-8931-70dcc6b97296",
    "a900180b-f017-4419-9541-f75956a100b8",
    "1d8144d1-8ef0-42bb-9f6d-1975becabb63",
    "aa9e6ec8-d4e2-43f2-9e3e-f721617086b6",
    "830d5250-8d4a-4759-a3f8-fa2ad1d95144",
    "9b1a2661-c26b-438d-976b-7b41e06dac28",
    "856d36db-3dd5-47c2-b160-96fc664e7608",
    "bf92e317-a356-4bf0-960d-4686e53a9daa",
    "abb1155d-578c-467f-9931-9e570fdd064c",
    "072b3d6d-3231-4e65-832a-f948debf3379",
    "bc843c1d-cce7-4add-8eb6-4b5dfdc9a605",
    "b2cca048-a3a4-4a97-ac22-0d57bd3e97f9",
    "69e21bb9-d156-42d1-b096-05a9dd104238",
    "52c35a00-4929-4913-854e-b04088aeb341",
    "bb1fc0c9-d66f-443e-862b-e5197849d7ea",
    "11ace016-2523-4658-8080-6daafe1e6ae6",
    "26c79e6f-dc4b-48c9-9e0b-665ab9c4389c",
    "a006d140-d494-48be-82c8-6e6f06cfa1df",
    "771d97a8-cc3a-4f73-a8ea-ae518a30276b",
    "58c53847-7cfe-4c00-b380-ff0079440b9c",
    "5d23404d-1bb1-40db-8987-06326141606a",
    "77d8cebd-88cd-4fe8-b243-bb83e6e6cf85",
    "f1083b57-3e75-4e63-aa84-cfa20323623b",
    "28de82ef-c0ce-4208-8bf9-88e6a2ca9141",
    "e33726d5-0796-4ff1-9ae9-7537068b4fa2",
    "7e2df6Ob-e13d-4b0f-aeae-f1516b0a831f",
    "d9172948-4eee-4ea7-983c-5b952c5b3158",
    "b5d2c3e2-1b0d-4f9c-9f3b-5e8f4c3b2d4c",
    "101f5398-b4ff-4184-a792-5cd27d766232",
    "3f5557f0-24e2-4f4d-b8e9-d3bb6b55eca0",
    "680b7a69-d4f7-4187-9a66-f281cb945fba",
    "3fbbbe3d-0b47-45f1-b710-f03d05a68533",
    "39ce3d96-deeb-490b-b3d0-5eb8171f8ee8",
    "012da062-f39a-4cdc-a586-f2f0bf4d636a",
    "cbf9cce6-7fd5-4247-93f3-76cf35334636",
    "c1b6aa7d-3292-4f1a-9a70-bf88d7fc9f71",
    "b85ca717-9d1f-4c0f-addd-1231b834f231",
    "c321b56c-fc91-4a9c-b89a-2e0189c4d8d5",
    "af82833a-5d62-45c1-bebc-1d3557d936ff",
    "1bc573b2-3da1-413f-81fd-09ccf595b563",
    "4864375b-9cf1-4a04-b743-91e055534c21",
    "734a8a9d-94f7-4f45-94c9-8acac8c94b04",
    "ff980070-845d-42d1-b376-faa7b23dbf65",
    "966749b7-6aa7-4999-97c4-6fdfeadcfaf9",
    "8c6da3fb-5bc4-4176-a3ec-66347c1c4877",
    "43d44e3f-e5af-45fe-99bd-66c641fa7cb4",
    "878de5b5-0def-4308-ab9b-3d34a2c632b1",
    "0edf3a38-17b2-4ccf-8180-bd470cbf36f7",
    "35034cc5-fcc6-44fc-b5ec-ba720b87c161"

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
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

    /* Sidebar background with gradient and rounded corners */
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #2c3e50, #34495e); /* Professional gradient */
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* Smooth shadow for depth */
        color: #ecf0f1; /* Light text for contrast */
        font-family: 'Roboto', sans-serif; /* Modern font */
        animation: fadeIn 1s ease-in-out; /* Smooth entry animation */
    }

    /* Fade in animation */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    /* Highlighted GDG Organizer name - Khushi Bagga */
    .gdg-organizer {
        font-size: 2.2em;
        font-weight: 600;
        text-transform: uppercase;
        background: linear-gradient(135deg, #1abc9c, #3498db); /* Cool gradient */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.3); /* Subtle shadow for depth */
        text-align: center;
        margin-bottom: 30px;
        animation: pulse 1.2s infinite; /* Pulse animation */
    }

    /* Pulse animation */
    @keyframes pulse {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
        100% {
            transform: scale(1);
        }
    }

    /* Khushi Bagga's professional title styling */
    .organizer-info {
        font-size: 1.6em;
        color: #bdc3c7; /* Softer text for professional tone */
        text-align: center;
        line-height: 1.6;
        font-style: italic;
        margin-bottom: 40px;
    }

    /* Title styling with border and color accent */
    .sidebar-title {
        font-size: 1.7em;
        font-weight: 500;
        margin-bottom: 20px;
        color: #ecf0f1;
        border-bottom: 2px solid #2980b9;
        padding-bottom: 10px;
        animation: slideIn 0.8s ease-in-out;
    }

    /* Slide in animation for titles */
    @keyframes slideIn {
        from { transform: translateX(-50px); }
        to { transform: translateX(0); }
    }

    /* Subheader and labs information */
    .subheader {
        font-size: 1.4em;
        font-weight: bold;
        color: #3498db; /* Bright accent for visibility */
        margin-top: 25px;
        margin-bottom: 10px;
        text-transform: uppercase;
    }

    .mentor-info {
        font-size: 1.2em;
        color: #bdc3c7; /* Softer text for mentor info */
        margin-bottom: 25px;
        line-height: 1.6;
    }

    /* Lab list items styling */
    .lab-list {
        font-size: 1.1em;
        color: #ecf0f1;
        padding-left: 10px;
        list-style-type: none;
        padding-left: 0;
        animation: fadeInUp 1s ease-in-out;
    }

    /* Subtle animation for list items */
    .lab-list li {
        margin-bottom: 10px;
        position: relative;
        padding-left: 20px;
    }

    .lab-list li:before {
        content: '•';
        color: #f39c12; /* Orange bullet points */
        position: absolute;
        left: 0;
        top: 3px;
    }

    /* Divider styling */
    .divider {
        border-top: 1px solid #7f8c8d;
        margin: 20px 0;
        opacity: 0.8;
        animation: fadeIn 1.2s ease-in-out;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar content
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

        /* Responsive table styling */
        .data {
            margin: auto; /* Center the table */
            width: 80%; /* Set the width for larger screens */
        }

        @media (max-width: 768px) {
            h1 {
                font-size: 2em;  /* Adjust font size for mobile devices */
                white-space: normal; /* Allow wrapping on smaller screens */
            }

            .data {
                width: 90%; /* Decrease the width for mobile devices */
                margin: auto; /* Center the table */
            }

            .data th, .data td {
                font-size: 0.8em; /* Decrease font size for mobile devices */
                padding: 8px; /* Adjust padding for smaller screens */
            }
        }

        @media (min-width: 769px) {
            .data {
                width: 100%; /* Full width for larger screens */
            }

            .data th, .data td {
                font-size: 1em; /* Standard font size for larger screens */
                padding: 12px; /* Adjust padding for better spacing */
            }
        }
    </style>

    <h1>🚀LEADERBOARD 🚀</h1> <!-- Title should fit in one line -->
    <div class="divider"></div>
    
""", unsafe_allow_html=True)


# Display the leaderboard if data is available
if not leaderboard_df.empty:
    # Render the DataFrame as an HTML table
    st.write(leaderboard_df[['Rank', 'Name', 'League', 'Points']].set_index('Rank').to_html(classes='data', header="true", index=True, escape=False), unsafe_allow_html=True)

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

if top_5_scorers.empty:
    st.write("No data available for the leaderboard.")
else:
    perks_unlocked = False  # Flag to check if any perks are unlocked
    for index, row in top_5_scorers.iterrows():
        if row['Points'] > 100:  # Example threshold for perks
            st.markdown(f"<div class='perks'>{row['Name']} has unlocked exclusive perks!</div>", unsafe_allow_html=True)
            perks_unlocked = True  # Set the flag to True if perks are unlocked

    if not perks_unlocked:
        st.write("No players have unlocked exclusive perks.")


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

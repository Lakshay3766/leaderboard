import requests
import json

# Your Discord webhook URL
WEBHOOK_URL = 'https://discord.com/api/webhooks/1282503600160903259/rOiYaHh8yMs6nH5TZktiV562Dkbj2wzVxq6N-u2URgqfeQDRFFoLJ7dv_sFLRAjAevDq'  # Replace with your actual webhook URL

# The URL of your Streamlit API running on localhost
API_URL = 'http://localhost:8501/?json=1'  # Use localhost

def post_leaderboard_to_discord():
    print("Fetching leaderboard data from API...")
    try:
        # Fetch the leaderboard data from your Streamlit API
        response = requests.get(API_URL)

        # Print the status code of the response
        print(f"API response status code: {response.status_code}")
        
        # Print the raw response for debugging
        print("Raw response from API:", response.text)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to fetch data from API: {response.status_code}")
            return

        leaderboard_data = json.loads(response.text)

        # Format the leaderboard message
        leaderboard_message = "🚀 **Leaderboard** 🚀\n\n"
        for entry in leaderboard_data:
            leaderboard_message += f"**{entry['Rank']}. {entry['Name']}** - {entry['League']} - {entry['Points']} points\n"

        # Create the payload for the webhook
        payload = {
            "content": leaderboard_message
        }

        # Send the POST request to the Discord webhook
        webhook_response = requests.post(WEBHOOK_URL, json=payload)
        
        # Print the status code and response content of the webhook request
        print(f"Webhook response status code: {webhook_response.status_code}")
        print("Webhook response content:", webhook_response.text)

        if webhook_response.status_code == 204:
            print("Leaderboard posted to Discord successfully!")
        else:
            print(f"Failed to post to Discord: {webhook_response.status_code}")

    except Exception as e:
        print("Failed to post leaderboard to Discord:", e)

# Call the function to post the leaderboard
post_leaderboard_to_discord()

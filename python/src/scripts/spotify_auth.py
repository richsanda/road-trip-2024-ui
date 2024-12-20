import requests
import base64

# Your Spotify app credentials
client_id = 'id'
client_secret = 'secret'

# Encode the client_id and client_secret
credentials = f"{client_id}:{client_secret}"
b64_credentials = base64.b64encode(credentials.encode()).decode()

# Set the URL and headers
url = "https://accounts.spotify.com/api/token"
headers = {
    "Authorization": f"Basic {b64_credentials}",
    "Content-Type": "application/x-www-form-urlencoded"
}
payload = {
    "grant_type": "client_credentials"
}

# Request an access token
response = requests.post(url, headers=headers, data=payload)
access_token = response.json().get("access_token")
print(access_token)

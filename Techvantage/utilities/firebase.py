import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings
from rest_framework import exceptions

# Initialize Firebase App (this should only be done once in your entire project)
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "newproject-7ad97",
  "private_key_id": "b394a7caa7be4dcfb5a87e3f91f09a98ccf7a7ae",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDUMXklrac+U2E0\nIMuTH8p5986ak3UiiNfmL8YBj1dffA9rzqaUbU3jq5de5xFNtth72HH/6kJOwmDX\n6ie7txgsvbt9TQ60HOeplwudybB0jGQZ+1zvcLnDHy7O/OBkQMhmqNNewd97Ig1R\n08etxXJNLsXArhFJ79B2ireXc5MNumFi4gKgo77pqbQpcWFxpakmIqkl0Gw6PFFC\n+ckzmOFKSrEZbP1zXiIiSCvI3iZ0gMrNFG4+CWGFUP0aOKkmRB7PiUze+zzvddLq\nFXEEMM/n+nUcpZzA5PTNpImyetT/nakNHa2rIyLyv+k15wVZbveXTlAvNIRlzSNN\nuKrYCLXjAgMBAAECggEAGpfmtHuqgaume4d+q/4ofJe7i3DelcjrsfwbxzdFPoDI\nV/0KsIBwag+nxWuVJhW71O2f//BGhiNjSrwcZbDBNV5EAKSnKpiSyhTVjl1oIXs0\n0nLHx3Rru5INZkCYCMh7tS4Ea5RFo2N1ouM1W8hqllS90POf1BHboPeqoa8I54fR\nVbC0U10+KOX6XHFSBB4ok0LCmD/GpkazUQSHArXa98E3a9a7cI1RGqcF9vqG3Exa\nI8bNpCm6BuyYGaESKZzfYVCZ54ApEV5WYN8/BU72NJribUnh6V2pVXBwjgQgxoRI\ny/l8kh5R5r9IHTQIqzd64ADpQcavHm4Ow8P+uOBCCQKBgQDx73nrlx5FgRuVm2GB\nzybEljtpGJwvQ5QtbU6GLZxOoiOgBwwXu6lOd3AHchZdg9VktfGPpGFpLMgNU6g/\nENS07kOjMQ6byFB/XIktZpkSiDTct2VflNy64zT74sQw5zDK3XrOMahr86z4yXUg\n4n1a6KgtAYq40b1vhos82ZVg+QKBgQDgh15dcar0CQkxycZNZT6mLnYJRe8oMDKu\nAxX/FbsRPjjDxd8StzMdkXAxPhhwCczQIttzPg6R5ConQ38bYNh3Wrg29i+Poq8V\nBeJqlvhUXco1Cp6oIi5Cw69m9itXWtPGiXRCbicy80FqTqy1+C2XpimMzTMULl6d\nM8JmANnguwKBgQDdhV9GBqVyEIgYUSBTwkAGCmS1kxIW+LKpcYdPtl2DZlRmR22c\nIXkhXp0WRDEUSQzP3QQkeOe0bIt0IGBR9nA8hlkqCFYO77g9FZaJGoMYA90bJ1VL\n0jrVaApwhC8Nc/IqHec++xryVTjQx21WwerznUm3g8zn8yuX/UJqYfOzyQKBgQCQ\nuxG8AFpnRi/UFTGrkBjLPGW/4oGgETmJ69lQ/awBGG+02qbJxKfBZo/AXjuYdOi+\nPcnhxl3T8xStDJgxiMLgZO0cGKNd3ksnrQxfEwPuNiry9+5/iNDzHnrBTutvOtAK\nSW5Up/bCpAVFxoMUJW8WMvjTly5W0vEQOl4ULHZFowKBgAUDwlyLADa5Ou6O19Dd\n4bxSK1AkC6RO9O40qrQCZwONqrDy8Bq6NE1abDlc4FAM4JUqSFfLP3AK+QgIH8Ap\nnIW3Wgq9Tm9UCH45N675dyfpCmmwrT/fzbKpuNdlqNIoTip/YMRAc/RlOfW+l5ZY\nKK6ZSyJM0J/vacGnipKz9k4m\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-6at0z@newproject-7ad97.iam.gserviceaccount.com",
  "client_id": "115858408144336071349",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-6at0z%40newproject-7ad97.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
})
firebase_admin.initialize_app(cred)

def verify_firebase_token(id_token):
    """
    Verifies the Firebase ID token sent by the client.
    Raises exceptions if the token is invalid or expired.
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except auth.ExpiredIdTokenError:
        raise exceptions.AuthenticationFailed('Token has expired. Please log in again.')
    except auth.InvalidIdTokenError:
        raise exceptions.AuthenticationFailed('Invalid token. Please log in again.')
    except Exception as e:
        raise exceptions.AuthenticationFailed('Token authentication failed.')

def login_firebase_user(email, password):
    """
    Simulates a Firebase login using REST API.
    """
    import requests
    import json

    FIREBASE_WEB_API_KEY = settings.FIREBASE_WEB_API_KEY
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": True
    })
    
    response = requests.post(url, data=payload)
    data = response.json()

    if response.status_code == 200:
        return data  # contains token and user info
    else:
        raise exceptions.AuthenticationFailed(data.get("error", {}).get("message", "Authentication failed"))

def logout_firebase_user(uid):
    """
    Revokes refresh tokens for the user, effectively logging them out.
    """
    auth.revoke_refresh_tokens(uid)

def create_firebase_user(email, password, display_name):
    """
    Creates a new Firebase user with email and password.
    """
    try:
        user = auth.create_user(email=email, password=password, display_name=display_name) 
        return user
    except Exception as e:
        raise exceptions.APIException(f'Error creating user: {str(e)}')
    
def update_user_display_name(uid, new_display_name):
    """
    Function to update Firebase user's displayName.
    """
    user = auth.update_user(
        uid,
        display_name=new_display_name  # Updating displayName
    )
    return user

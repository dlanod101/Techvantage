import firebase_admin
from firebase_admin import credentials, auth
from django.conf import settings
from rest_framework import exceptions

# Initialize Firebase App (this should only be done once in your entire project)
cred = credentials.Certificate('/path/to/firebaseprivatekey.json')
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

import firebase_admin
from firebase_admin import credentials, firestore
import os

def initialize_firebase():
    """
    Initializes the Firebase Admin SDK.
    """
    # Check if the app is already initialized
    if not firebase_admin._apps:
        # Securely load credentials from environment variables
        cred_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if cred_path:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("Firebase initialized successfully.")
        else:
            print("GOOGLE_APPLICATION_CREDENTIALS environment variable not set. Firebase not initialized.")

def get_firestore_db():
    """
    Returns a Firestore client instance.
    """
    # Ensure Firebase is initialized before returning the client
    if not firebase_admin._apps:
        initialize_firebase()

    # Check again in case initialization failed
    if firebase_admin._apps:
        return firestore.client()
    else:
        # Return None or raise an exception if Firebase is not available
        return None

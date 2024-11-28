import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate("F:/Mobile/firstapp-a74b4-firebase-adminsdk-annkl-11774c25b4.json")

firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

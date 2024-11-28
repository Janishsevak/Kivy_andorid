import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase with your service account key
cred = credentials.Certificate(r'F:\Mobile\firstapp-a74b4-firebase-adminsdk-annkl-e9ff32bc11.json')
firebase_admin.initialize_app(cred)

# Access Firestore database
db = firestore.client()

# Example: Get data from a collection
users_ref = db.collection('users')
docs = users_ref.stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')


from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow CORS for all domains

# Initialize Firebase Admin SDK
firebase_service_account = os.getenv("FIREBASE_SERVICE_ACCOUNT")

if firebase_service_account:
    # Parse the JSON string into a dictionary
    cred_dict = json.loads(firebase_service_account)
    
    # Initialize Firebase using the parsed credentials
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
    
    # Now you can interact with Firebase (e.g., Firestore)
    db = firestore.client()
else:
    print("Firebase credentials not found")

# Collections in Firestore
USERS_COLLECTION = "users"
LOAN_COLLECTION = "loans"

@app.route('/login', methods=['POST'])
def login():
    """Handle user login."""
    data = request.json
    email = data.get('email')
    password = data.get('password')

    try:
        users_ref = db.collection(USERS_COLLECTION).where("email", "==", email).where("password", "==", password).get()
        if users_ref:
            user_data = users_ref[0].to_dict()
            return jsonify({"status": "success", "user": user_data}), 200
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/submit-loan', methods=['POST'])
def submit_loan():
    """Submit a loan application."""
    data = request.json
    try:
        loan_data = {
            "applicant": data.get("applicant"),
            "reason": data.get("reason"),
            "amount": data.get("amount"),
            "guarantors": data.get("guarantors"),
            "approved": False,
            "guarantor_responses": {g: None for g in data.get("guarantors")},
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        db.collection(LOAN_COLLECTION).add(loan_data)
        return jsonify({"status": "success", "message": "Loan submitted successfully"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/guarantor-response', methods=['POST'])
def guarantor_response():
    """Handle guarantor's response to a loan request."""
    data = request.json
    try:
        loan_id = data.get("loan_id")
        approved = data.get("approved")
        current_user_email = data.get("email")

        loan_ref = db.collection(LOAN_COLLECTION).document(loan_id)
        loan_data = loan_ref.get().to_dict()

        if not loan_data:
            return jsonify({"status": "error", "message": "Loan not found"}), 404

        # Update guarantor response
        loan_data["guarantor_responses"][current_user_email] = "approved" if approved else "rejected"

        # Update overall approval status
        if all(resp == "approved" for resp in loan_data["guarantor_responses"].values()):
            loan_data["approved"] = True
        elif any(resp == "rejected" for resp in loan_data["guarantor_responses"].values()):
            loan_data["approved"] = False

        loan_ref.update(loan_data)
        return jsonify({"status": "success", "message": "Response recorded"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/loan-status', methods=['GET'])
def loan_status():
    """Retrieve loan status data."""
    try:
        loans = db.collection(LOAN_COLLECTION).get()
        loan_list = [loan.to_dict() for loan in loans]
        return jsonify({"status": "success", "loans": loan_list}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

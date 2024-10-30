from flask import Flask, request, jsonify, session, redirect, url_for, render_template
from flask_cors import CORS
from google.cloud.firestore_v1.base_query import FieldFilter
import pyrebase
from flask_caching import Cache
import firebase_admin
import  logging
from firebase_admin import credentials, firestore, auth, initialize_app
from config import Config
from datetime import datetime, timedelta
import os
import requests

firebase_config = Config.firebaseConfig

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# Construct the absolute path to the service account key file
base_dir = os.path.dirname(os.path.abspath(__file__))
service_key_path = os.path.normpath(os.path.join(base_dir, 'kingaboranewServiceKey.json'))
# Initialize Firebase Admin SDK

cred = credentials.Certificate(service_key_path)
firebase_admin.initialize_app(cred, {'projectId': 'kingaboravaccinationsystem'})
db = firestore.client()
# Initialize the Flask application
app = Flask(__name__)
cors = CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

# Set a secret key if using sessions or forms
app.secret_key = 'your_secret_key'

# create a user using firebase authenticate
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Get JSON data from the request

    # Extract data from the request
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    nationalID = data.get("nationalID")
    contacts = data.get("contacts")

    # Validate required fields
    if not email or not username or not password or not nationalID or not contacts:
        logging.error("Missing required fields: email, username, password, nationalID, or contacts")
        return jsonify({"error": "Missing email, username, password, nationalID, or contacts"}), 400

    try:
        # Create a new user in Firebase Authentication
        user = auth.create_user_with_email_and_password(email, password)
        user_data = {
            'parentName': username,
            'parentEmailAddress': email,
            'parentNationalID': nationalID,
            'parentPhoneNumber': contacts,
        }

        local_id = user['localId']

        # Add data to Firestore with try-catch for error logging
        try:
            db.collection('parentData').document(local_id).set(user_data)
            logging.info(f"User data successfully stored in Firestore for localId: {local_id}")

        except Exception as firestore_error:
            logging.error(f"Error adding user data to Firestore for localId: {local_id}: {firestore_error}")
            return jsonify({"error": "Error adding data to Firestore"}), 500

        # Redirect URL after successful registration
        redirect_url = f"http://localhost:8080/KingaBora-Vaccination-System/Parent/PARENTPROFILE.html?localId={local_id}"

        return jsonify({"message": "Successfully created the user", "localId": local_id, "redirectUrl": redirect_url}), 201

    except Exception as e:
        logging.error(f"Error creating user: {e}")
        return jsonify({"error": str(e)}), 400  # Return error message
    
# Example route to handle POST requests
@app.route('/email_authenticate', methods=['POST'])
def email_authenticate():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Sign in the user with Firebase
        user = auth.sign_in_with_email_and_password(email, password)
        local_id = user['localId']

        # Example: Fetch user data from Firestore (optional, you can expand based on your use case)
        # user_data = firestore_db.collection('users').document(local_id).get()
        # username = user_data.to_dict().get('username', 'User')

        # Store user information in session (optional)
        session['local_id'] = local_id
        
        # session['username'] = username

        # Return JSON response with redirect URL
        # redirect_url = "http://localhost:8080/KingaBora-Vaccination-System/landingpage/altIndex.html"
        # return jsonify({"message": "Successfully logged in", "localId": local_id, "redirectUrl": redirect_url}), 201
        redirect_url = f"http://localhost:8080/KingaBora-Vaccination-System/Parent/PARENTPROFILE.html?localId={local_id}"
        return jsonify({"message": "Successfully created the user", "localId": local_id, "redirectUrl": redirect_url}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/childDetails', methods=['GET'])
def ChildDetails():
    try:
        # Get the correct query parameter
        parentNationalID = request.args.get("ParentNationalID")
        
        # Query Firestore correctly
        doc_ref = db.collection('childData')   #this is the collection of the children (table in sql)
        query = doc_ref.where("ParentNationalID", "==", parentNationalID)  # Correct usage without FieldFilter , this filters
        docs = query.stream()
        
        document_list = [
         {"id": doc.id, **doc.to_dict()} for doc in docs
        ]  # Unpack document data and add ID

        if document_list:
          logging.info(f"Children found: {document_list}")
          return jsonify({"message": "Children found", "childNames": document_list}), 200
        else:
          logging.info("No children found.")
          return jsonify({"error": "No children found for the given ParentNationalID"}), 404

    except Exception as e:
       logging.error(f"Error fetching child details: {str(e)}")
       return jsonify({"errors": str(e)}), 500



@app.route('/parentDetails', methods=['GET'])
def parentDetails():
    try:
        parentlocalId = request.args.get("ParentlocalID")  # Get the localId from the query parameters
        doc_ref = db.collection('parentData').document(parentlocalId)
        doc = doc_ref.get()

        data = doc.to_dict()
       
        if data:
            logging.info(f"Children found: {data}")
            return jsonify({"message": "Parent found", "parentDetails": data}), 200  # Ensure the key matches what the frontend expects
        else:
            logging.info("No Parent found.")
            return jsonify({"error": "No parent found for the given Parent ID"}), 404

    except Exception as e:
        logging.error(f"Error fetching child details: {str(e)}")
        return jsonify({"errors": str(e)}), 500
    
@app.route('/vaccinationupdate')
def vaccinationupdate():
    try:
        child_local_id = request.args.get("localId")  # Get the localId from the query parameters

        doc_ref=db.collection('VaccinationHistory')
        query=doc_ref.where(filter=FieldFilter("Child_local_ID","==",child_local_id))
        docs=query.stream()
        document_list=[]
        for doc in docs:
            data=doc.to_dict()
            document_list.append(data)
       
        if data:
            logging.info(f"Vaccination file: {document_list}")
            return jsonify({"message": "Vaccination file", "Vaccination": document_list}), 200
        else:
            logging.info("No children found.")
            return jsonify({"error": "No vaccine found for the given ParentName"}), 404

       

    except Exception as e:
        logging.error(f"Error fetching child details: {str(e)}")
        return jsonify({"errors": str(e)}), 500    

@app.route('/Vaccines')
def Vaccines():
  try:
    period = request.args.get("period")  # Get the period from the query parameters
    logging.info(f"Searching for period: {period}")  # Debug logging

    doc_ref = db.collection('DrugInventory')
    # This is correct now since DrugPeriod is an array
    query = doc_ref.where('DrugPeriod', 'array_contains', period)

    docs = query.stream()
    document_list = []
    for doc in docs:
      data = doc.to_dict()
      logging.info(f"Found document: {data}")  # Debug logging
      drug_name = data.get('DrugName')
      if drug_name:
        document_list.append(drug_name)

    if document_list:
      logging.info(f"Drugs found with period {period}: {document_list}")
      return jsonify({"message": "Drug list", "Drugs": document_list}), 200
    else:
      logging.info(f"No drugs found with period {period}.")
      return jsonify({"error": "No drugs found for the given period"}), 404

  except Exception as e:
    logging.error(f"Error fetching drugs: {str(e)}")
    import traceback
    logging.error(traceback.format_exc())  # Add full stack trace
    return jsonify({"error": str(e)}), 500

@app.route('/storevaccinereceipt', methods=['POST'])
def storevaccinereceipt():
    data = request.get_json()

    # Extract data from the request
    childName = data.get("ChildName")
    child_local_ID = data.get("Child_local_ID")
    DateofVaccination = data.get("DateofVaccination")
    NextVisit = data.get("NextVisit")
    NurseName = data.get("NurseName")
    nextscheduletime = data.get("nextscheduletime")
    vaccinesIssued = data.get("vaccinesIssued")

    # Create a new user in Firestore
    vaccine_data = {
        'childName': childName,
        'child_local_ID': child_local_ID,
        'DateofVaccination': DateofVaccination,
        'NextVisit': NextVisit,
        'NurseName': NurseName,
        'nextscheduletime': nextscheduletime,
        'vaccinesIssued': vaccinesIssued
    }

    try:
        doc_ref = db.collection('VaccinationHistory').add(vaccine_data)
        doc_id = doc_ref.id  # Get the generated document ID

        # Redirect URL after successful registration
        redirect_url = f"http://localhost:8080/KingaBora-Vaccination-System/Parent/PARENTPROFILE.html?localId={doc_id}"

        return jsonify({"message": "Successfully created the user", "localId": doc_id, "redirectUrl": redirect_url}), 201

    except Exception as firestore_error:
        logging.error(f"Error adding user data to Firestore: {firestore_error}")
        return jsonify({"error": "Error adding data to Firestore"}), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Running on localhost:5000

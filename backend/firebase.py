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
from collections import defaultdict
import os
import secrets
import string
import pytz
import requests
from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth.transport.requests import Request


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
# app = Flask(__name__)
# cors = CORS(app)
# # Ensure CORS is configured correctly
# CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})
# CORS(app, origins="http://localhost")



app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Set a secret key if using sessions or forms
app.secret_key = 'your_secret_key'

# create a user using firebase authenticate

# Initialize Firestore DB (Ensure Firebase Admin SDK is initialized properly)
db = firestore.client()



@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Get JSON data from the request

    # Extract data from the request
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    nationalID = data.get("nationalID")
    contacts = data.get("contacts")
    is_google_signup = data.get("isGoogleSignup", False)  # Check if it's Google signup

    # Validate required fields (skip password validation for Google signup)
    if not email or not username or not nationalID or not contacts:
        logging.error("Missing required fields: email, username, nationalID, or contacts")
        return jsonify({"error": "Missing email, username, nationalID, or contacts"}), 400

    if not is_google_signup and not password:
        logging.error("Missing required password for manual signup")
        return jsonify({"error": "Missing password"}), 400

    try:
        if is_google_signup:
            # For Google sign-up, skip password and handle Google-specific logic
            user = auth.create_user_with_email_and_password(email, 'temporaryPassword')  # Assigning a temporary password
        else:
            # For manual sign-up, create a user with provided password
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

        # Check which role the user has by searching in Firestore collections
        firestore_db = db  # Assuming db is your Firestore client
        redirect_url = None

        # Check administrator collection
        admin_doc = firestore_db.collection('administratorData').document(local_id).get()
        if admin_doc.exists:
            redirect_url = "http://localhost:8080/KingaBora-Vaccination-System/Admin/admin_dashboard.html"

        # Check parent collection
        if redirect_url is None:
            parent_doc = firestore_db.collection('parentData').document(local_id).get()
            if parent_doc.exists:
                redirect_url = f"http://localhost:8080/KingaBora-Vaccination-System/Parent/PARENTPROFILE.html?localId={local_id}"

        # Check nurse collection
        if redirect_url is None:
            nurse_doc = firestore_db.collection('nurseData').document(local_id).get()
            if nurse_doc.exists:
                redirect_url = f"http://localhost:8080/KingaBora-Vaccination-System/nurse/nurse_dashboard.html?localId={local_id}"

        # If no role found, raise an error
        if redirect_url is None:
            return jsonify({"error": "User role not found in any collection"}), 404

        # Store user information in session (optional)
        session['local_id'] = local_id

        # Return JSON response with appropriate redirect URL
        return jsonify({"message": "Successfully logged in", "localId": local_id, "redirectUrl": redirect_url}), 201

    except Exception as e:
        return jsonify({"error":str(e)}),400




@app.route('/google_authenticate', methods=['POST'])
def google_authenticate():
    try:
        token = request.json.get('token')
        if not token:
            return jsonify({'error': 'Token is missing'}), 400

        # Verify the Google OAuth2 token
        idinfo = id_token.verify_oauth2_token(token, Request())

        # Extract user data
        user_id = idinfo['sub']
        email = idinfo.get('email')
        name = idinfo.get('name')

        # Store or update user data in Firestore
        user_data = {
            'parentName': name,
            'parentEmailAddress': email,
        }
        db.collection('parentData').document(user_id).set(user_data, merge=True)

        # Redirect URL
        redirect_url = f"http://localhost:8080/KingaBora-Vaccination-System/Parent/PARENTPROFILE.html?localId={user_id}"

        return jsonify({'localId': user_id, 'redirectUrl': redirect_url}), 200

    except ValueError as e:
        logging.error(f"Google authentication error: {str(e)}")
        return jsonify({'error': 'Invalid token', 'details': str(e)}), 400
    except Exception as e:
        logging.error(f"Server error: {str(e)}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500



@app.after_request
def add_headers(response):
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    return response

@app.route('/google_authenticate', methods=['OPTIONS'])
def google_authenticate_options():
    response = app.make_response('')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.route('/parentDetails', methods=['GET'])
def parentDetails():
    try:
        parentlocalId = request.args.get("ParentlocalID")
        if not parentlocalId:
            return jsonify({"error": "No ParentlocalID provided"}), 400

        doc_ref = db.collection('parentData').document(parentlocalId)
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            # Exact field names from your Firebase
            return jsonify({
                "message": "Parent found", 
                "parentDetails": {
                    "parentName": data.get('parentName'),
                    "parentEmailAddress": data.get('parentEmailAddress'),
                    "parentPhoneNumber": data.get('parentPhoneNumber'),
                    "parentNationalID": data.get('parentNationalID')
                }
            }), 200
        else:
            return jsonify({"error": "No parent found for the given ID"}), 404

    except Exception as e:
        logging.error(f"Error fetching parent details: {str(e)}")
        return jsonify({"error": str(e)}), 500
    

def parse_date(date_string):
    """Try multiple date formats"""
    formats = [
        '%B %d, %Y at %I:%M:%S %p GMT+3',
        '%B %d, %Y at %I:%M:%S %p',
        '%B %d, %Y at %I:%M:%S %p GMT',
        '%B %d, %Y',
        '%Y-%m-%d',
        # Add more formats if needed
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    # If no format works, log the problematic string and return None
    logging.error(f"Could not parse date string: {date_string}")
    return None    
    logging.error(f"Error fetching child details: {str(e)}")
    return jsonify({"errors": str(e)}), 500
    

@app.route('/GetUsersChart', methods=['GET'])
def GetUsersChart():
    try:
        # References to each collection
        parent_ref = db.collection('parentData')
        child_ref = db.collection('childData')
        nurse_ref = db.collection('nurseData')
        admin_ref = db.collection('administratorData')

        # Get all documents in each collection and count them
        parent_docs = parent_ref.stream()
        child_docs = child_ref.stream()
        nurse_docs = nurse_ref.stream()
        admin_docs = admin_ref.stream()

        # Count documents in each collection
        parent_count = sum(1 for _ in parent_docs)
        child_count = sum(1 for _ in child_docs)
        nurse_count = sum(1 for _ in nurse_docs)
        admin_count = sum(1 for _ in admin_docs)

        # Log the counts for debugging purposes
        logging.info(f"Total Parents: {parent_count}, Children: {child_count}, Nurses: {nurse_count}, Administrators: {admin_count}")

        # Return the counts in the JSON response
        return jsonify({
            "message": "Document counts retrieved successfully",
            "parentCount": parent_count,
            "childCount": child_count,
            "nurseCount": nurse_count,
            "adminCount": admin_count
        }), 200

    except Exception as e:
        logging.error(f"Error fetching document counts: {str(e)}")
        return jsonify({"errors": str(e)}), 500


@app.route('/vaccinationupdate')
def vaccinationupdate():
    try:
        child_local_id = request.args.get("localId")
        
       

        doc_ref=db.collection('VaccinationHistory')
        query=doc_ref.where(filter=FieldFilter("child_local_ID","==",child_local_id))
        docs=query.stream()
        document_list=[]
        for doc in docs:
            data = doc.to_dict()
            document_list.append(data)

        if document_list:
            # Sort documents, putting any with unparseable dates at the end
            try:
                document_list.sort(
                   key=lambda x: datetime.strptime(
                        x['DateOfVaccination'], "%B %d, %Y at %I:%M:%S %p GMT%z"
                    ),
                    reverse=True 
                )
            except Exception as sort_error:
                logging.error(f"Sorting error: {sort_error}")
                # Continue with unsorted list
            
            return jsonify({
                "message": "Vaccination file",
                "Vaccination": document_list
            }), 200
        else:
            logging.info("No children found.")
            return jsonify({
                "error": "No vaccine found for the given ParentName"
            }), 404

    except Exception as e:
        logging.error(f"Error fetching child details: {str(e)}")
        return jsonify({"errors": str(e)}), 500

@app.route('/Vaccines', methods=['GET'])
def Vaccines():
    try:
        period = request.args.get("period")  # Get the period from the query parameters
        logging.info(f"Searching for period: {period}")  # Debug logging

        doc_ref = db.collection('DrugInventory')
        query = doc_ref.where('DrugPeriod', 'array_contains', period)
        docs = query.stream()

        # Create a list of dictionaries with DrugName as the key and DrugPrice as the value
        document_list = {}
        for doc in docs:
            data = doc.to_dict()
            logging.info(f"Found document: {data}")  # Debug logging
            
            drug_name = data.get('DrugName')
            drug_price = data.get('DrugPrice')
            
            # Only add if both DrugName and DrugPrice are available
            if drug_name and drug_price is not None:
                document_list[drug_name] = drug_price

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

## drugs 1
@app.route('/drugAnalytics', methods=['POST'])
def drugAnalytics():
    data = request.get_json()
    selected_drugs = data.get("SelectedDrug", [])
    druglocalid=""

    try:
        for drug_name in selected_drugs:
            # Query Firestore for each drug in the DrugInventory collection
            drug_query = db.collection('DrugInventory').where('DrugName', '==', drug_name).stream()
           
            # For each document that matches the drug name, get the price
             
            utc_now = datetime.utcnow()

           # Format the date and time
            formatted_date = utc_now.strftime("%a %b %d %Y %H:%M:%S GMT%z")

           # Adjust the time zone to GMT+3
            gmt_offset = "+0300"
            east_africa_time = formatted_date.replace("GMT", f"GMT{gmt_offset} (East Africa Time)") 
            for doc in drug_query:
                drug_data = doc.to_dict()
                price = drug_data.get('DrugPrice', 0)
                drugquantity=drug_data.get('DrugQuantity',0)
                drugquantity=drugquantity-1
                
                if drugquantity > 0:
                    new_quantity = drugquantity - 1
                    
                    # Update the DrugQuantity in Firestore
                    doc.reference.update({"DrugQuantity": new_quantity})
                    
                    # Log the drug administration in DrugAdministered collection
                    drug_admin_data = {
                        'Quantity': 1,
                        'DrugName': drug_name,
                        'DateOfAdministration': east_africa_time,
                        'Price': price,
                    }
                    doc_ref = db.collection('DrugAdministered').add(drug_admin_data)
                    druglocalid = doc_ref[1].id




                
               

        return jsonify({"message": "Prices retrieved successfully", "localid":druglocalid}), 200
    
    except Exception as firestore_error:
        logging.error(f"Error retrieving drug prices from Firestore: {firestore_error}")
        return jsonify({"error": "Error retrieving drug prices"}), 500
    
@app.route('/DrugAdministered', methods=['POST'])
def DrugAdministered():
    data = request.get_json()
    selected_drugs = data.get("SelectedDrug", [])
    total_price = 0
    druglocalid=""

    try:
        for drug_name in selected_drugs:
            # Query Firestore for each drug in the DrugInventory collection
            drug_query = db.collection('DrugInventory').where('DrugName', '==', drug_name).stream()
           
            # For each document that matches the drug name, get the price
             
            utc_now = datetime.utcnow()

           # Format the date and time
            formatted_date = utc_now.strftime("%a %b %d %Y %H:%M:%S GMT%z")

           # Adjust the time zone to GMT+3
            gmt_offset = "+0300"
            east_africa_time = formatted_date.replace("GMT", f"GMT{gmt_offset} (East Africa Time)") 
            for doc in drug_query:
                drug_data = doc.to_dict()
                price = drug_data.get('DrugPrice', 0)
                drug_data = {
                   'Quantity': 1,
                   'DrugName': drug_name,
                   'DateOfAdministration': east_africa_time,
                   'Price': price,
                   }



                
                total_price += price

        return jsonify({"message": "Prices retrieved successfully", "total_price": total_price, "localid":druglocalid}), 200

    except Exception as firestore_error:
        logging.error(f"Error retrieving drug prices from Firestore: {firestore_error}")
        return jsonify({"error": "Error retrieving drug prices"}), 500
    
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
    height = data.get("height")
    parentEmailAddress = data.get("parentEmailAddress")
    weight=data.get("weight")
    height = data.get("height")
    weight=data.get("weight")

    # Create a new user in Firestore
    vaccine_data = {
        'childName': childName,
        'child_local_ID': child_local_ID,
        'DateofVaccination': DateofVaccination,
        'NextVisit': NextVisit,
        'NurseName': NurseName,
        'nextscheduletime': nextscheduletime,
        'vaccinesIssued': vaccinesIssued,
        'weight':weight,
        'height':height,
        'parentEmailAddress':parentEmailAddress,
        'vaccinesIssued': vaccinesIssued,
        'weight':weight,
        'height':height
    }

    try:
        doc_ref = db.collection('VaccinationHistory').add(vaccine_data)
        doc_id = doc_ref.id  # Get the generated document ID

        # Redirect URL after successful registration
        redirect_url = f"http://localhost:8080/KingaBora-Vaccination-System/nurse/nurse_dashboard.html"

        return jsonify({"message": "Successfully created the user", "localId": doc_id, "redirectUrl": redirect_url}), 201

    except Exception as firestore_error:
        logging.error(f"Error adding user data to Firestore: {firestore_error}")
        return jsonify({"error": "Error adding data to Firestore"}), 500



   ##reg nurse 1
   #  
@app.route('/registerNurse', methods=['POST'])
def registerNurse():
    data = request.get_json()  # Get JSON data from the request

# fullname,
#               email,
#               phonenumber,
#               password,
#               gender
              
    # Extract data from the request
    fullname = data.get("fullname")
    email = data.get("email")
    phonenumber = data.get("phonenumber")
    password = data.get("password")
    gender = data.get("gender")
    nationalID = data.get("nationalID")


    # Validate required fields
    if not email or not fullname or not password or not phonenumber or not gender or not  nationalID:
        logging.error("Missing required fields: email, username, password, nationalID, or contacts")
        return jsonify({"error": "Missing email, username, password, nationalID, or contacts"}), 400

    try:
        # Create a new user in Firebase Authentication
        user = auth.create_user_with_email_and_password(email, password)
        nurse_data = {
            'nurseName': fullname,
            'nurseEmailAddress': email,
            'nursephonenumber': phonenumber,
            'nurseGender': gender,
            'nurseNationalID': nationalID
        }

        local_id = user['localId']

        # Add data to Firestore with try-catch for error logging
        try:
            db.collection('nurseData').document(local_id).set(nurse_data)
            logging.info(f"User data successfully stored in Firestore for localId: {local_id}")

        except Exception as firestore_error:
            logging.error(f"Error adding user data to Firestore for localId: {local_id}: {firestore_error}")
            return jsonify({"error": "Error adding data to Firestore"}), 500

        # Redirect URL after successful registration
        redirect_url = f"http://localhost:8080/KingaBora-Vaccination-System/Admin/admin_dashboard.html?localId={local_id}"

        return jsonify({"message": "Successfully created the user", "localId": local_id, "redirectUrl": redirect_url}), 201

    except Exception as e:
        logging.error(f"Error creating user: {e}")
        return jsonify({"error": str(e)}), 400  # Return error message   
    
@app.route('/getParentDetails', methods=['GET'])
def getParentDetails():
    try:
        # Get the 'localID' query parameter
        child_localID = request.args.get("localID")

        # Check if localID is provided
        if not child_localID:
            return jsonify({"error": "Missing 'localID' parameter"}), 400

        # Directly reference the document by its ID
        doc_ref = db.collection('childData').document(child_localID)
        doc = doc_ref.get()

        # Check if the document exists
        if doc.exists:
            # Retrieve 'emailaddress' and 'parentName' from the document
            doc_data = doc.to_dict()
            response_data = {
                "emailaddress": doc_data.get("emailaddress"),
                "parentName": doc_data.get("ParentName")
            }
            return jsonify({"message": "Parent details found", "data": response_data}), 200
        else:
            return jsonify({"error": "No document found for the given 'localID'"}), 404

    except Exception as e:
        logging.error(f"Error fetching parent details: {str(e)}")
        return jsonify({"error": str(e)}), 500

    # this is sections for admin data
    
    
    
 #this is the nurse profile
 # 


@app.route('/getVaccinationDueList', methods=['GET'])
def getVaccinationDueList():
    try:
        # Get today's date, tomorrow's, and the day after tomorrow's dates in the correct format
        tz = pytz.FixedOffset(3 * 60)  # GMT+3
        today = datetime.now(tz).date()  # Today
        tomorrow = today + timedelta(days=1)  # Tomorrow
        day_after_tomorrow = today + timedelta(days=2)  # Day after tomorrow
        
        # Query Firestore for all documents in 'VaccinationHistory'
        doc_ref = db.collection('VaccinationHistory')
        docs = doc_ref.stream()

        # Prepare response data
        response_data = []
        for doc in docs:
            doc_data = doc.to_dict()
            next_visit_str = doc_data.get("NextVisit")  # Get the NextVisit string
            
            if next_visit_str:
                # Remove the "GMT+3" part and convert to datetime (ignoring time)
                next_visit_no_tz = next_visit_str.rsplit(" GMT", 1)[0]
                next_visit_datetime = datetime.strptime(next_visit_no_tz, "%B %d, %Y at %I:%M:%S %p")
                
                # Convert the NextVisit datetime to the same timezone (GMT+3) to make the comparison
                localized_next_visit = tz.localize(next_visit_datetime).date()

                # Check if the NextVisit date is today, tomorrow, or the day after tomorrow
                if localized_next_visit in [today, tomorrow, day_after_tomorrow]:
                    response_data.append({
                        "childName": doc_data.get("childName"),
                        "DateofVaccination": doc_data.get("DateofVaccination"),
                        "parentEmailAddress": doc_data.get("parentEmailAddress"),
                        "NextVisit": next_visit_str,
                    })

        # Return results if any found
        if response_data:
            return jsonify({"message": "Vaccination details found", "data": response_data}), 200
        else:
            return jsonify({"error": "No vaccination details match the specified dates"}), 404

    except Exception as e:
        logging.error(f"Error fetching vaccination details: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/getEmailList', methods=['GET'])
def get_email_list():
    try:
        # Set the timezone (Africa/Nairobi)
        timezone = pytz.timezone('Africa/Nairobi')

        # Get today's date and add 1 day for reminder
        today = datetime.now(timezone).date()
        reminder_date = today + timedelta(days=7)  # Add 1 day to today's date

        # Format the reminder date in "Nov 24, 2024" format (same format as in the database)
        formatted_reminder_date = reminder_date.strftime("%b %d, %Y")

        # Retrieve all documents in the VaccinationHistory collection
        docs = db.collection('VaccinationHistory').stream() if db else []

        result_docs = []
        for doc in docs:
            data = doc.to_dict()
            next_visit_str = data.get("NextVisit")
            vaccines_issued = data.get("vaccinesIssued", 0)
            
            if next_visit_str:
                # Parse and clean the NextVisit date from the database (remove time and timezone)
                try:
                    # Split the string by spaces and get the correct parts (Month, Day, Year)
                    next_visit_parts = next_visit_str.split(' ')[1:4]  # [1:4] will give Month, Day, Year
                    cleaned_next_visit_str = " ".join(next_visit_parts)  # Reassemble as "Nov 18, 2024"
                    
                    # Now compare the cleaned NextVisit with the reminder date
                    if cleaned_next_visit_str == formatted_reminder_date:
                        result_docs.append({
                            "NextVisit": cleaned_next_visit_str,
                            "parentEmailAddress": data.get("parentEmailAddress"),
                            "childName": data.get("childName"),
                            "vaccinesIssued": vaccines_issued 
                        })
                except ValueError as e:
                    logging.error(f"Error parsing NextVisit date: {e}")

        # Return the records where the NextVisit date matches the reminder date
        return jsonify({"data": result_docs})

    except Exception as e:
        logging.error(f"Error fetching child data: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/ViewActivities', methods=['GET'])
def ViewActivities():
    try:
        # Get the correct query parameter
        # In this case, we don't need any query parameters, we just want to retrieve the 4 most recent documents

        # Query Firestore correctly
        doc_ref = db.collection('VaccinationHistory')
        # Order the results by the creation timestamp in descending order to get the most recent documents first
        query = doc_ref.order_by('DateofVaccination', direction=firestore.Query.DESCENDING)
        # Limit the results to 2 documents
        docs = query.limit(2).stream()

        document_list = [
            {"id": doc.id, **doc.to_dict()} for doc in docs
        ]  # Unpack document data and add ID

        if document_list:
            logging.info(f"Children found: {document_list}")
            return jsonify({"message": "Children found", "childNames": document_list}), 200
        else:
            logging.info("No children found.")
            return jsonify({"error": "No activities found"}), 404

    except Exception as e:
        logging.error(f"Error fetching child details: {str(e)}")
        return jsonify({"errors": str(e)}), 500
        
        
@app.route('/getNurseProfileByLocalId', methods=['GET'])
def get_nurse_profile_by_local_id():
    local_id = request.args.get('localId')  # Retrieve localId from query parameters

    if not local_id:
        return jsonify({"error": "Missing localId parameter"}), 400

    try:
        # Query the database to get the nurse's profile by localId
        # Assuming you're using Firestore or a similar NoSQL database where each document has a localId
        nurse_collection = db.collection('nurseData')  # Replace with your actual collection
        nurse_document = nurse_collection.document(local_id).get()

        if nurse_document.exists:
            nurse_data = nurse_document.to_dict()  # Convert the document to a dictionary
            return jsonify({
                "data": [{
                    "nurseName": nurse_data.get("nurseName", "N/A"),
                    "nurseNationalID": nurse_data.get("nurseNationalID", "N/A"),
                    "nursePhoneNumber": nurse_data.get("nursephonenumber", "N/A"),
                    "nurseGender": nurse_data.get("nurseGender", "N/A"),
                    "nurseEmail": nurse_data.get("nurseEmailAddress", "N/A")
                }]}), 200
        else:
            return jsonify({"error": "No nurse found for the provided localId"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/getEmailList2', methods=['GET'])
def getEmailList2():
    try:
        # Get the 'NextVisit' query parameter
        NextVisit = request.args.get("NextVisit")
        
        # Check if NextVisit is provided
        if not NextVisit:
            return jsonify({"error": "Missing 'NextVisit' parameter"}), 400

        # Parse the provided NextVisit parameter into a datetime object (without timezone)
        NextVisit_no_tz = NextVisit.rsplit(" GMT", 1)[0]
        visit_datetime = datetime.strptime(NextVisit_no_tz, "%B %d, %Y at %I:%M:%S %p")
        
        # Manually add timezone (GMT+3) and convert to UTC
        input_tz = pytz.FixedOffset(3 * 60)  # GMT+3 is 3 hours ahead of UTC
        localized_datetime = input_tz.localize(visit_datetime)
        utc_datetime = localized_datetime.astimezone(pytz.UTC)

        # Query Firestore for all documents in 'VaccinationHistory'
        doc_ref = db.collection('VaccinationHistory')
        docs = doc_ref.stream()

        # Prepare response data by filtering based on NextVisit
        response_data = []
        for doc in docs:
            doc_data = doc.to_dict()
            
            # Convert each document's NextVisit string to a datetime for comparison
            doc_next_visit = doc_data.get("NextVisit")

            if doc_next_visit:
                doc_next_visit_no_tz = doc_next_visit.rsplit(" GMT", 1)[0]
                doc_visit_datetime = datetime.strptime(doc_next_visit_no_tz, "%B %d, %Y at %I:%M:%S %p")
                
                # Localize and convert document datetime to UTC
                doc_localized_datetime = input_tz.localize(doc_visit_datetime)
                doc_utc_datetime = doc_localized_datetime.astimezone(pytz.UTC)
                
                # Compare document's UTC NextVisit with the provided UTC NextVisit
                if doc_utc_datetime <= utc_datetime:
                    # Handle vaccinesIssued array
                    vaccines_issued = doc_data.get("vaccinesIssued", [])
                    
                    # Check if vaccinesIssued is a list
                    if not isinstance(vaccines_issued, list):
                        vaccines_issued = []

                    # Add the filtered document data to the response
                    response_data.append({
                        "childName": doc_data.get("childName"),
                        "DateofVaccination": doc_data.get("DateofVaccination"),
                        "parentEmailAddress": doc_data.get("parentEmailAddress"),
                        "NextVisit": doc_data.get("NextVisit"),
                        "vaccinesIssued": vaccines_issued
                    })
                    
                    # Stop after collecting 3 records
                    if len(response_data) == 2:
                        break
        
        # Return results or 404 if none found
        if response_data:
            return jsonify({"message": "Parent details found", "data": response_data}), 200
        else:
            return jsonify({"error": "No documents found for the given 'NextVisit'"}), 404

    except Exception as e:
        logging.error(f"Error fetching parent details: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
#child data
@app.route('/childDetails', methods=['GET'])
def ChildDetails():
    try:
        parentNationalID = request.args.get("ParentNationalID")
        if not parentNationalID:
            return jsonify({"error": "No ParentNationalID provided"}), 400

        doc_ref = db.collection('childData')
        query = doc_ref.where("ParentNationalID", "==", parentNationalID)
        docs = query.stream()
        
        document_list = [{"id": doc.id, **doc.to_dict()} for doc in docs]

        if document_list:
            return jsonify({"message": "Children found", "childNames": document_list}), 200
        else:
            return jsonify({"error": "No children found for this parent"}), 404

    except Exception as e:
        logging.error(f"Error fetching child details: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
#fetchChildByLocalId    
@app.route('/fetchChildByLocalId', methods=['GET'])
def fetchChildByLocalId():
    try:
        local_id = request.args.get("localId")  # Get the localId from the query parameters
        if not local_id:
            return jsonify({"error": "No localId provided"}), 400

        # Reference the child document using the localId
        doc_ref = db.collection('childData').document(local_id)
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            return jsonify({
                "message": "Child found",
                "BirthCertificateID": data.get('BirthCertificateID'),
                "ChildName": data.get('ChildName'),
                "DateOfBirth": data.get('DateOfBirth'),
                "Gender": data.get('Gender'),
                "ParentName": data.get('ParentName'),
                "ParentNationalID": data.get('ParentNationalID'),
                "emailaddress": data.get('emailaddress'),
                "height": data.get('height'),
                "weight": data.get('weight')
            }), 200
        else:
            return jsonify({"error": "No child found for the given localId"}), 404

    except Exception as e:
        logging.error(f"Error fetching child details: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
    
@app.route('/addChild', methods=['POST'])
def addChild():
    try:
        data = request.get_json()
        
        nextscheduletime = "At Birth"
        # Create child data document
        child_data = {
            'BirthCertificateID': data.get('BirthCertificateID'),
            'ChildName': data.get('ChildName'),
            'DateOfBirth': data.get('DOB'),
            'Gender': data.get('Gender'),
            'ParentName': data.get('ParentName'),
            'ParentNationalID': data.get('ParentNationalID'),
            'emailaddress': data.get('parentEmailAddress'),
            # 'Weight': data.get('weight'),
            # 'Height': data.get('height')
        }

        # Add document to 'childData' collection and get the document reference
        doc_ref = db.collection('childData').add(child_data)
        
        doc_id = doc_ref[1].id  # Retrieve the document ID directly
        vaccination_data={
            'ChildGender': data.get('Gender'),
            'childName': data.get('ChildName'),
            'DateOfVaccination': data.get('DOB'),
            'NextVisit': data.get('DOB'),
            'nextscheduletime':"At Birth",            
            'NurseName': "Faith",
            'child_local_ID':doc_id,
            'parentEmailAddress': data.get('parentEmailAddress'),
            'vaccinesIssued': [],
            # 'Weight': data.get('weight'),
            # 'Height': data.get('height')
            
        }
        doc_reference = db.collection('VaccinationHistory').add(vaccination_data)

        # Construct the redirect URL with the document ID and schedule time
        redirect_url = f"http://localhost:8080/KingaBora-Vaccination-System/nurse/vaccinationpage.html?localId={doc_id}"
        
        return jsonify({
            "message": "Successfully created the user",
            "localId": doc_id,
            "redirectUrl": redirect_url
       
        }), 201

    except Exception as e:
        logging.error(f"Error adding child: {str(e)}")
        return jsonify({"error": str(e)}), 500



# Run the Flask application


# from today (kangskii)



@app.route('/updateParentProfile', methods=['PUT'])
def updateParentProfile():
   try:
       local_id = request.args.get('localId')
       if not local_id:
           return jsonify({"error": "Missing localId parameter"}), 400

       data = request.get_json()
       updated_data = {
           'parentName': data.get('parentName'),
           'parentEmailAddress': data.get('parentEmailAddress'),
           'parentPhoneNumber': data.get('parentPhoneNumber'),
           'parentNationalID': data.get('parentNationalID'),
       }

       # Update the Firestore document
       db.collection('parentData').document(local_id).update(updated_data)
       logging.info(f"Profile updated successfully for localId: {local_id}")

       return jsonify({"message": "Profile updated successfully"}), 200

   except Exception as e:
       logging.error(f"Error updating profile: {str(e)}")
       return jsonify({"error": str(e)}), 500   
    
@app.route('/ViewActivities2', methods=['GET'])
def ViewActivities2():
    try:
        # Reference to the VaccinationHistory collection
        doc_ref = db.collection('VaccinationHistory')
        
        # Order the results by DateofVaccination in descending order
        query = doc_ref.order_by('DateofVaccination', direction=firestore.Query.DESCENDING)
        
        # Fetch all documents in the collection without a limit
        docs = query.stream()

        # Build a list of all document data with document IDs
        document_list = [{"id": doc.id, **doc.to_dict()} for doc in docs]

        if document_list:
            logging.info(f"Activities found: {document_list}")
            return jsonify({"message": "Activities found", "childNames": document_list}), 200
        else:
            logging.info("No activities found.")
            return jsonify({"error": "No activities found"}), 404

    except Exception as e:
        logging.error(f"Error fetching activity details: {str(e)}")
        return jsonify({"errors": str(e)}), 500
    

@app.route('/drug_inventory', methods=['GET'])
def get_drug_inventory():
    try:
        drugs_ref = db.collection('DrugInventory')
        drugs = drugs_ref.stream()
        
        # Collect only required fields
        drug_list = [{'DrugName': drug.to_dict().get('DrugName'), 
                      'DrugQuantity': drug.to_dict().get('DrugQuantity')} 
                      for drug in drugs]
        
        return jsonify(drug_list), 200

    except Exception as e:
        logging.error(f"Error fetching DrugInventory: {e}")
        return jsonify({"error": "An error occurred while fetching DrugInventory"}), 500
@app.route('/drug_sales', methods=['GET'])
def get_drug_sales():
    try:
        # Fetch data from the DrugsAdministered collection
        drugs_ref = db.collection('DrugsAdministered')
        drugs = drugs_ref.stream()

        # Dictionary to accumulate sales data
        sales_data = {}

        # Loop through each document in the collection
        for drug in drugs:
            drug_data = drug.to_dict()
            drug_name = drug_data.get('DrugName')
            price = drug_data.get('Price', 0)
            quantity = drug_data.get('Quantity', 0)

            # Calculate revenue for this instance of the drug
            revenue = price * quantity

            # Accumulate the revenue and quantity for each drug
            if drug_name in sales_data:
                sales_data[drug_name]['total_revenue'] += revenue
                sales_data[drug_name]['total_quantity'] += quantity
            else:
                sales_data[drug_name] = {
                    'total_revenue': revenue,
                    'total_quantity': quantity,
                    'price_per_unit': price  # Save the price for later profit calculation
                }

        # Define cost prices (in KSH) for each drug type (hardcoded here for simplicity)
        cost_prices = {
            'MMR': 200,
            'DTP': 300,
            'Polio': 150,
            'Hepatitis B': 500,
            'COVID-19': 250
        }

        # Calculate profits for each drug
        for drug_name, data in sales_data.items():
            cost_price = cost_prices.get(drug_name, 0)
            data['profit'] = data['total_revenue'] - (data['total_quantity'] * cost_price)

        return jsonify(sales_data), 200

    except Exception as e:
        logging.error(f"Error fetching drug sales data: {e}")
        return jsonify({"error": "An error occurred while fetching drug sales data"}), 500
    

def parse_date(date_str):
    try:
        # Strip off the timezone and parse the core part of the date
        core_date_str = date_str.split(" GMT")[0]
        return datetime.strptime(core_date_str, '%a %b %d %Y %H:%M:%S')
    except ValueError as e:
        print(f"Date parsing error for {date_str}: {e}")
        return None

@app.route('/getChildDataLimited', methods=['GET'])
def getChildDataLimited():
    try:
        # Query Firestore for all documents in 'childData'
        doc_ref = db.collection('childData')
        docs = doc_ref.stream()

        # Prepare response data (limit to 3 records)
        response_data = []
        for doc in docs:
            if doc.exists:  # Check if the document exists
                doc_data = doc.to_dict()

                # Extract necessary fields from the document
                child_info = {
                    "BirthCertificateID": doc_data.get("BirthCertificateID"),
                    "ChildName": doc_data.get("ChildName"),
                    "DateOfBirth": doc_data.get("DateOfBirth"),
                    "ParentName": doc_data.get("ParentName"),
                    "childId": doc.id  # To use as a link for the "View Child" button
                }
                response_data.append(child_info)

                # Limit to 3 records
                if len(response_data) == 3:
                    break

        # Return the data in JSON format
        if response_data:
            return jsonify({"message": "Child data found", "data": response_data}), 200
        else:
            return jsonify({"error": "No child data found"}), 404

    except Exception as e:
        logging.error(f"Error fetching limited child data: {str(e)}")
        return jsonify({"error": str(e)}), 500
# Endpoint to retrieve and count vaccines administered each day in the past week
@app.route('/drug_sales2', methods=['GET'])
def drug_sales2():
    try:
        # Get the current date and time, and calculate the start date (7 days ago)
        today = datetime.now()
        start_date = today - timedelta(days=7)

        # Query the database for DrugsAdministered entries
        drugs_administered_ref = db.collection('DrugsAdministered')
        drugs_data = drugs_administered_ref.get()

        # Dictionary to count doses administered per day
        daily_counts = defaultdict(int)

        for entry in drugs_data:
            data = entry.to_dict()
            date_str = data.get("DateOfAdministration")
            if date_str:
                parsed_date = parse_date(date_str)
                if parsed_date and parsed_date >= start_date:
                    # Count doses by day
                    day_key = parsed_date.strftime('%Y-%m-%d')
                    daily_counts[day_key] += 1

        # Prepare data for the response
        sorted_dates = sorted(daily_counts.keys())
        daily_data = [{"date": date, "count": daily_counts[date]} for date in sorted_dates]

        return jsonify({
            "status": "success",
            "data": daily_data
        })

    except Exception as e:
        print(f"Error fetching weekly drug sales data: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/top_drugs_administered', methods=['GET'])
def top_drugs_administered():
    try:
        today = datetime.now()
        start_date = today - timedelta(days=7)

        # Query the database for DrugsAdministered entries
        drugs_administered_ref = db.collection('DrugsAdministered')
        drugs_data = drugs_administered_ref.get()

        # Dictionary to count doses administered per day for each drug
        daily_drug_counts = defaultdict(lambda: defaultdict(int))

        for entry in drugs_data:
            data = entry.to_dict()
            date_str = data.get("DateOfAdministration")
            drug_name = data.get("DrugName")  # Assuming you have a field for the drug name
            if date_str and drug_name:
                parsed_date = parse_date(date_str)
                if parsed_date >= start_date:
                    day_key = parsed_date.strftime('%Y-%m-%d')
                    daily_drug_counts[day_key][drug_name] += 1

        # Prepare data for the response
        result = {}
        for date, drugs in daily_drug_counts.items():
            # Sort drugs by count and get the top 3
            sorted_drugs = sorted(drugs.items(), key=lambda x: x[1], reverse=True)[:3]
            result[date] = {drug: count for drug, count in sorted_drugs}

        return jsonify({
            "status": "success",
            "data": result
        })

    except Exception as e:
        print(f"Error fetching top drugs administered: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500



""""@app.route('/view_users', methods=['GET'])
#def view_users():
    # Fetching parent data
    parents_ref = db.collection('parentData')
    parents = parents_ref.stream()

    parent_list = []
    for parent in parents:
        parent_dict = parent.to_dict()

        parent_list.append({
            'parent_national_id': parent_dict.get('parentNationalID', 'N/A'),
            'parent_name': parent_dict.get('parentName', 'N/A'),
            'parent_gender': parent_dict.get('parentGender', 'N/A'),
            'parent_email': parent_dict.get('parentEmailAddress', 'N/A'),
            'parent_contact': parent_dict.get('parentPhoneNumber', 'N/A'),
        })

    return jsonify(parent_list)
"""

@app.route('/view_users', methods=['GET'])
def view_users():
    # Fetching parent data
    parents_ref = db.collection('parentData')
    parents = parents_ref.stream()

    # Fetching child data
    children_ref = db.collection('childData')
    children = children_ref.stream()

    # Create a dictionary to map parent national IDs to parent data
    parent_dict = {}
    for parent in parents:
        parent_data = parent.to_dict()
        national_id = parent_data.get('parentNationalID', 'N/A')
        parent_dict[national_id] = {
            'parent_national_id': national_id,
            'parent_name': parent_data.get('parentName', 'N/A'),
            'parent_gender': parent_data.get('parentGender', 'N/A'),
            'parent_email': parent_data.get('parentEmailAddress', 'N/A'),
            'parent_contact': parent_data.get('parentPhoneNumber', 'N/A'),
            'children': []  # Initialize an empty list for children
        }

    # Collect children data and associate them with their parents
    for child in children:
        child_data = child.to_dict()
        parent_national_id = child_data.get('ParentNationalID')
        if parent_national_id in parent_dict:
            parent_dict[parent_national_id]['children'].append(child_data.get('ChildName', 'Unknown'))

    # Prepare the final list to return
    parent_list = list(parent_dict.values())
    
    return jsonify(parent_list)


@app.route('/view_users_simple', methods=['GET'])
def view_users_simple():
    # Fetching parent data, limiting to 3 records
    parents_ref = db.collection('parentData').limit(3)
    parents = parents_ref.stream()

    # Fetching child data
    children_ref = db.collection('childData')
    children = children_ref.stream()

    # Create a dictionary to map parent national IDs to parent data
    parent_dict = {}
    for parent in parents:
        parent_data = parent.to_dict()
        national_id = parent_data.get('parentNationalID', 'N/A')
        parent_dict[national_id] = {
            'parent_national_id': national_id,
            'parent_name': parent_data.get('parentName', 'N/A'),
            'parent_contact': parent_data.get('parentPhoneNumber', 'N/A'),
            'children': []  # Initialize an empty list for children
        }

    # Collect children data and associate them with their parents
    for child in children:
        child_data = child.to_dict()
        parent_national_id = child_data.get('ParentNationalID')
        if parent_national_id in parent_dict:
            parent_dict[parent_national_id]['children'].append(child_data.get('ChildName', 'Unknown'))

    # Prepare the final list to return
    parent_list = list(parent_dict.values())
    
    return jsonify(parent_list)

nurse_collection = db.collection('nurseData')

@app.route('/manage_nurses', methods=['GET'])
def get_nurses():
    try:
        nurses = nurse_collection.stream()
        nurse_list = []
        for nurse in nurses:
            nurse_data = nurse.to_dict()
            nurse_info = {
                "nurseNationalID": nurse_data.get("nurseNationalID", "N/A"),
                "nurseName": nurse_data.get("nurseName", "N/A"),
                "nursephonenumber": nurse_data.get("nursephonenumber", "N/A"),
                "nurseGender": nurse_data.get("nurseGender", "N/A"),
                "nurseEmailAddress": nurse_data.get("nurseEmailAddress", "N/A")
            }
            nurse_list.append(nurse_info)
        
        return jsonify(nurse_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/manage_nurses/<nurseNationalID>', methods=['DELETE'])
def delete_nurse(nurseNationalID):
    try:
        # Query for the document with the specified National ID
        nurse_docs = nurse_collection.where('nurseNationalID', '==', nurseNationalID).stream()
        found = False
        for doc in nurse_docs:
            nurse_collection.document(doc.id).delete()
            found = True

        if found:
            return jsonify({"message": f"Nurse with ID {nurseNationalID} has been deleted"}), 200
        else:
            return jsonify({"message": "Nurse not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

vaccines_ref = db.collection('DrugsAdministered')
@app.route('/add_vaccine_data', methods=['POST'])
def add_vaccine_data():
    data = request.json  # Get the data from the request
    print("Received data:", data)  # Log the incoming data for debugging
    try:
        # Check if data is a list
        if not isinstance(data, list):
            return jsonify({"success": False, "error": "Data should be a list of vaccine records."}), 400

        # Add each record to Firestore
        for record in data:
            vaccines_ref.add(record)  # Add each record to the collection

        return jsonify({"success": True, "message": "Vaccine data added successfully."}), 201
    except Exception as e:
        print(f"Error: {str(e)}")  # Print the error to the console for debugging
        return jsonify({"success": False, "error": str(e)}), 500




def parse_date2(date_str):
    try:
        # Strip off the timezone and parse the core part of the date
        core_date_str = date_str.split(" GMT")[0]
        return datetime.strptime(core_date_str, '%a %b %d %Y %H:%M:%S')
    except ValueError as e:
        print(f"Date parsing error for {date_str}: {e}")
        return None
# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Running on localhost:5000
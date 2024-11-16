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




@app.route('/google_authenticate', methods=['POST'])
def google_authenticate():
    try:
        token = request.json.get('token')
        if not token:
            return jsonify({'error': 'Token is missing'}), 400

        # Verify the token without passing client_id
        idinfo = id_token.verify_oauth2_token(token, Request())

        # Token is valid, proceed with your logic
        user_id = idinfo['sub']
        return jsonify({'localId': user_id, 'redirectUrl': '/dashboard'})

    except ValueError as e:
        return jsonify({'error': 'Invalid token'}), 400


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
@app.route('/vaccinationupdate')
def vaccinationupdate():
    try:
        child_local_id = request.args.get("localId")
        
        doc_ref = db.collection('VaccinationHistory')
        query = doc_ref.where(filter=FieldFilter("child_local_ID", "==", child_local_id))
        docs = query.stream()
        document_list = []
        
        for doc in docs:
            data = doc.to_dict()
            document_list.append(data)

        if document_list:
            # Sort documents, putting any with unparseable dates at the end
            try:
                document_list.sort(
                    key=lambda x: parse_date(x['DateofVaccination']) or datetime.min,
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

@app.route('/DrugAdministered', methods=['POST'])
def DrugAdministered():
    data = request.get_json()
    selected_drugs = data.get("SelectedDrug", [])
    total_price = 0

    try:
        for drug_name in selected_drugs:
            # Query Firestore for each drug in the DrugInventory collection
            drug_query = db.collection('DrugInventory').where('DrugName', '==', drug_name).stream()
            
            # For each document that matches the drug name, get the price
            for doc in drug_query:
                drug_data = doc.to_dict()
                price = drug_data.get('DrugPrice', 0)
                total_price += price

        return jsonify({"message": "Prices retrieved successfully", "total_price": total_price}), 200

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
        'parentEmailAddress':parentEmailAddress
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
        redirect_url = f"http://localhost:8080/KingaBora-Vaccination-System/JoyAdmin/Admin/manage_profile.html?localId={local_id}"

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
def getEmailList():
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
                    # Only add the email address, child name, and NextVisit to the response
                    response_data.append({
                        "childName": doc_data.get("childName"),
                        "parentEmailAddress": doc_data.get("parentEmailAddress"),
                        "NextVisit": doc_data.get("NextVisit"),
                    })
        
        # Return results or 404 if none found
        if response_data:
            return jsonify({"message": "Parent details found", "data": response_data}), 200
        else:
            return jsonify({"error": "No documents found for the given 'NextVisit'"}), 404

    except Exception as e:
        logging.error(f"Error fetching parent details: {str(e)}")
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
        # Limit the results to 4 documents
        docs = query.limit(4).stream()

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
    
    
@app.route('/addChild', methods=['POST'])
def addChild():
    try:
        data = request.get_json()
        
        # Parse and format the date
        original_date = data.get('dateOfBirth')
        parsed_date = parse_date(original_date)
        if parsed_date is None:
            return jsonify({"error": "Invalid date format"}), 400
        
        formatted_date = parsed_date.strftime("%B %d, %Y at %I:%M:%S %p GMT+3")
        
        # Create child document data
        child_data = {
            'BirthCertificateID': data.get('birthCertificateID'),
            'ChildName': data.get('childName'),
            'DateOfBirth': formatted_date,  # Use the formatted date
            'Gender': data.get('gender'),
            'Weight': float(data.get('weight')),
            'Height': float(data.get('height')),
            'ParentName': data.get('parentName'),
            'ParentNationalID': data.get('parentNationalID'),
            'emailaddress': data.get('emailaddress')
        }

        # Validate required fields
        required_fields = ['BirthCertificateID', 'ChildName', 'ParentNationalID']
        for field in required_fields:
            if not child_data.get(field):
                return jsonify({"error": f"Missing required field: {field}"}), 400

        # Check if a child with this Birth Certificate ID already exists
        existing_children = db.collection('childData').where('BirthCertificateID', '==', child_data['BirthCertificateID']).get()
        if len(list(existing_children)) > 0:
            return jsonify({"error": "A child with this Birth Certificate ID already exists"}), 400

        # Add to Firestore with auto-generated ID
        doc_ref = db.collection('childData').add(child_data)
        
        # Get the auto-generated document ID
        doc_id = doc_ref[1].id

        return jsonify({
            "message": "Child added successfully",
            "childId": doc_id,
            "birthCertificateID": child_data['BirthCertificateID']
        }), 201

    except Exception as e:
        logging.error(f"Error adding child: {str(e)}")
        return jsonify({"error": str(e)}), 500


# from today (kangskii)

from datetime import datetime

@app.route('/ChildVaccinationProgress', methods=['GET'])
def ChildVaccinationProgress():
    try:
        docs = db.collection('VaccinationHistory').stream()
        child_data = {}

        for doc in docs:
            data = doc.to_dict()
            child_name = data.get("childName")
            vaccination_date = data.get("DateofVaccination")
            weight = data.get("weight")
            height = data.get("height")

            # Ensure we have necessary data
            if child_name and vaccination_date and weight is not None and height is not None:
                # Parse the date
                try:
                    date_parsed = datetime.strptime(vaccination_date.rsplit(" GMT", 1)[0], "%B %d, %Y at %I:%M:%S %p")
                except ValueError as e:
                    logging.error(f"Date parsing error for {vaccination_date}: {e}")
                    continue  # Skip if date is not in expected format

                # Initialize child entry if it doesn't exist
                if child_name not in child_data:
                    child_data[child_name] = []

                # Append the entry with parsed date
                child_data[child_name].append({
                    "date": date_parsed,
                    "weight": weight,
                    "height": height
                })

        # Sort each child's records by date
        for child_name in child_data:
            child_data[child_name].sort(key=lambda x: x["date"])

        # Convert dates back to strings for JSON response
        formatted_data = {}
        for child_name, records in child_data.items():
            formatted_data[child_name] = {
                "dates": [record["date"].strftime("%B %d, %Y at %I:%M:%S %p") for record in records],
                "weights": [record["weight"] for record in records],
                "heights": [record["height"] for record in records]
            }

        # Log the sorted data to verify structure
        logging.info("Child vaccination progression data prepared: %s", formatted_data)

        return jsonify({
            "message": "Child vaccination progression data fetched",
            "data": formatted_data
        }), 200

    except Exception as e:
        logging.error(f"Error fetching child vaccination progression data: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
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
    
    # Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Running on localhost:5000
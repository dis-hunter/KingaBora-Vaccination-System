// Firebase Configuration
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT_ID.appspot.com",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID",
    measurementId: "YOUR_MEASUREMENT_ID"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

// Get the current user's ID (Assuming the user is authenticated)
const userId = "USER_ID"; // Replace with actual user ID logic, e.g., Firebase Auth

// Function to open modal and fetch data
function openModal() {
    const modal = document.getElementById("profileModal");
    modal.style.display = "block";

    // Fetch nurse data from Firestore
    db.collection("nurses").doc(userId).get().then((doc) => {
        if (doc.exists) {
            const nurseData = doc.data();
            document.getElementById("nurseName").innerText = nurseData.nurseName;
            document.getElementById("nurseNationalID").innerText = nurseData.nurseNationalID;
            document.getElementById("nursePhoneNumber").innerText = nurseData.nursePhoneNumber;
            document.getElementById("nurseEmailAddress").innerText = nurseData.nurseEmailAddress;
        } else {
            console.log("No such document!");
        }
    }).catch((error) => {
        console.error("Error getting document:", error);
    });
}

// Function to close modal
function closeModal() {
    const modal = document.getElementById("profileModal");
    modal.style.display = "none";
}

// Function to redirect to the edit form
function redirectToEditForm() {
    window.location.href = "edit-profile.html"; // Replace with your form page URL
}

// Close modal when clicking outside of it
window.onclick = function(event) {
    const modal = document.getElementById("profileModal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
};

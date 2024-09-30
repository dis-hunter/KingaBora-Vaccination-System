// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDigqFcCi42MFXvhsuaQH-0HoeWVCRIrq8",
  authDomain: "kingaboravaccinationsystem.firebaseapp.com",
  projectId: "kingaboravaccinationsystem",
  storageBucket: "kingaboravaccinationsystem.appspot.com",
  messagingSenderId: "797186497406",
  appId: "1:797186497406:web:7ff7e514e5add24dd6f12f",
  measurementId: "G-1WJNS5WW31"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
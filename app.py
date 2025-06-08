from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from pyfingerprint.pyfingerprint import PyFingerprint
import tenseal
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "caf5989106fc5265b629d7ca1761e891ddbe9eaee031f0d12971fc53277b60c4")  # Replace with a secure hex key

# Set up MongoDB Atlas Connection
mongo_uri = "mongodb+srv://AA:XpxJHyR3oA7pOaWS@cluster0.vgemvty.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_uri)
db = client["biometricDB"]
users_collection = db["users"]

# Initialize fingerprint scanner
try:
    scanner = PyFingerprint('/dev/ttyUSB1', 9600, 0xFFFFFFFF, 0x00000000)
    if not scanner.verifyPassword():
        raise ValueError("Fingerprint scanner password incorrect!")
    print("Fingerprint scanner connected successfully.")
except Exception as e:
    print("Error connecting to fingerprint scanner:", e)
    scanner = None

def scan_fingerprint():
    """Capture fingerprint and encrypt it using TenSEAL"""
    if scanner is None:
        return None

    print("Place your finger on the scanner...")
    while scanner.readImage() == False:
        pass

    scanner.convertImage(0x01)
    fingerprint_features = scanner.downloadCharacteristics(0x01)

    # Homomorphic Encryption
    context = tenseal.context()
    context.generate_galois_keys()
    encrypted_fp = context.encrypt(fingerprint_features)
    return encrypted_fp.serialize()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if users_collection.find_one({"username": username}):
            return "User already exists. Try logging in."

        fingerprint_data = scan_fingerprint()
        if fingerprint_data is None:
            return "Fingerprint scanner error. Try again later."

        user_data = {
            "username": username,
            "password": hashed_password,
            "fingerprint": fingerprint_data
        }
        users_collection.insert_one(user_data)
        return redirect(url_for('login'))
    return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user = users_collection.find_one({"username": username})
        if user and user["password"] == hashed_password:
            session["username"] = username
            fingerprint_data = scan_fingerprint()
            if fingerprint_data == user["fingerprint"]:
                session["authenticated"] = True
                return redirect(url_for('dashboard'))
            else:
                return "Fingerprint authentication failed. Try again."
        else:
            return "Invalid credentials."
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if "username" in session and session.get("authenticated", False):
        return f"Welcome {session['username']}!"
    else:
        return redirect(url_for('login'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """Allows users to reset their password, ensuring the new password is different from the old one"""
    if request.method == 'POST':
        username = request.form.get("username")
        new_password = request.form.get("new_password")

        if not username or not new_password:
            return "Username and new password are required."

        hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()

        user = users_collection.find_one({"username": username})
        if user:
            if user["password"] == hashed_new_password:
                return "New password cannot be the same as the old password."

            users_collection.update_one({"username": username}, {"$set": {"password": hashed_new_password}})
            return redirect(url_for('login'))
        else:
            return "User not found."

    return render_template("forgot_password.html")

if __name__ == "__main__":
    app.run(debug=False)
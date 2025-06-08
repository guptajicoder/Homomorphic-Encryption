### **Biometric Authentication System - Setup & Usage Guide**  

This documentation will guide you on setting up your own **biometric authentication system** using **Flask**, **MongoDB Atlas**, and **Homomorphic Encryption** via **TenSEAL**.  

---

## **1. Prerequisites**  
Before setting up the environment, ensure you have:  
✅ Python **3.x** installed ([Download Python](https://www.python.org/downloads/))  
✅ MongoDB Atlas account ([MongoDB Atlas](https://www.mongodb.com/atlas))  
✅ Virtual environment (`venv` for dependency isolation)  
✅ Fingerprint scanner hardware (compatible with **PyFingerprint**)  

---

## **2. Environment Setup**  
### **Step 1: Create & Activate Virtual Environment**  
Open **Command Prompt/Terminal** and run:  
```powershell
python -m venv myenv
```
Activate the environment:  
- **Windows**:
  ```powershell
  .\myenv\Scripts\Activate.ps1
  ```
- **Mac/Linux**:
  ```bash
  source myenv/bin/activate
  ```

---

### **Step 2: Install Dependencies**  
Run the following command inside your virtual environment:  
```powershell
pip install flask pymongo pyfingerprint tenseal dnspython
```

---

### **Step 3: Configure MongoDB Atlas**  
1. **Create a MongoDB cluster** on **MongoDB Atlas**.  
2. **Set up a database named `biometricDB`**.  
3. **Create a user** with proper credentials.  
4. **Whitelist your IP** (or use `0.0.0.0/0` for open access).  
5. **Get the connection string** (it will look like this):  
   ```plaintext
   mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
   ```
6. Replace **username & password** in `app.py`.

---

## **3. Running the App**  
### **Modify `app.py` for Your Credentials**  
Ensure the connection string is set up correctly:  
```python
mongo_uri = "mongodb+srv://<your-username>:<your-password>@cluster0.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongo_uri)
db = client["biometricDB"]
users_collection = db["users"]
```
Replace `<your-username>` and `<your-password>` with **MongoDB credentials**.

### **Start Flask Server**  
Run:
```powershell
python app.py
```
✅ If successful, the terminal will show:
```
* Running on http://127.0.0.1:5000/
```
Open this in your **browser**.

---

## **4. Using the System**  
### **Sign Up Flow**
1. **Enter username & password.**  
2. **Place your finger on the fingerprint scanner.**  
3. Data is **encrypted via Homomorphic Encryption (TenSEAL)** before storage.  
4. **Account created!** 🎉

### **Login Flow**
1. **Enter username & password.**  
2. **Scan your fingerprint for verification.**  
3. **If matches, user is authenticated.** ✅  
4. Redirects to the **dashboard**.

### **Forgot Password**
1. Click **"Forgot Password?"** in **login page**.  
2. Enter **username & new password**.  
3. System ensures **new password differs from the old one**.  
4. **Password updated in MongoDB.**  

---

## **5. Troubleshooting**
🚨 **MongoDB Authentication Error?**  
- Check **MongoDB credentials** & update `app.py`.  
- **Whitelist your IP** in MongoDB Atlas.  

🚨 **Fingerprint Scanner Not Recognized?**  
- Run:
  ```powershell
  ls /dev/ttyUSB*
  ```
- Ensure correct **port (`/dev/ttyUSB1` or `COM3`)** is set in `app.py`.

🚨 **Flask Not Running?**  
- Ensure **virtual environment is activated** before running:
  ```powershell
  python app.py
  ```


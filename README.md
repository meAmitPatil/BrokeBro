# **BrokeBro**

BrokeBro is an AI-powered voice assistant that calls you in real-time to stop impulsive spending, specifically on food delivery apps like DoorDash.

## **Features**
- Detects DoorDash orders via Screenpipe OCR.
- Calls you using an AI assistant **"Future You"** to persuade you to reconsider your purchase.
- Uses **Groq** for smart, humorous responses.
- Customizable voice settings.

---

## **Getting Started**

### **1) Clone the Repository**
```bash
https://github.com/meAmitPatil/BrokeBro
cd BrokeBro
```

### **2) Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate
```

### **3) Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4) Configure Environment Variables**
Set up Groq, Vapi accounts and their api keys
```bash
cp .env.example .env
```

### **5) Run the Fastapi Server**
```bash
cd server
uvicorn server.main:app --reload
```

### **6) Run the Screenpipe Client**
```bash
cd client
python main.py
```

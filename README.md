# PiggyBot - WhatsApp Expense Tracker Bot

PiggyBot is a WhatsApp-based expense tracker bot that helps users manage their expenses seamlessly through WhatsApp messages. The bot is powered by a Flask backend and utilizes MongoDB for data storage. It leverages machine learning for message classification and integrates Gemini's API to improve response accuracy.

---

## 🚀 Features

✅ **Expense Tracking** - Log expenses directly via WhatsApp messages.  
✅ **MongoDB Storage** - Efficient and scalable database for managing user expenses.  
✅ **Gemini API Integration** - Enhances response generation with LLM-based insights.  
✅ **Webhook Implementation** - Securely receives and processes WhatsApp messages.  
✅ **Render Deployment** - Hosted on Render for permanent accessibility.  

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Database:** MongoDB
- **LLM Integration:** Gemini API (Phi-3 Mini)
- **Deployment:** Render/ngrok
- **WhatsApp API:** Meta's WhatsApp Business API

---



## 🔧 Setup & Installation

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/your-username/PiggyBot.git
cd PiggyBot
```

### **2️⃣ Create a Virtual Environment**
```sh
python -m venv piggybot_env
source piggybot_env/bin/activate  # On macOS/Linux
piggybot_env\Scripts\activate  # On Windows
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Set Up Environment Variables**
Create a `.env` file and configure the following:
```
WHATSAPP_TOKEN=<your-whatsapp-api-token>
MONGO_URI=<your-mongodb-uri>
GEMINI_API_KEY=<your-openai-api-key>
```

### **5️⃣ Run the Flask Application**
```sh
python app.py
```

### **6️⃣ Expose Webhook (For Local Testing)**
```sh
ngrok http 5000
```
Use the generated URL to configure your WhatsApp Webhook.

---

## 📡 Deployment on Render

1. Push your code to GitHub.
2. Create a new Render web service.
3. Connect your GitHub repository.
4. Add the necessary environment variables.
5. Deploy and obtain a public URL for the webhook.

---

## 🛠️ Troubleshooting

### **Duplicate Messages Received**
🔹 Ensure the webhook returns `200 OK` to prevent WhatsApp retries.
🔹 Track processed message IDs to avoid duplicate processing.
🔹 Check logs for unexpected webhook triggers.

### **Bot Responding Without User Input**
🔹 Verify if a loop or cron job is causing automatic messages.
🔹 Log incoming webhook requests to debug unwanted responses.
🔹 Check MongoDB to confirm if old messages are being reprocessed.

---

## 📌 Future Enhancements

🚀 Add NLP-based expense categorization  
🚀 Implement analytics and visualization dashboards  
🚀 Introduce budget alerts and financial recommendations 
🚀 Improving consistency in LLM outputs


---



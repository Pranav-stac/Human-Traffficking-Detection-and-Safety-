# 🚨 Human Trafficking Detection, Prevention & Support System 🚨

Welcome to the **Human Trafficking Detection, Prevention, and Support System**! This project leverages AI/ML models and mobile technology to detect violent activities through CCTV footage, provide alerts, and help individuals send distress signals along with their location to a centralized admin dashboard. The admin website also contains stories of trafficked individuals, support resources, and important information on how to prevent trafficking.

---

## 🌟 Features

- **AI/ML Detection (MobileNet & Bi-directional LSTM):**
  - 🎥 Trained on **1000 videos** of violence and non-violence.
  - 📹 Detects suspicious activities from **CCTV footage** using a trained model.
  - 🚨 Sends **real-time alerts** to an admin panel.

- **Admin Website (Django):**
  - 🖥️ Real-time alert dashboard with **violence detection** notifications.
  - 📖 Stories of trafficked individuals and their recovery.
  - 📚 Support resources and information for **trafficking prevention**.
  
- **Mobile App:**
  - 🗺️ **Google Map Integration** for easy navigation and locating safety zones.
  - 🚨 **SOS Button** to send distress signals with location to the admin.
  - 🛡️ **Safety Features** like contact sharing and location tracking.

---

## 📸 Screenshots & Demo

Here are some screenshots and a video demo to help you visualize how the system works:

- **Admin Dashboard with Alerts:**
  ![Admin Dashboard](path-to-your-image/admin-dashboard.png)

- **Mobile App with Google Maps & SOS Button:**
  ![Mobile App Google Maps](path-to-your-image/mobile-app-maps.png)

- **SOS Signal Sent with Location:**
  ![SOS Signal](path-to-your-image/sos-signal.png)

- **Video Demo:**
  [Watch the Demo](path-to-your-video/demo.mp4)

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally:

### 📦 Prerequisites

Ensure you have the following installed on your system:

- **Python 3.8+**
- **Django 4.0+**
- **TensorFlow/Keras for AI Model**
- **Flutter** for the mobile app
- **Google Maps API** for location services
- **PostgreSQL** for the database

### 🔧 Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YourUsername/human-trafficking-detection.git
   cd human-trafficking-detection


bash
Copy code
pip install -r requirements.txt
Set up the PostgreSQL Database:

bash
Copy code
# Create the database
createdb trafficking_detection
# Migrate Django models to the database
python manage.py migrate
Run the AI model setup:

Download the MobileNet and Bi-Directional LSTM models trained on 1000 videos.
Place the models in the models/ directory.
Run the Django Development Server:

bash
Copy code
python manage.py runserver
Set up ngrok to create a public URL for your Django server:

Download and install ngrok from here.
Run ngrok to forward your local Django server:
bash
Copy code
ngrok http 8000
Copy the Forwarding URL provided by ngrok (e.g., https://your-tunnel-url.ngrok.io).
Configure the Mobile App:

Open the mobile app’s configuration.
Replace the API endpoint in the app with your ngrok tunnel URL:
dart
Copy code
const apiEndpoint = "https://your-tunnel-url.ngrok.io/api/";
Run the Mobile App:

Set up Flutter on your system.
Add your Google Maps API Key in the Flutter code.
Build and run the app on your mobile device or emulator:

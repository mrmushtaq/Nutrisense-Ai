# 🥗 NutriSense AI
### Intelligent Food Recognition and Personalized Nutrition Recommendation System

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat-square&logo=streamlit)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?style=flat-square&logo=tensorflow)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightblue?style=flat-square&logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📌 Project Overview

**NutriSense AI** is an AI-powered nutrition assistant that uses computer vision and intelligent recommendation techniques to analyze food images, estimate nutritional information, track user eating habits, and provide personalized dietary recommendations.

The system allows users to:
- Upload a food image
- Automatically recognize the food using an AI image classification model
- Map detected food with nutritional data
- Store meal records in a database
- Track daily calorie goals
- Get personalized nutrition advice through an AI coach

---

## ❓ Problem Statement

Many people find it difficult to manually track their daily food intake, calories, and nutritional balance. Traditional calorie tracking applications require users to manually search and enter food details.

**NutriSense AI** solves this problem by automating food identification and nutrition tracking using Artificial Intelligence.

---

## 🎯 Objectives

- ✅ Automatically recognize food from images using AI
- ✅ Estimate calories and macronutrients
- ✅ Maintain user meal history
- ✅ Track daily calorie consumption
- ✅ Monitor protein, carbohydrate, and fat intake
- ✅ Generate personalized nutrition recommendations
- ✅ Provide an easy-to-use AI nutrition assistant

---

## 🔄 System Workflow

```
User uploads food image
        ↓
AI Food Recognition Model (EfficientNetB0)
        ↓
Food Prediction + Confidence Score
        ↓
Nutrition Knowledge Base Lookup
        ↓
Calories, Protein, Carbs, Fat Calculation
        ↓
SQLite Database Storage
        ↓
Dashboard Analytics
        ↓
AI Nutrition Recommendation Agent (Groq LLaMA)
```

---

## 🧩 Main Modules

### 1. 📸 AI Food Recognition Module
Uses a pretrained **EfficientNetB0** model trained on the **Food-101** dataset.

| Feature | Detail |
|---|---|
| Architecture | EfficientNetB0 (Transfer Learning) |
| Dataset | Food-101 + Pakistani Food Dataset |
| Output | Food label + Confidence Score |

**Example:**
```
Input:  Pizza image
Output: Food: Pizza | Confidence: 99%
```

---

### 2. 🥦 Nutrition Analysis Module
Maps predicted food with a comprehensive nutrition database.

| Nutrient | Example (Biryani) |
|---|---|
| Calories | 450 kcal |
| Protein | 20g |
| Carbohydrates | 55g |
| Fat | 15g |
| Health Score | 78/100 |

---

### 3. 🗄️ Database Module
**SQLite** is used as a lightweight embedded relational database.

**Main Tables:**
- `users` — User information and profiles
- `meals` — Food scan records and nutrition data
- `nutrition_foods` — Nutrition knowledge base

---

### 4. 📊 Dashboard Module
Complete overview of user nutrition status.

**Features:**
- Calories consumed vs goal
- Number of meals logged
- Health score
- Goal progress percentage
- Recent meal cards
- Weekly calorie trend chart

---

### 5. 🔥 Daily Calories Tracker
Tracks daily nutrition goals in real time.

- Daily calorie goal vs consumed
- Remaining calories
- Protein, Carbs, Fat progress bars

---

### 6. 📜 Meal History Module
Permanent storage of all scanned meals.

- Previous meal records with timestamps
- Calorie and nutrition history
- Meal type tracking

---

### 7. 🤖 AI Nutrition Coach
Powered by **Groq LLaMA 3.3 70B** — provides real-time personalized advice.

**Inputs:** Daily calories, macros, health score, meal history  
**Outputs:** Diet tips, warnings, next meal suggestions

**Example Response:**
> *"Aap ka protein intake thoda kam hai. Agle meal mein grilled chicken ya daal add karein for better muscle recovery. 💪"*

**Features:**
- Responds in English or Roman Urdu
- Goal-based recommendations (Weight Loss / Gain / Maintenance)
- Quick question buttons
- Full conversation history

---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| **Frontend** | Streamlit |
| **Language** | Python 3.10+ |
| **AI / ML** | TensorFlow, EfficientNetB0, Food-101 |
| **AI Coach** | Groq API (LLaMA 3.3 70B) |
| **Database** | SQLite |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Plotly |
| **Styling** | Custom CSS + Google Fonts (Inter) |

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/mrmushtaq/NutriSense-AI.git
cd NutriSense-AI
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the `streamlit_app/` directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at: [console.groq.com](https://console.groq.com)

### 4. Run the Application
```bash
cd streamlit_app
streamlit run home.py
```

### 5. Open in Browser
```
http://localhost:8501
```

---

## 📁 Project Structure

```
NutriSense-AI/
├── streamlit_app/
│   ├── home.py                    # Main dashboard
│   ├── Account.py                 # Sign In / Sign Up
│   ├── config.py                  # Goal recommendations & AI config
│   ├── .env                       # API keys (not committed)
│   ├── pages/
│   │   ├── 1_Upload_Food.py       # Food Scan page
│   │   ├── 2_Nutrition_Result.py  # Nutrition Report
│   │   ├── 3_Daily_Calories.py    # Calorie Tracker
│   │   ├── 4_Meal_History.py      # Meal History
│   │   └── 5_AI_Recommendation.py # AI Coach
│   └── src/
│       ├── ai/
│       │   ├── image_processor.py # Image preprocessing
│       │   └── prediction.py      # EfficientNetB0 inference
│       ├── database/
│       │   ├── connection.py      # SQLite connection
│       │   ├── meals.py           # Meal CRUD operations
│       │   └── user.py            # User management
│       ├── nutrition/
│       │   └── nutrition_database.py # Food nutrition data
│       └── utils/
│           ├── ui.py              # Shared UI components
│           ├── cards.py           # Card components
│           └── helpers.py         # Utility functions
```

---

## 🖥️ Screenshots

| Page | Description |
|---|---|
| Dashboard | Overview of daily nutrition stats |
| Food Scan | Upload image → AI recognition |
| Nutrition Report | Macro breakdown with charts |
| Daily Calories | Calorie tracker with progress |
| Meal History | All logged meals |
| AI Coach | Chat with AI nutrition assistant |

---

## 👤 Demo Account

You can try the app without signing up using the **"Continue as Demo User"** button on the login screen.

---

## 🎓 Academic Information

| Field | Detail |
|---|---|
| **Student** | Mushtaque Ali |
| **Roll No** | 023-23-0165 |
| **University** | Sukkur IBA University (SIBAU) |
| **Program** | Information Security |
| **Project** | NutriSense AI — Final Year Project |

---

## 📄 License

This project is developed for academic purposes at **Sukkur IBA University**.

---

## 🙏 Acknowledgements

- [Food-101 Dataset](https://data.vision.ee.ethz.ch/cvl/datasets_extra/food-101/)
- [TensorFlow / Keras](https://www.tensorflow.org/)
- [Streamlit](https://streamlit.io/)
- [Groq API](https://console.groq.com/)
- [Plotly](https://plotly.com/)

---

<div align="center">
  <strong>NutriSense AI v1.0</strong><br>
  Powered by TensorFlow EfficientNetB0 · Food-101 + Pakistani Food Dataset<br>
  Built with ❤️ at Sukkur IBA University
</div>
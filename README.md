# 🛒 RetailMind – Customer Feedback Analyzer

RetailMind is an **AI-powered NLP system** that analyzes customer reviews, performs sentiment analysis, extracts top topics, and generates summaries.  
It provides an interactive **React dashboard** backed by a **FastAPI backend**, making customer feedback easy to visualize and act upon.  

---

## 🚀 Features
- 📥 Import reviews from **Hugging Face datasets** or CSV/JSON files  
- 🧹 **Text preprocessing** (cleaning, stopword removal, normalization)  
- 😊 **Sentiment Analysis** using **VADER**  
- 📝 **Summarization** using Hugging Face **T5**  
- 🔑 **Topic extraction** for identifying top customer concerns  
- 📊 Interactive **React Dashboard** with charts & tables  
- ⚡ **REST API** built with **FastAPI** to serve results  

---

## 🏗️ Project Structure
```
RetailMind/
│-- Backend/          # FastAPI backend with NLP pipeline
│-- Frontend/         # React dashboard (charts, UI)
│-- .gitignore
│-- README.md
```

---

## 🖥️ Tech Stack
- **Backend**: Python, FastAPI, NLTK, Hugging Face Transformers  
- **Frontend**: React, Chart.js / Recharts, Tailwind CSS  
- **Other Tools**: Pandas, scikit-learn, VADER  

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repo
```bash
git clone https://github.com/RishabhBaghel8959/RetailMind.git
cd RetailMind
```

### 2️⃣ Backend Setup (FastAPI)
```bash
cd Backend
python -m venv .venv
.venv\Scripts\activate   # (Windows)
pip install -r requirements.txt
uvicorn app:app --reload
```
Backend will run at: 👉 `http://127.0.0.1:8000`

### 3️⃣ Frontend Setup (React)
```bash
cd ../Frontend
npm install
npm start
```
Frontend will run at: 👉 `http://localhost:3000`


---

## 📜 License
This project is licensed under the **MIT License**.  

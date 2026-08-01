# 🚗 Rade Mate – College Auto & Cab Pooling

**Team ID:** CX021  
**Team Name:** Innovix

---

# 👥 Team Members

- **Divyanshu Katwe** – Frontend Developer
- **Nayan Gokhale** – Backend Developer
- **Najuka Shendre** – UI/UX Designer
- **Ritika Shinde** – Testing & Presentation

---

# 📌 Problem Statement

Many college students travel to and from college every day using autos or cabs. Often, multiple students are heading to the same destination at similar times but are unaware of each other. As a result, they book separate rides, increasing travel expenses and causing unnecessary vehicle usage.

**Rade Mate** solves this problem by allowing students to create rides, discover other students traveling on the same route, request to join rides, and automatically split the fare. This makes commuting more affordable, convenient, and environmentally friendly.

---

# 💻 Tech Stack

### Frontend
- React.js (Vite)
- Tailwind CSS
- React Router
- Axios
- Lucide React Icons

### Backend
- FastAPI (Python)
- Uvicorn
- Pydantic
- FastAPI CORS Middleware

### Database
- No Database (Prototype uses in-memory Python lists and dictionaries)

### Tools & Technologies
- Git
- GitHub
- Visual Studio Code

---

# ✨ Features

- 🚗 Create a Ride
- 🔍 Browse Available Rides
- 📍 Smart Route Matching
- 🤝 Join Ride
- 💰 Automatic Fare Splitting
- ⚡ Dynamic UI Updates
- 📱 Fully Responsive Design
- ✅ Input Validation
- ⚠️ Friendly Error Handling
- 📊 Dashboard with Ride Statistics
- 🎯 Sample Ride Data for Live Demo

---

# 📦 Installation

## Frontend

```bash
cd frontend
npm install
```

## Backend

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

---

# ▶️ How to Run

## Frontend

```bash
cd frontend
npm run dev
```

## Backend

```bash
cd backend
uvicorn src.main:app --reload
```

---

# 🚀 Project Workflow

1. Student creates a ride by entering pickup, destination, date, time, seats, and fare.
2. Other students browse available rides.
3. The system finds rides with similar routes and timings.
4. Students send a join request.
5. Available seats are updated instantly.
6. Fare is automatically divided among all passengers.
7. The application provides a smooth and responsive user experience for the live demo.

---

# 🎯 Objective

To reduce transportation costs for college students by enabling ride sharing among students traveling on similar routes and at similar times. The platform promotes affordable travel, better resource utilization, and a smarter campus commuting experience.

---

# 🌟 Future Enhancements

- Google Maps Integration
- Live Location Tracking
- In-App Chat
- Ride Ratings & Reviews
- Push Notifications
- AI-Based Smart Route Recommendations

---

# 👨‍💻 Developed By

**Team Innovix**  
**CODEX Hackfest 2026**

# 🛺 RideMate – College Auto & Cab Pooling

> **Hackathon Prototype & Live Demo Application**  
> A modern, full-stack, responsive web application for college students to pool Auto Rickshaws and Cabs, split fares dynamically, and find smart matches based on campus locations and travel times.

---

## 🌟 Key Features

1. **10 Pre-loaded Sample Rides**: Automatically initialized on backend launch (College to Sitabuldi, Airport, Dharampeth, Sadar, Medical Square, IT Park, Railway Station, etc.).
2. **In-Memory Python Data Store**: High performance zero-database architecture (Python lists and dicts).
3. **Smart Ride Matching Algorithm**: Evaluates pickup, destination, vehicle type, and travel time within a **±30 minute** window, generating percentage scores (**98% Match**, **90% Match**, **82% Match**).
4. **Automated Fare Splitting**: Dynamically calculates per-person fare share as riders join (e.g. ₹200 total ➔ 1 Rider: ₹200, 2 Riders: ₹100, 3 Riders: ₹67, 4 Riders: ₹50).
5. **Instant UI Updates**: Sub-millisecond optimistic state updates in React without page reloads.
6. **Graceful Error Handling**: Interactive toast notifications, inline form validation, error states for empty fields, invalid fare, and exhausted seat capacity.
7. **Modern Glassmorphism UI**: High aesthetic Blue + White + Green theme with subtle backdrop blurs, glow effects, Lucide icons, and responsive layouts for mobile, tablet, and desktop.

---

## 🚀 Tech Stack

### Frontend
- **Framework**: React.js 18 + Vite
- **Styling**: Tailwind CSS + Custom Glassmorphism System
- **Routing**: React Router DOM (v6)
- **HTTP Client**: Axios
- **Icons**: Lucide React Icons

### Backend
- **Framework**: FastAPI (Python)
- **ASGI Server**: Uvicorn
- **Validation**: Pydantic v2
- **CORS**: FastAPI CORSMiddleware
- **Database**: None (In-Memory Python Data Structures)

---

## 📂 Project Structure

```
taskfloww/
├── backend/
│   ├── main.py              # FastAPI app setup, CORS, route registration
│   ├── models.py            # Pydantic schemas (Ride, RideCreate, JoinRideResponse, DashboardStats)
│   ├── data.py              # In-memory storage & 10 sample rides seeder
│   ├── routes.py            # API routes (GET, POST, PUT, DELETE, JOIN, SEARCH, STATS)
│   ├── utils.py             # Smart Matching algorithm & fare splitting helpers
│   └── requirements.txt     # Python backend dependencies
├── frontend/
│   ├── package.json         # Vite, React, Tailwind CSS, Axios, Lucide React dependencies
│   ├── vite.config.js       # Vite proxy setup for /api
│   ├── tailwind.config.js   # Tailwind custom theme & glassmorphism system
│   ├── index.html           # HTML template with Google Fonts
│   └── src/
│       ├── index.css        # Glassmorphic utilities & backdrop filters
│       ├── main.jsx         # React application entry point
│       ├── App.jsx          # React Router layout & global state
│       ├── services/
│       │   └── api.js       # Axios client with centralized API methods
│       ├── hooks/
│       │   └── useRides.js  # React custom hook for state & optimistic UI updates
│       ├── components/
│       │   ├── Navbar.jsx          # Responsive glassmorphism header
│       │   ├── Footer.jsx          # Modern sleek footer
│       │   ├── StatCard.jsx        # Glassmorphic metrics card
│       │   ├── RideCard.jsx        # Ride listing card with seats & fare split
│       │   ├── RideFilter.jsx      # Multi-field search & vehicle filter
│       │   ├── JoinRideModal.jsx   # Instant join confirmation modal
│       │   ├── Toast.jsx           # Notification alert popups
│       │   └── SmartMatchCard.jsx  # Highlight top matched rides
│       └── pages/
│           ├── LandingPage.jsx     # Hero section, About, Features & CTA
│           ├── DashboardPage.jsx   # Stats overview, active rides feed
│           ├── BrowseRidesPage.jsx # Full ride discovery & filter engine
│           └── CreateRidePage.jsx   # Ride offer form with live fare split preview
├── run_app.py               # Single command launcher script
└── README.md                # Documentation & hackathon evaluation guide
```

---

## 🔌 Connected Backend REST APIs

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/rides` | List all rides (supports pickup, destination, date, vehicle filters) |
| `GET` | `/api/rides/search` | Advanced Smart Match search with location & time scoring |
| `GET` | `/api/rides/stats` | Retrieve aggregate metrics for Dashboard cards |
| `GET` | `/api/rides/{id}` | Fetch specific ride details by ID |
| `POST` | `/api/rides` | Create a new ride offer (validates fare > 0, seats > 0) |
| `PUT` | `/api/rides/{id}` | Update existing ride details |
| `DELETE` | `/api/rides/{id}` | Remove/cancel ride post |
| `POST` | `/api/rides/{id}/join` | Join ride (decrements seats, recalculates fare split) |

---

## 🏃 Running Instructions

### Option 1: Quick Launcher (Recommended)
Run the helper script from the project root directory:

```bash
python run_app.py
```

This will automatically install dependencies and launch both servers simultaneously:
- **Frontend App**: `http://localhost:5173`
- **Backend API**: `http://127.0.0.1:8000`
- **Swagger Docs**: `http://127.0.0.1:8000/docs`

---

### Option 2: Manual Terminal Execution

#### 1. Start FastAPI Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

#### 2. Start React + Vite Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 🎯 Hackathon Live Demo Checklist

- [x] **Home Landing**: Hero with animated badges, features grid, how it works process.
- [x] **Dashboard**: Live stats for Total Available Rides, Active Rides, Seats Available, and Total Estimated Savings.
- [x] **Browse Rides**: Search by pickup/destination, filter by Auto/Cab and date, view match score % badges.
- [x] **Smart Matching**: Try searching "Sitabuldi" or "Airport" to see match scores ranked up to **98% Match**.
- [x] **Instant Join Ride**: Click "Join Ride" on any card -> watch seats drop immediately and per-person fare share decrease in real-time.
- [x] **Create Ride**: Fill out the form to post a new ride offer -> watch live fare split preview sidebar recalculate as you type total fare & seats.
- [x] **Error Handling**: Try submitting negative fare or empty locations -> observe instant validation feedback and toast popups without app crashing.

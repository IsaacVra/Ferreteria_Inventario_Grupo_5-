# CORS Issue Fix

## Problem
The frontend (localhost:5173) cannot connect to the backend (127.0.0.1:5000) due to CORS policy errors.

## Solution
1. **Fixed CORS Configuration**: Updated `backend/app.py` to properly configure CORS with specific origins, methods, and headers.

2. **Fixed API Endpoints**: Updated `frontend/src/auth.js` to use the correct `/api/auth` prefix that matches the backend routes.

3. **Created Startup Scripts**:
   - `start_app.bat` - Starts both backend and frontend servers
   - `start_backend.bat` - Starts only the backend server
   - `start_frontend.bat` - Starts only the frontend server

## How to Run

### Option 1: Use the startup script (Recommended)
```bash
# Double-click or run from command line
start_app.bat
```

### Option 2: Start servers manually
```bash
# Terminal 1 - Backend
cd backend
ferreteria_venv\Scripts\activate.bat
python app.py

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

## Verification
1. Backend should start on http://127.0.0.1:5000
2. Frontend should start on http://localhost:5173
3. Test the health endpoint: http://127.0.0.1:5000/api/health

## Troubleshooting
- If backend doesn't start, check MySQL connection in `backend/.env`
- If frontend can't connect, ensure both servers are running
- Check browser console for any remaining errors

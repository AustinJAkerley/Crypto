# 🚀 Quick Start Guide - CryptoLib Web Application

This is a **5-minute quick start** to get the application running locally.

## Prerequisites
- Python 3.11+
- Node.js 20+
- Terminal/Command Prompt

## Backend Setup (2 minutes)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin user (optional but recommended)
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: (choose a password)

# Start Django server
python manage.py runserver
```

**Backend is now running at http://localhost:8000** ✓

## Frontend Setup (2 minutes)

**Open a NEW terminal window** (keep the backend running!)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start React development server
npm start
```

**Frontend will automatically open at http://localhost:3000** ✓

## Test the Application (1 minute)

1. **Register a new account:**
   - The React app should open automatically
   - Click "Sign up" 
   - Fill in the form (username, email, password)
   - Click "Sign up" button

2. **Try a crypto operation:**
   - Click on "RSA Key Generation" card
   - Click "Generate Keys" button
   - View your generated RSA key pair!

3. **Try PyScript demo (no server needed):**
   ```bash
   # From project root, just open in browser
   open pyscript/index.html
   # or double-click the file
   ```

## What You'll See

### Login/Register Page
- Beautiful Canva-style split-screen design
- Purple gradient on the left
- Clean white form on the right
- 🔐 Lock icon and branding

### Dashboard
- Welcome message with your name
- 4 crypto tool cards:
  - RSA Key Generation 🔑
  - RSA Encryption 🔒
  - RSA Decryption 🔓
  - Diffie-Hellman 🤝

### Crypto Tools
- Tabbed interface for each operation
- Input forms with validation
- Real-time results in styled boxes
- All data processed securely via JWT auth

## Common Issues

### Backend won't start
```bash
# Make sure you're in the backend directory
cd backend

# Make sure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Try a different port if 8000 is busy
python manage.py runserver 8001
```

### Frontend won't start
```bash
# Clear npm cache if needed
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
npm start
```

### CORS Errors
- Make sure backend is running on port 8000
- Make sure frontend is on port 3000
- Settings are pre-configured for these ports

## API Endpoints

Once running, test these endpoints:

**Authentication:**
- POST http://localhost:8000/api/auth/register/
- POST http://localhost:8000/api/auth/login/
- GET http://localhost:8000/api/auth/me/

**Crypto Operations (requires login token):**
- POST http://localhost:8000/api/crypto/rsa/keygen/
- POST http://localhost:8000/api/crypto/rsa/encrypt/
- POST http://localhost:8000/api/crypto/rsa/decrypt/
- POST http://localhost:8000/api/crypto/dh/exchange/

## Next Steps

- Read [docs/local.md](../docs/local.md) for detailed setup
- Read [docs/staging.md](../docs/staging.md) for deployment
- Read [docs/production.md](../docs/production.md) for production

## File Locations

```
backend/
├── manage.py          # Django management
├── requirements.txt   # Python dependencies
├── .env.example       # Environment variables template
└── api/
    └── views.py       # Crypto endpoints

frontend/
├── package.json       # Node dependencies
├── src/
│   ├── App.js         # Main React app
│   └── components/    # React components

pyscript/
└── index.html         # Browser-based crypto demo

docs/
├── local.md           # Detailed local setup
├── staging.md         # Staging deployment
└── production.md      # Production deployment
```

## Development Workflow

1. **Make changes to backend:**
   - Edit files in `backend/api/`
   - Django auto-reloads on save
   - Test at http://localhost:8000/api/

2. **Make changes to frontend:**
   - Edit files in `frontend/src/`
   - React auto-reloads on save
   - View at http://localhost:3000

3. **Test everything:**
   - Use the web interface
   - Check browser console for errors
   - Check terminal for server logs

## Stopping the Servers

**Backend:**
- Press `Ctrl+C` in the backend terminal
- Deactivate venv: `deactivate`

**Frontend:**
- Press `Ctrl+C` in the frontend terminal

## Restarting

```bash
# Backend
cd backend
source venv/bin/activate
python manage.py runserver

# Frontend (in new terminal)
cd frontend
npm start
```

## Success Checklist

- ✅ Backend running on port 8000
- ✅ Frontend running on port 3000
- ✅ Can register a new user
- ✅ Can login successfully
- ✅ Can see dashboard with crypto tools
- ✅ Can generate RSA keys
- ✅ PyScript demo works in browser

## Getting Help

1. Check the error message in terminal
2. Check browser console (F12) for frontend errors
3. Review the documentation in `docs/`
4. Verify all dependencies are installed
5. Make sure ports 8000 and 3000 are available

---

**You're all set! 🎉 Start building with CryptoLib!**

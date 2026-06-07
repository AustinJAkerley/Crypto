# Local Development Setup

This guide will help you set up the CryptoLib web application on your local machine for development.

## Prerequisites

- Python 3.11 or higher
- Node.js 20 or higher
- npm or yarn
- Git

## Step-by-Step Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Crypto
```

### 2. Backend Setup

#### 2.1 Create Python Virtual Environment

```bash
cd backend
python3 -m venv venv
```

#### 2.2 Activate Virtual Environment

**On Linux/macOS:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

#### 2.3 Install Backend Dependencies

```bash
pip install -r requirements.txt
```

#### 2.4 Set Up Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

The default `.env` file is configured for local development with SQLite, so no changes are needed.

#### 2.5 Run Database Migrations

```bash
python manage.py migrate
```

#### 2.6 Create a Superuser (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

#### 2.7 Start Django Development Server

```bash
python manage.py runserver
```

The backend API will be available at `http://localhost:8000`

**Test the API:**
- Admin panel: http://localhost:8000/admin/
- API endpoints: http://localhost:8000/api/

### 3. Frontend Setup

Open a new terminal window/tab (keep the backend server running).

#### 3.1 Navigate to Frontend Directory

```bash
cd frontend
```

#### 3.2 Install Node.js Dependencies

```bash
npm install
```

#### 3.3 Start React Development Server

```bash
npm start
```

The frontend will automatically open in your browser at `http://localhost:3000`

If it doesn't open automatically, navigate to: http://localhost:3000

### 4. Using the Application

1. **Register a new account:**
   - Click "Sign up" on the login page
   - Fill in your details and create an account

2. **Access the dashboard:**
   - After registration, you'll be redirected to the dashboard
   - You'll see available crypto tools

3. **Try the crypto tools:**
   - Click on any tool card or use the "Crypto Tools" link in the navbar
   - Each tool has a dedicated tab with input forms

### 5. PyScript Browser Demo

The PyScript demo runs independently without the backend:

1. Open the file in a web browser:
   ```bash
   # From the project root
   open pyscript/index.html
   # or navigate to file:///path/to/Crypto/pyscript/index.html
   ```

2. Or serve it with a simple HTTP server:
   ```bash
   cd pyscript
   python -m http.server 8080
   # Then open http://localhost:8080
   ```

## Environment Variables Reference

### Backend (.env)

```env
# Django Settings
DJANGO_SETTINGS_MODULE=core.settings.local
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=15
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

### Frontend

For local development, the API URL defaults to `http://localhost:8000/api`.

To override, create a `.env` file in the `frontend/` directory:

```env
REACT_APP_API_URL=http://localhost:8000/api
```

## Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```bash
python manage.py runserver 8001
# Update frontend API URL accordingly
```

**Import errors with crypto library:**
Make sure you're running from the `backend/` directory, or the path insertion in `api/views.py` might not work correctly.

### Frontend Issues

**Port 3000 already in use:**
The React dev server will prompt you to use a different port. Press 'Y' to accept.

**CORS errors:**
- Make sure the backend is running on port 8000
- Check that `CORS_ALLOWED_ORIGINS` in backend settings includes `http://localhost:3000`

**API connection errors:**
- Verify the backend server is running
- Check the browser console for error messages
- Verify the API URL in `frontend/src/api/client.js`

## Development Tips

1. **Hot Reload:** Both Django and React support hot reloading. Changes to code will automatically refresh.

2. **Database Reset:** To reset the database during development:
   ```bash
   cd backend
   rm db.sqlite3
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. **View API Docs:** Use Django REST Framework's browsable API:
   - Navigate to http://localhost:8000/api/ in your browser
   - Click on any endpoint to see the interactive interface

4. **Debug Mode:** 
   - Django: Check `backend/core/settings/local.py` - DEBUG is True
   - React: Development build includes source maps

## Next Steps

- Read [staging.md](./staging.md) for deployment to a staging server
- Read [production.md](./production.md) for production deployment best practices
- Explore the crypto library in the `crypto/` directory
- Check the Django admin panel at http://localhost:8000/admin/

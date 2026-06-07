# CryptoLib Web Application

A full-stack web application built on top of the Python cryptography library, featuring a Django REST API backend, React frontend with modern Canva-style authentication UI, and PyScript integration for browser-based cryptographic operations.

## 🚀 Features

### Backend (Django REST API)
- **JWT Authentication** - Secure token-based authentication with access and refresh tokens
- **RESTful API** - Clean, well-documented endpoints for all crypto operations
- **Environment-based Settings** - Separate configurations for local, staging, and production
- **RSA Operations** - Key generation, encryption, and decryption endpoints
- **Diffie-Hellman** - Secure key exchange protocol implementation
- **CORS Support** - Configured for cross-origin requests from React frontend

### Frontend (React)
- **Modern UI** - Canva-style design with gradient backgrounds and clean forms
- **Protected Routes** - JWT-based authentication with automatic token refresh
- **Responsive Design** - Mobile-friendly interface that works on all devices
- **Interactive Crypto Tools** - Tabbed interface for different cryptographic operations
- **Real-time Results** - Instant feedback with styled result displays

### PyScript Integration
- **Browser-based Execution** - Run crypto algorithms directly in the browser
- **No Backend Required** - Standalone HTML page with embedded Python code
- **Interactive Demos** - Fast Power, Extended Euclidean Algorithm, and simple RSA
- **Educational** - Perfect for learning cryptographic concepts

## 📁 Project Structure

```
/home/runner/work/Crypto/Crypto/
├── backend/                    # Django REST API
│   ├── manage.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── core/                   # Project settings
│   │   ├── settings/
│   │   │   ├── base.py         # Shared settings
│   │   │   ├── local.py        # Development settings
│   │   │   ├── staging.py      # Staging settings
│   │   │   └── production.py   # Production settings
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── api/                    # API application
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
├── frontend/                   # React application
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── components/
│       │   ├── Auth/           # Login & Register
│       │   ├── Dashboard/      # Main dashboard
│       │   ├── Crypto/         # Crypto tools
│       │   └── Layout/         # Navbar
│       ├── context/            # Auth context
│       ├── api/                # API client
│       ├── App.js
│       └── index.js
├── pyscript/                   # PyScript demo
│   └── index.html
├── docs/                       # Documentation
│   ├── local.md                # Local development
│   ├── staging.md              # Staging deployment
│   └── production.md           # Production deployment
└── crypto/                     # Original crypto library
```

## 🎯 Quick Start

See detailed guides in the `docs/` directory:
- [Local Development Setup](./docs/local.md)
- [Staging Deployment](./docs/staging.md)
- [Production Deployment](./docs/production.md)

### Local Development (TL;DR)

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

**Access:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

## 🔐 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/token/refresh/` - Refresh access token
- `GET /api/auth/me/` - Get current user info (requires auth)

### Cryptographic Operations (All require JWT authentication)
- `POST /api/crypto/rsa/keygen/` - Generate RSA key pair
- `POST /api/crypto/rsa/encrypt/` - Encrypt with RSA
- `POST /api/crypto/rsa/decrypt/` - Decrypt with RSA
- `POST /api/crypto/dh/exchange/` - Diffie-Hellman key exchange

## 🎨 Design Features

### Canva-Style Authentication
- **Split-screen layout** with gradient brand panel
- **Modern form design** with rounded inputs and focus states
- **Purple gradient theme** (`#7c3aed` to `#4f46e5` to `#2563eb`)
- **Smooth animations** and hover effects
- **Responsive** for mobile and desktop

### Dashboard
- **Welcome section** with personalized greeting
- **Card grid** for crypto tool selection
- **Clean navigation** with navbar and logout
- **Consistent styling** across all pages

### Crypto Tools
- **Tabbed interface** for different operations
- **Form validation** with error handling
- **Result display** in styled code blocks
- **Loading states** for async operations

## 🛠️ Technologies Used

### Backend
- Django 4.2.16
- Django REST Framework 3.15.2
- djangorestframework-simplejwt 5.3.1
- django-cors-headers 4.4.0
- PostgreSQL (production) / SQLite (development)
- Gunicorn (production)

### Frontend
- React 18.2.0
- React Router DOM 6.22.0
- Axios 1.6.7
- Inter font family

### PyScript
- PyScript 2024.11.1
- Embedded Python algorithms

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

1. **[local.md](./docs/local.md)** - Complete local development setup
   - Prerequisites and system requirements
   - Step-by-step installation
   - Environment configuration
   - Troubleshooting guide

2. **[staging.md](./docs/staging.md)** - Staging server deployment
   - Server setup and configuration
   - PostgreSQL database setup
   - Nginx and Gunicorn configuration
   - SSL certificate setup

3. **[production.md](./docs/production.md)** - Production best practices
   - Security hardening
   - Database backups
   - Monitoring and logging
   - Performance optimization
   - Docker deployment option

## 🔒 Security Features

- **JWT Authentication** with access and refresh tokens
- **Password hashing** using Django's secure defaults
- **CORS configuration** to prevent unauthorized access
- **HTTPS enforcement** in production
- **CSRF protection** enabled
- **Security headers** (HSTS, X-Frame-Options, etc.)
- **Environment variable management** for secrets

## 🧪 Testing

### Test the PyScript Page
Open `pyscript/index.html` in a browser or serve with:
```bash
cd pyscript
python -m http.server 8080
# Visit http://localhost:8080
```

### Test API Endpoints
Use the Django REST Framework browsable API:
```bash
# Start the backend server
cd backend
python manage.py runserver

# Visit http://localhost:8000/api/ in your browser
```

## 📝 Environment Variables

### Backend (.env)
```env
DJANGO_SETTINGS_MODULE=core.settings.local
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=crypto_db
DB_USER=crypto_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
CORS_ALLOWED_ORIGINS=http://localhost:3000
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=15
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

### Frontend (.env) - Optional
```env
REACT_APP_API_URL=http://localhost:8000/api
```

## 🤝 Contributing

This is a demonstration project. For production use:
1. Review and update security settings
2. Implement comprehensive testing
3. Add input validation and sanitization
4. Set up monitoring and logging
5. Configure automated backups

## 📄 License

This project uses the crypto library which may have its own license. Please review the main project license before deploying.

## 🆘 Support

For issues or questions:
1. Check the documentation in `docs/`
2. Review Django and React error logs
3. Verify environment configuration
4. Check CORS and network settings

## 🎓 Educational Use

This application is built on top of an educational cryptography library. The implementations are for learning purposes. For production cryptographic needs, use established libraries like:
- `cryptography` (Python)
- `PyCryptodome`
- OpenSSL

## 📊 Status

✅ **Completed Features:**
- Full Django REST API backend
- React frontend with authentication
- JWT token management
- RSA key generation, encryption, decryption
- Diffie-Hellman key exchange
- PyScript browser demo
- Comprehensive documentation
- Environment-based configuration

## 🚦 Next Steps

After setup, consider:
1. Adding more cryptographic algorithms (ECC, DSA)
2. Implementing file upload/download for key management
3. Adding 2FA for enhanced security
4. Creating API documentation with Swagger/OpenAPI
5. Implementing rate limiting
6. Adding unit and integration tests

---

**Built with ❤️ using Django, React, and PyScript**

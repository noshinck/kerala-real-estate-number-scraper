# DataHarvest - Complete Setup Guide

## 📁 Project Structure

```
dataharvest/
├── frontend/
│   └── index.html          # Web interface
├── backend/
│   ├── app.py             # Flask API
│   └── requirements.txt    # Python dependencies
└── SETUP.md               # This file
```

---

## 🚀 Quick Start

### Step 1: Setup Backend (Python Flask)

1. **Create backend folder:**
```bash
mkdir dataharvest
cd dataharvest
mkdir backend
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv

# Activate (Mac/Linux):
source venv/bin/activate

# Activate (Windows):
venv\Scripts\activate
```

3. **Save `app.py` and `requirements.txt` in backend folder**

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Run the backend:**
```bash
python app.py
```

Backend will run on `http://localhost:5000`

---

### Step 2: Setup Frontend

1. **Create frontend folder:**
```bash
cd ..  # Go back to dataharvest folder
mkdir frontend
cd frontend
```

2. **Save `index.html` in frontend folder**

3. **Open in browser:**
   - Simply double-click `index.html`
   - OR use a local server:
   ```bash
   python -m http.server 8000
   ```
   Then visit: `http://localhost:8000`

---

## 🌐 Deployment

### Option 1: Deploy Backend to Heroku (Free)

1. **Install Heroku CLI:**
```bash
# Mac
brew install heroku

# Windows/Linux
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Create `Procfile` in backend folder:**
```
web: gunicorn app:app
```

3. **Add gunicorn to requirements.txt:**
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

4. **Deploy:**
```bash
cd backend
heroku login
heroku create dataharvest-api
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

5. **Get your API URL:**
```bash
heroku open
```
Your API will be at: `https://dataharvest-api.herokuapp.com`

6. **Update frontend:**
   - Open `index.html`
   - Change `API_URL` from `http://localhost:5000` to your Heroku URL

---

### Option 2: Deploy Frontend to Netlify (Free)

1. **Go to [Netlify](https://www.netlify.com/)**
2. **Sign up/Login**
3. **Drag and drop** your `index.html` file
4. **Done!** Your site is live

---

### Option 3: Deploy Both on Railway (Free)

1. **Go to [Railway.app](https://railway.app/)**
2. **Create new project**
3. **Deploy from GitHub:**
   - Push your code to GitHub
   - Connect Railway to your repo
   - Railway will auto-detect Flask and deploy

---

## 🔧 Configuration

### Update API URL in Frontend

In `index.html`, find this line:
```javascript
const API_URL = 'http://localhost:5000/api/extract';
```

Change to your deployed backend URL:
```javascript
const API_URL = 'https://your-backend.herokuapp.com/api/extract';
```

### Increase Record Limit

In `backend/app.py`, change max limit:
```python
if not isinstance(limit, int) or limit < 1 or limit > 500:  # Change 200 to 500
```

In `frontend/index.html`, add more options:
```html
<option value="500">500 Records</option>
<option value="all">All Records</option>
```

---

## 🌍 Adding More Languages

### Add Language Selector to Frontend

In `index.html`, add this after the form:

```html
<div class="form-group">
    <label class="form-label">LANGUAGE</label>
    <select class="form-select" id="language">
        <option value="en">English</option>
        <option value="ml">Malayalam</option>
        <option value="hi">Hindi</option>
    </select>
</div>
```

### Create Translation Object

Add to the `<script>` section:

```javascript
const translations = {
    en: {
        title: "DataHarvest",
        subtitle: "EXTRACT · ORGANIZE · EXCEL",
        button: "START EXTRACTING"
    },
    ml: {
        title: "ഡാറ്റാഹാർവെസ്റ്റ്",
        subtitle: "എക്സ്ട്രാക്ട് · ഓർഗനൈസ് · എക്സൽ",
        button: "എക്സ്ട്രാക്ഷൻ ആരംഭിക്കുക"
    },
    hi: {
        title: "डेटाहार्वेस्ट",
        subtitle: "निकालें · व्यवस्थित करें · उत्कृष्टता",
        button: "निष्कर्षण शुरू करें"
    }
};

function changeLanguage(lang) {
    document.querySelector('.hero-title span').textContent = translations[lang].title;
    document.querySelector('.hero-subtitle').textContent = translations[lang].subtitle;
    document.querySelector('.cta-button').textContent = translations[lang].button;
}

// Add event listener
document.getElementById('language').addEventListener('change', (e) => {
    changeLanguage(e.target.value);
});
```

---

## 🐛 Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
pip install -r requirements.txt
```

### ChromeDriver issues

**Error**: `ChromeDriver version mismatch`

**Solution**: webdriver-manager auto-downloads. If issues persist:
```bash
pip install --upgrade webdriver-manager
```

### CORS errors in browser

**Error**: `Access-Control-Allow-Origin`

**Solution**: Backend already has CORS enabled. If still having issues:
```bash
pip install flask-cors
```

Then verify in `app.py`:
```python
from flask_cors import CORS
CORS(app)
```

### Frontend can't connect to backend

**Check**:
1. Backend is running: Visit `http://localhost:5000/api/health`
2. API_URL is correct in frontend
3. No firewall blocking port 5000

---

## 📊 API Documentation

### Endpoints

#### 1. Extract Data
```
POST /api/extract
```

**Request:**
```json
{
  "source": "kerala-rera",
  "limit": 50
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "name": "Rajesh Kumar",
      "phone": "+919876543210",
      "email": "rajesh@example.com",
      "address": "Ernakulam, Kerala",
      "category": "Individual"
    }
  ],
  "stats": {
    "total": 50,
    "with_email": 45,
    "with_phone": 48,
    "with_address": 42
  }
}
```

#### 2. Health Check
```
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "DataHarvest API"
}
```

#### 3. Get Sources
```
GET /api/sources
```

**Response:**
```json
{
  "sources": [
    {
      "id": "kerala-rera",
      "name": "Kerala RERA Agents",
      "max_records": 823
    }
  ]
}
```

---

## 🔐 Security Notes

1. **API Rate Limiting**: Add rate limiting in production
2. **Authentication**: Add API keys for production use
3. **HTTPS**: Always use HTTPS in production
4. **Environment Variables**: Store sensitive config in .env files

---

## 📝 License

MIT License - Free to use and modify

---

## 🤝 Support

For issues or questions:
1. Check this setup guide
2. Review error logs
3. Test API endpoints directly

---

## ✅ Checklist

- [ ] Backend running on port 5000
- [ ] Frontend opens in browser
- [ ] API_URL correctly configured
- [ ] Test extraction with 10 records
- [ ] CSV download works
- [ ] Ready to deploy!

---

**You're all set! 🚀**
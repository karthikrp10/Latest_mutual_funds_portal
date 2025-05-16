**Latest_mutual_funds_portal**
A simple Mutual Fund Portal built with FastAPI and vanilla JavaScript. Allows users to register, login, and view open-ended mutual fund schemes fetched via the RapidAPI Mutual Fund NAV API. Includes JWT-based authentication and real-time fund filtering by RTA agent (CAMS, KARVY).

**Mutual Fund Portal**

A secure and interactive web application that allows users to register, log in, and view mutual fund portfolio data (CAMS/KARVY) in real-time.

**Set up MongoDB (required)**
sudo systemctl start mongod

**Features**
- User registration and login with JWT authentication
- Fund house selection (CAMS or KARVY)
- Portfolio loading after authentication
- Dynamic UI with secure token handling
- Backend powered by FastAPI and MongoDB
- Frontend built with HTML, CSS, and Vanilla JS

**Preview image**

![Mutual Fund Portal Preview](static/barebull.png)

**Tech Stack**


Backend - FastAPI, Uvicorn
Auth    - JWT (PyJWT) 
Database - MongoDB (No Auth)
Frontend  - HTML, CSS, JS
External API - RapidAPI (NAVs)

**Installation & Run**
``bash
git clone https://github.com/karthikrp10/Latest_mutual_funds_portal.git
cd Latest_mutual_funds_portal

**Project Structure**

main.py # FastAPI application entry point
auth.py # Authentication (register, login)
funds.py # Fund-related routes
static/
- index.html # Frontend UI (login/register/dashboard)
- barebull.png # Background image
templates/
- dashboard.html # Optional Jinja2 page
requirements.txt


**Create virtual environment and install dependencies**
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
- pip install "jinja2<3.1" # should be below 3.1 version


**Run the server**
uvicorn main:app --reload or run main.py


**Usage**
1.Open your browser at http://localhost:8000

2.Register a new account or login

3.Select a fund house (CAMS / KARVY)

4.Click Load Funds to view your portfolio


**Environment Variables**
**You can define these in your environment or .env file:**
RAPIDAPI_KEY=your_rapidapi_key
RAPIDAPI_HOST=latest-mutual-fund-nav.p.rapidapi.com
SECRET_KEY=your_jwt_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
MONGO_HOST=localhost
MONGO_PORT=27017

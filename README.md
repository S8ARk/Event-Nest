# College Event Recommendation System (CERS)

Welcome to CERS! This guide will help you launch the application from scratch on your local machine.

## Prerequisites
Make sure you have **Python 3.8+** installed on your system. 

## 0 to 1: Startup Guide

Follow these steps in your terminal (Command Prompt or PowerShell) to get the application running:

### Step 1: Open the Project
Open your terminal and navigate to the project directory:
```bash
cd path\to\PROJECT
```

### Step 2: Create a Virtual Environment (Recommended)
It's best practice to run Python apps in an isolated environment.
```bash
# Create the virtual environment named 'venv'
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# If you are on Mac/Linux, use:
# source venv/bin/activate
```

### Step 3: Install Dependencies
Install all required libraries, including Flask, SQLAlchemy, and NLTK.
```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables
Create a file named `.env` in the root folder of the project if it doesn't exist, and add a secret key:
```env
SECRET_KEY=your_super_secret_key_here
```

### Step 5: Run the Application
Start the Flask development server. This command will automatically create the local SQLite database (`instance/cers.db`) and seed it with starter data (Categories, Interests, and an Admin user).
```bash
python run.py
```

### Step 6: Explore!
Open your web browser and go to:
**http://127.0.0.1:5000**

---

### 🔑 Test Accounts
The database automatically seeds an Admin account on its first run. You can use this to instantly explore the system:
- **Email:** `admin@cers.edu`
- **Password:** `admin123`

To test the core features, you can click **Sign Up** to create a new `Student` account or `Organizer` account!

# College Event Recommendation System (V2)

Welcome to CERS V2! This radically modernized application acts as an intelligent event discovery engine leveraging Python, Flask, an NLTK Artificial Intelligence algorithm, modern MVC Service Architectures, and Glassmorphism UI styling rules.

## Prerequisites
Make sure you have **Python 3.8+** installed on your system. Due to the new DevOps security upgrades, you will also need to generate a local configuration matrix.

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

### Step 4: Setup Environment Variables (VITAL for V2 Security)
Create a file strictly named `.env` in the root folder of the project. You must supply a cryptographically generated string to satisfy the DevOps safety mechanisms:
```env
SECRET_KEY=your_super_secret_key_here
# Optional Constants:
MIN_SCORE_THRESHOLD=15.0
```

### Step 5: Run the Application
Start the Flask development server. This command will autonomously trigger the NLTK Corpus generator to download the NLP library cores, build the local SQLite database (`instance/cers.db`), and seed it with starter data (Categories, Interests, and an Admin user).
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

# College Event Recommendation System (CERS)
## System Architecture & Security Handover Document

### 1. Architecture & Tech Stack Interaction

**Front-End to Back-End Communication**
CERS utilizes a Server-Side Rendering (SSR) architecture pattern. 
- **Front-End:** Written in Vanilla HTML/CSS with Jinja2 templating.
- **Back-End:** Python/Flask. 
When a user navigates to a URL, the Flask router (`app/routes/`) intercepts the HTTP GET request and passes data contexts to Jinja2 (`app/templates/`), which compiles the final HTML string delivered to the browser.
Forms are constructed via `Flask-WTF` forms. When a user submits data, an HTTP POST request sends the payload back to Flask. WTForms securely validates the payload on the server side before the data ever touches the SQL ORM.

**NLP Request Lifecycle**
The Natural Language Processing runs asynchronously to the main CRUD operations to avoid blocking standard web traffic:
1. **Extraction Phase:** When an Event Admin creates or edits an Event (`POST /events/create`), `app/services/nlp_utils.py` uses `nltk` to strip stopwords and tokenize the large text description into core semantic keywords. These are saved to the Event's `keywords` column.
2. **Scoring Phase:** When a Student updates their Profile Interests, or logs into their Dashboard, the `recommender.py` service invokes. It loads the Student's interest tokens and calculates the mathematical overlap percentage against all active Event keywords. 
3. **Caching:** To keep the dashboard lightning-fast, the top 10 results are cached in the `InteractionModel.Recommendation` table. The Dashboard template simply queries this pre-calculated cache.

---

### 2. Data Storage & Schema (DFD Mapping)

**Storage Mechanism**
Currently, data is stored locally in a file-based relational database: `instance/cers.db`. It interacts with the Python code via `Flask-SQLAlchemy`, which translates Python object manipulations into raw SQL queries.

**Entity-Relationship (ER) Overview**
- **User (1) ↔ (Many) Event:** 
  An *Organizer* (User) is the foreign-key owner (`organizer_id`) of multiple Events.
- **User (Many) ↔ (Many) Event (via Registration):** 
  A *Student* (User) RSVPs to Events. Because a student can attend many events, and an event can have many students, we resolve this many-to-many relationship using the `Registration` associative table.
- **Category (1) ↔ (Many) Event:** 
  Every Event maps strictly to one predefined Category (e.g., "Technology").
- **User ↔ Profile Attributes:** 
  Students map 1-to-many to `UserInterest` (what they like) and 1-to-many to `Recommendation` (the AI's cached suggestions for them).

---

### 3. Authentication & Security

**Password Protection**
Passwords are never stored in plaintext. When a user submits the Registration form, `Flask-Bcrypt` hashes the password using a computational blowfish cipher algorithm combined with a randomly generated "salt" (`bcrypt.generate_password_hash()`). If the database is compromised, hackers cannot reverse-engineer the stored hashes back into readable passwords.

**Privilege Separation (Student vs. Admin)**
CERS maintains a single `User` table but differentiates access using the `role` string column (`student`, `organizer`, `admin`). 
We enforce security at the endpoint level using Python decorators (`@role_required`). For example, the `events.create` route is decorated with `@role_required('organizer')`. Before the view logic executes, the decorator intercepts the request, checks `current_user.role`, and throws a `403 Forbidden` error if a student tries to manually type the URL to bypass the UI.

**Session Hijacking & CSRF Prevention**
1. **Session Management:** Handled by `Flask-Login`. The session token is stored in the browser as a cryptographically signed cookie. Because the cookie is signed using the application's `SECRET_KEY`, if a user attempts to tamper with the cookie payload to hijack another account, the cryptographic signature check will fail, and Flask will immediately invalidate the session.
2. **CSRF Protection:** `Flask-WTF` automatically injects a hidden, randomized CSRF token into every rendered HTML form. When the POST request hits the server, Flask verifies the token against the active session before processing the data, making Cross-Site Request Forgery impossible.

---

### 4. Deployment & CI/CD Pipelines

**Migration to a Live Server**
To move this from your local Windows machine to a live Linux server (e.g., AWS EC2, DigitalOcean, Heroku):
1. **Provision Infrastructure:** Spin up a cloud server and install Python.
2. **Environment Variables:** Create a remote `.env` file containing a complex `SECRET_KEY` and a production database URL.
3. **Version Control:** `git clone` the repository onto the server.
4. **Dependencies:** Create a Virtual Environment (`venv`) and run `pip install -r requirements.txt`.
5. **Database:** (Optional) Swap SQLite for a robust concurrent relational database like **PostgreSQL**, updating the `DATABASE_URL`.
6. **Daemonize:** Configure a process manager like `Systemd` or `Supervisor` to keep the application running continuously in the background.

**Production WSGI Server**
The built-in Flask server (`app.run()`) is meant exclusively for local development; it processes one request at a time. For production, you must use a WSGI server like **Gunicorn** (for Linux) or **Waitress** (for Windows). Gunicorn utilizes asynchronous "worker pathways" to handle hundreds of concurrent user requests. 
*Architecture:* **Nginx** (Reverse Proxy) → **Gunicorn** (WSGI) → **Flask** (App).

**Database Migrations (Schema Changes)**
If you need to add a new column (e.g., `phone_number` to `User`) while the app is live with thousands of users, you cannot drop and recreate the table without data loss. 
You will integrate **Flask-Migrate** (built on Alembic):
1. Run `flask db init` (once, to set up tracking).
2. Modify your Python model classes.
3. Run `flask db migrate -m "added phone number"`. The system generates an SQL difference file.
4. Run `flask db upgrade` on the production server. This safely injects the new column into the live database without touching the existing records.

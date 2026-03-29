# College Event Recommendation System (V2)
## Feature Capability & System Handover Overview

**Project Lead/Developer:** Phase 2 Modernization Completed
**Architecture State:** MVC Isolated Services / DevOps Secured

---

### 1. PLATFORM CAPABILITY DISCLOSURE
The newly overhauled CERS acts as an incredibly smart, predictive platform designed to unify university communities by automatically curating and projecting relevant administrative events directly onto specific student dashboards using artificial intelligence logic.

#### Key Features Deployed
*   **Mandatory User Onboarding Matrix:** A sophisticated middleware wall that prevents newly registered students from accessing the platform until they have visually selected their core university interests (Computer Science, Music, Sports, etc.).
*   **Real-Time AI Recommendations:** A dynamic system that runs Python Natural Language Algorithms in the background instantly the moment a student loads their dashboard or an admin creates a new event.
*   **Secure Service Abstractions:** Advanced MVC routing that isolates database security limits (e.g., maximum event capacity rules) into untouchable Python services, drastically lowering the vulnerability to web attack.
*   **Dynamic Glassmorphism UI:** A highly modern, beautifully styled frontend system powered by decoupled CSS variables, transparent scroll-responsive navigation bars, auto-dimming dark modes, and floating toast verification interfaces.

---

### 2. PRIMARY USE CASES & SYSTEM ACTORS

#### Use Case 1: The Student "Discovery" Experience
1. Student navigates to the portal and signs up natively via an encrypted bcrypt workflow.
2. The system intercepts the URL and forces the Student through an aesthetic grid of floating Interest cards.
3. Upon finalizing preferences, the dashboard renders. The backend instantly queries all globally active college events, lemmatizes their core descriptions, scores them against the Student's weighted interest tokens, and dynamically prints the top 10 ranked events onto the `Recommended for You` section.
4. The Student seamlessly RSVPs in one click, updating the database capacity live.

#### Use Case 2: The Organizer "Publishing" Engine
1. A faculty member logs in securely as an `Organizer` via predefined permissions.
2. They access the `Create Event` controller.
3. Upon publishing a highly descriptive tech summit event, the `NLP_Utils` Service layer silently intercepts the event in the background. It utilizes the sophisticated `nltk` library to strip meaningless verbs and adverbs, transforming the giant paragraph into semantic anchor keys (e.g., `['computer', 'technology', 'learn', 'hardware']`) and saves these to the hidden backend.
4. The event instantly trickles through the entire global application feed, automatically pinging the dashboards of hundreds of students who overlap mathematically with the generated nouns. 

---

### 3. ARCHITECTURE DEPLOYMENT & OPERATION 
If you are moving to operate this system as a system administrator, you must understand the new structural mandates in V2:

#### The Application "Brain" (Services Directory)
Do not modify the web routes for database calculation changes! All logic determining whether an event is successfully created, deleted, or whether a student is allowed to RSVP is locked safely within `app/services/event_service.py` and `app/services/registration_service.py`. The web files (`app/routes`) solely handle HTML templates.

#### The DevOps `.env` Environment Sequence
The application is structurally locked behind environmental variables out of a strict security necessity.
If you clone this project onto a new machine, **it will intentionally crash on boot** unless you specifically fulfill the DevOps environment template `.env.example` by creating a `.env` file holding a unique cryptographic `SECRET_KEY`. 

#### The Asset Pipeline (CSS/JS)
The massive chunks of HTML inline styles and scripts have been structurally decoupled. If you desire to change the color palette (the glassmorphism styling) or the Javascript rendering (toast notifications / Dark Mode calculations), you only need to modify `app/static/css/main.css` and `app/static/js/main.js`. Editing those single files governs the UI for the entire application platform globally utilizing intense browser caching metrics.

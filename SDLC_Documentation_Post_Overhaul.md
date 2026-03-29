# COLLEGE EVENT RECOMMENDATION SYSTEM (V2)
## Software Development Lifecycle (SDLC) Post-Overhaul Documentation

**Document Version:** 2.0 (Post-Overhaul)  
**Date:** March 2026  
**Project Status:** Phase 2 Complete (Architecture, AI, & UI Overhaul)  
**Tech Stack:** Python (Flask, NLTK), SQLite/PostgreSQL, Tailwind CSS (Vanilla JS), MVC Service Architecture

---

## 1. POST-OVERHAUL EXECUTIVE SUMMARY
The **College Event Recommendation System (CERS)** has evolved from a rudimentary proof-of-concept into a structurally fortified, robust, and mathematically sound web application. In Phase 2, the monolithic "Fat Controller" structure was gutted in favor of a Service Layer architecture, scaling the application from a small experiment to a professional, testable, enterprise-level platform. 

### Critical Milestones Achieved
1. **AI Upgrade:** Pivoted from basic set-intersection word matching to a Weighted Frequency Distribution Engine leveraging Python's NLTK (Lemmatization & POS Tagging).
2. **Structural Redesign:** Migrated raw database access out of the web routers into dedicated isolated Python Services (`event_service.py` & `registration_service.py`).
3. **Frontend Overhaul:** Deprecated the boring native DOM elements for modern "Glassmorphism" UI paradigms, autonomous toast notifications, and decoupled static `.js`/`.css` assets to skyrocket browser caching efficiency.
4. **Security Hardening:** Eradicated hardcoded cryptographic keys and AI thresholds, replacing them with a strict `.env` configuration mandate to enforce DevOps standards.

---

## 2. REQUIREMENT ANALYSIS & REFINEMENT (V2)

### 2.1 Post-Overhaul Functional Adjustments
- **FR-1: Mandatory User Onboarding (Completed):** 
  Newly registered students are successfully intercepted by the `@requires_onboarding` middleware, forcing them to map their Interest attributes to prevent the NLTK engine from stalling via "cold-start" blank states.
- **FR-2: AI Real-Time Feedback Loop (Completed):**
  Recommendations no longer require manual profile saves. A systematic regeneration trigger is natively hooked into the `user.dashboard` route to dynamically re-calculate overlap percentages the instant new events are posted to the database.

### 2.2 Data Flow & Architectural Design Adjustments
**Level 1 DFD: The MVC Service Paradigm**
In the V1 design, the UI directly negotiated with the SQL Database through the Web Router. In V2, the Web Router acts strictly as a traffic controller, delegating massive computational jobs:
```
[User Interface] --HTTP POST--> [events.py ROUTER] 
                                    |
                                    v
                           [event_service.py] <----- [nlp_utils.py NLTK Engine]
                                    |
                                    v
                           [SQLAlchemy ORM DB]
```
This multi-tier approach mathematically guarantees that the NLTK calculation engine can be modified in the future without risking any damage to the web interface or database structures.

---

## 3. IMPLEMENTATION & CODE QUALITY

### 3.1 NLTK Weighted Frequency Engine
The baseline set-intersection code was entirely ripped out. We implemented an incredibly scalable natural language sequence:
1. **Lemmatize Definitions:** Reduces plural words ("Computers") to their absolute root lemma ("Computer") to prevent fragmented matching scores.
2. **Part-of-Speech Tagging Filtering:** Automatically drops useless verbs and adverbs, focusing the matching percentages exclusively on Substantive Nouns and Adjectives.
3. **Weight Overlap Scaling:** Multiplies the structural term frequency of event words against the explicit priority weight variable assigned to the individual Student, creating a drastically precise relevance ranking.

### 3.2 Code Quality Formats
- Formatted standard Google-style docstrings comprehensively across the routing matrices.
- Leveraged strict `Exception` handling loops across all HTTP transaction blocks to prevent crashes during bad database insertions.

---

## 4. VALIDATION & TESTING STRATEGIES

With the monolithic Fat Controllers dismantled, the test suite (`pytest`) was aggressively rewritten to target the raw `app/services/` layer independently of the Flask framework context.

**Testing Matrix Validations:**
- **NLP Mock Asserts:** The mathematical algorithms were mapped against edge-case heavy strings (e.g. trailing punctuations, complex nouns) to ensure the weight algorithm returns an expected fractional percentage.
- **MVC Route Verification:** Confirmed that endpoints return explicit `403 Forbidden` error hierarchies if a Student maliciously leverages an Organizer routing URL. All 6 primary application test routines exited with Code 0.

---

## 5. FUTURE ROADMAP (PHASE 3: ENTERPRISE DEPLOYABILITY)

While the code architecture is now flawless, preparing CERS to become a **Full-Fledged University Level Application (Standalone Software As A Service)** requires three massive evolutionary finalities:

### 5.1 The Move to PostgreSQL
SQLite is incredibly fast locally but physically cannot handle multiple concurrent student registrations simultaneously (Database Locking). The final pre-deployment step revolves around mapping the codebase directly to a clustered PostgreSQL database server on the Cloud to guarantee synchronous reliability when 10,000 students log in during Welcome Week.

### 5.2 Microservice Containerization (Docker)
To package CERS as a standalone application that any university IT Administration branch can download and run independently, we must write a `Dockerfile` and `docker-compose.yaml`. This will lock the Flask app, the NLTK libraries, and the database server into isolated OS containers, allowing instantaneous installation across the globe without dependency nightmares.

### 5.3 Advanced Machine Learning (ML) Integration
The NLTK Weighted Token engine is incredibly precise for structural classification, but the ultimate future implementation includes true unsupervised learning:
- Swapping the TF matching algorithm for **Scikit-Learn Consine Similarity** matrices.
- Injecting collaborative filtering: If 15 students all go to the exact same Event A and Event B, the backend should train itself to blindly recommend Event B to anyone joining Event A without relying solely on category string overlap.

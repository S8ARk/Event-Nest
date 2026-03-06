# COLLEGE EVENT RECOMMENDATION SYSTEM
## Software Development Lifecycle Documentation
### Early-Phase Requirements Analysis & System Design

**Document Version:** 1.0  
**Date:** January 2026  
**Project Status:** Requirements & Design Phase  
**Target Complexity:** Intermediate  
**Tech Stack:** Python (Flask, NLTK), SQLite, Vanilla Frontend

---

## EXECUTIVE SUMMARY

### Project Overview
The **College Event Recommendation System (CERS)** is a web-based platform designed to solve the critical problem of scattered event information across college campuses. The system intelligently matches student interests with relevant college events, increasing participation and engagement through personalized recommendations powered by basic NLP techniques.

### Problem Statement
- **Current State:** Event information scattered across multiple channels (WhatsApp, email, notice boards)
- **Impact:** Low awareness → reduced student participation → underutilized events
- **Root Cause:** No centralized platform with intelligent discovery mechanism
- **Solution Scope:** Build a unified event hub with keyword-matching recommendations using NLTK

### Business Objectives
1. Centralize college event information in one accessible platform
2. Increase event discoverability through personalized recommendations
3. Improve student participation by 30-40% (target metric)
4. Demonstrate AI/NLP integration in real-world application
5. Create scalable architecture for multi-college future expansion

### Key Stakeholders
- **Students:** End users seeking event discovery
- **Event Organizers:** Faculty/clubs managing event creation
- **Admin Panel:** College authorities managing platform
- **Development Team:** 4-member student team implementing system

---

## 1. REQUIREMENT ANALYSIS & REFINEMENT

### 1.1 Functional Requirements

#### F1: Event Management (Admin/Organizer Role)
- **F1.1:** Create new event with title, description, category, date, time, location
- **F1.2:** Edit event details (category, description, timing updates)
- **F1.3:** Delete/archive past events
- **F1.4:** View event registration statistics
- **F1.5:** Publish/unpublish events

**Priority:** Critical | **Complexity:** Low

#### F2: Event Discovery & Browsing (Student Role)
- **F2.1:** View all upcoming events in grid/list format
- **F2.2:** Filter events by category (Academic, Sports, Cultural, Tech, Social)
- **F2.3:** Search events by keyword
- **F2.4:** View detailed event information page
- **F2.5:** Sort by date, popularity, recency

**Priority:** Critical | **Complexity:** Low-Medium

#### F3: Personalized Recommendation Engine (Core AI Feature)
- **F3.1:** Analyze student profile (registered interests)
- **F3.2:** Match student interests with event content using NLTK keyword extraction
- **F3.3:** Generate ranked event recommendations
- **F3.4:** Display top 5-10 recommendations on student dashboard
- **F3.5:** Learn from student interactions (clicks, registrations)

**Priority:** Critical | **Complexity:** Medium

#### F4: User Registration & Authentication
- **F4.1:** Student signup with email and basic profile
- **F4.2:** Organizer/admin registration (college email verification)
- **F4.3:** Login functionality with session management
- **F4.4:** Profile management (interest selection/update)
- **F4.5:** Password recovery

**Priority:** High | **Complexity:** Low-Medium

#### F5: Event Registration & RSVP
- **F5.1:** Register for events (RSVP)
- **F5.2:** View registered events in "My Events"
- **F5.3:** Cancel registration
- **F5.4:** View registration count per event

**Priority:** High | **Complexity:** Low

#### F6: Notification System
- **F6.1:** Email notifications for recommended events (optional)
- **F6.2:** In-app notifications for registrations
- **F6.3:** Event reminders 24 hours before event

**Priority:** Medium | **Complexity:** Low-Medium

#### F7: Analytics Dashboard (Admin)
- **F7.1:** View total events, registrations, popular categories
- **F7.2:** Track student participation trends
- **F7.3:** Recommendation accuracy metrics
- **F7.4:** Export reports

**Priority:** Medium | **Complexity:** Medium

---

### 1.2 Non-Functional Requirements

| Requirement | Specification | Rationale |
|------------|--------------|-----------|
| **Performance** | Page load time < 2 seconds; recommendation generation < 1 second | User experience critical for adoption |
| **Scalability** | Support 5000+ students, 500+ events | Future multi-college expansion |
| **Availability** | 99% uptime during college hours | Campus-wide dependency |
| **Security** | Password hashing (bcrypt), session tokens, SQL injection prevention | Student data protection |
| **Usability** | Mobile-responsive UI, intuitive navigation | Diverse student tech literacy |
| **Maintainability** | Clean code, modular architecture, documented API | Team collaboration & handoff |
| **Data Retention** | Archive past events for historical analysis | Alumni engagement potential |

---

### 1.3 System Constraints & Assumptions

#### Technical Constraints
- **Technology Stack:** Fixed (Flask, SQLite, Vanilla JS, NLTK)
- **No Advanced ML:** Basic keyword matching only (no deep learning)
- **Single-Tier Deployment:** Single server (not cloud-distributed initially)
- **No Real-time:** Batch recommendation updates (hourly/daily)

#### Business Constraints
- **Development Timeline:** 12-16 weeks (semester-long project)
- **Team Size:** 4 members with varying expertise
- **Testing Scope:** Unit + integration testing (no formal QA team)
- **Documentation:** Academic + professional standards

#### Assumptions
- Assume stable college internet connectivity
- Assume 70% student device smartphone/laptop access
- Assume event organizers provide accurate descriptions
- Assume NLTK keyword extraction sufficient for MVP (no transformer models)

---

### 1.4 Refined Requirements Summary

**Must-Have (MVP):**
- Event CRUD operations
- Student event browsing & search
- Basic personalized recommendations (NLTK keyword matching)
- User authentication
- Event registration RSVP

**Should-Have:**
- Interest profile management
- Analytics dashboard
- Notification system
- Advanced filtering options

**Nice-to-Have:**
- Social sharing features
- Event ratings & reviews
- Calendar integration
- Mobile app version

---

## 2. REQUIREMENT MODELLING: DIAGRAMS & VISUALIZATIONS

### 2.1 Data Flow Diagram (DFD)

#### Level 0: Context Diagram
```
┌─────────────────────────────────────────────────┐
│                                                 │
│    Student         Event Data      Admin        │
│      │                │              │          │
│      └─────────────────┴──────────────┘         │
│              │                                  │
│         [CERS System]                           │
│              │                                  │
│      ┌───────┴───────────────────┐             │
│      │                           │              │
│   Recommendations        Event Information     │
│   & Notifications       & Statistics           │
│      │                           │              │
│      └─────────────────┬─────────┘              │
│              │                                  │
│         Student & Organizer                    │
│              │                                  │
└─────────────────────────────────────────────────┘
```

#### Level 1: DFD - Main Processes
```
                    ┌─── D1: User Database ──┐
                    │                        │
        1.0         │                        │
    ┌───────────────┼─ Student Login ────────┼──┐
    │               │                        │  │
Student │            └────────────────────────┘  │
    │   │                                        │
    │   │    2.0 ┌──────────────────────┐      │
    │   │    Event ├─ D2: Event DB       │      │
    │   └───►Discovery├────────────────────┤      │
    │        │      │ - Events          │      │
    │        │      │ - Categories      │      │
    │        │      │ - Registrations   │      │
    │        └──────┤                    │◄─────┘
    │               └────────────────────┘
    │                        │
    │     ┌──────────────────┘
    │     │
    │     ▼
    │  3.0 ┌────────────────────────┐
    │  Recommendation├─ D3: User Profiles ─┐
    │  Engine        │  - Interests      │
    │     │          │  - Preferences    │
    │     │          └────────────────────┘
    │     │
    │     ▼
    │  4.0 ┌──────────────────────┐
    │  User Interaction│ D4: Interaction Log
    │  Tracking   │  - Clicks, Registrations
    │     │      └──────────────────────┘
    └─────┘
         │
         ▼
   Personalized Event Feed

    Event Organizer
         │
         │    5.0
         └──► Event Management
              ├─ Create Event
              ├─ Update Event
              └─ View Analytics
```

#### Level 2: DFD - Recommendation Engine (Detailed)

```
Student Profile    Event Database
     │                   │
     └─────────┬─────────┘
               │
        ┌──────▼──────┐
        │ Extract Text │
        │ (NLTK Token)│
        │ Student      │
        │ Interests    │
        └──────┬──────┘
               │
        ┌──────▼─────────┐
        │ Extract Keywords│
        │ from Events    │
        │ (NLTK keyword  │
        │  extraction)   │
        └──────┬─────────┘
               │
        ┌──────▼──────────┐
        │ Calculate       │
        │ Similarity      │
        │ Score (TF-IDF   │
        │ or keyword      │
        │ overlap %)      │
        └──────┬──────────┘
               │
        ┌──────▼──────────┐
        │ Rank Events     │
        │ by Score        │
        └──────┬──────────┘
               │
        ┌──────▼──────────┐
        │ Apply Filters   │
        │ (Category,      │
        │  Date Range,    │
        │  Availability)  │
        └──────┬──────────┘
               │
        ┌──────▼──────────┐
        │ Store Result    │
        │ in Cache (D5:   │
        │ Recommendations)
        └──────┬──────────┘
               │
               ▼
        Top 10 Recommendations
        (Personalized Feed)
```

**Data Stores:**
- **D1:** User Database (credentials, profiles)
- **D2:** Event Database (all event information)
- **D3:** User Profiles (interests, preferences)
- **D4:** Interaction Log (clicks, registrations, rating)
- **D5:** Recommendation Cache (pre-computed recommendations)

---

### 2.2 Use Case Diagram

```
                          ┌─────────────────┐
                          │  CERS System    │
                          └────────┬────────┘
                                   │
            ┌──────────────────────┼──────────────────────┐
            │                      │                      │
        ┌─────────┐            ┌────────┐            ┌──────────┐
        │ Student │            │Organizer│           │   Admin  │
        └────┬────┘            └────┬────┘           └────┬─────┘
             │                      │                     │
             │   Register/          │                     │
             │   Login         ┌────┴─────┐               │
             ├──►────────────┬─┤   Auth   │               │
             │               │ └────┬─────┘              │
             │               │      │                     │
        ┌────┴───────┐      │  Create Event              │
        │ Browse      │      └─────►├────────────┐        │
        │ Events      │            │   Manage    │        │
        └────┬────────┘            │   Events    │        │
             │                     └────────────┤        │
             │  ┌──────────────────────────────┘        │
             │  │                                        │
        ┌────┴──▼──────────────────────────┐           │
        │  View Event Details   Register     │           │
        │                      for Event    │           │
        └────┬──────────────────────────────┘           │
             │                                           │
             │         ┌─────────────────────────────────┤
             │         │                                 │
        ┌────┴─────┐   │  View My Events                 │
        │ Get       │   │                                 │
        │ Personalized│ │  ┌──────────────────────────────┤
        │ Recommendations
        └──────────┘    │   │ View Analytics
                        │   │ Dashboard
                        │   └──────────────────────────────┤
                        │                                  │
                        └──────────────────────────────────┤
                                                           │
                                                      ┌────▼──┐
                                                      │ Update │
                                                      │ Config │
                                                      └────────┘
```

**Primary Use Cases:**

| Actor | Use Case | Description |
|-------|----------|-------------|
| Student | UC1: Register/Login | Create account & authenticate |
| Student | UC2: Browse Events | Search/filter/view all events |
| Student | UC3: View Recommendations | See personalized event suggestions |
| Student | UC4: Register for Event | RSVP to selected event |
| Organizer | UC5: Create Event | Add new event to system |
| Organizer | UC6: Manage Events | Edit/delete/publish events |
| Admin | UC7: Dashboard | View system analytics & metrics |
| System | UC8: Generate Recommendations | NLTK-based event suggestion |

---

### 2.3 Entity-Relationship Diagram (ERD)

```
┌─────────────────────┐         ┌──────────────────────┐
│      USER           │         │       EVENT          │
├─────────────────────┤         ├──────────────────────┤
│ PK  user_id         │         │ PK  event_id         │
│     email           │         │     title            │
│     password_hash   │         │     description      │
│     name            │         │     category_id FK   │
│     role            │         │     organizer_id FK  │
│     created_at      │         │     date             │
│     updated_at      │         │     time             │
│     is_active       │         │     location         │
└──┬──────────────────┘         │     max_capacity     │
   │ 1                          │     created_at       │
   │                            └──┬──────────────────┘
   │                               │ 1
   │ N                             │
   │ ┌────────────┐               │ N
   └─┤ INTEREST   ├───────────────┘
   │ ├────────────┤        ┌──────────────────────┐
   │ │PK interest_│        │    REGISTRATION      │
   │ │   _id      │        ├──────────────────────┤
   │ │   name     │        │ PK registration_id   │
   │ │   keyword_s│   ┌───►│    user_id FK        │
   │ │   (NLTK)   │   │    │    event_id FK       │
   │ │   keywords │   │    │    registered_at     │
   │ └────────────┘   │    │    status            │
   │                  │    └──────────────────────┘
   │  ┌──────────────────┐
   │  │ USER_INTEREST    │
   │  ├──────────────────┤
   │  │ PK user_interest │
   │  │    _id           │
   │  │    user_id FK◄───┘
   │  │    interest_id FK
   │  │    weight (priority)
   │  └──────────────────┘
   │
   └───────┬──────────────────────┐
           │                      │
      ┌────▼─────────┐      ┌─────▼──────────┐
      │   CATEGORY   │      │ RECOMMENDATION │
      ├──────────────┤      ├────────────────┤
      │ category_id  │      │ PK recom_id    │
      │ name         │      │    user_id FK  │
      │ description  │      │    event_id FK │
      └──────────────┘      │    score       │
                            │    reason      │
                            │    generated_at
                            └────────────────┘
           ┌──────────────────────────────────────┐
           │   INTERACTION_LOG                    │
           ├──────────────────────────────────────┤
           │ interaction_id (PK)                  │
           │ user_id (FK)                         │
           │ event_id (FK)                        │
           │ action_type (view/click/register)    │
           │ timestamp                            │
           │ metadata (device, duration)          │
           └──────────────────────────────────────┘
```

**Key Relationships:**
- User (1:M) → Interest (many-to-many through USER_INTEREST)
- Event (1:M) → Registration (Student RSVP)
- Event (M:1) ← Category (Event categorization)
- User (1:M) → Recommendation (Personalized suggestions)
- User/Event (M:N) → Interaction_Log (Tracking)

**Data Dictionary (Sample):**

| Attribute | Type | Constraints | Purpose |
|-----------|------|-------------|---------|
| user_id | INT | PK, AUTO_INCREMENT | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Authentication & contact |
| role | ENUM | 'student', 'organizer', 'admin' | Access control |
| event_id | INT | PK, AUTO_INCREMENT | Unique event identifier |
| category_id | INT | FK, NOT NULL | Event categorization |
| date | DATE | NOT NULL, >= TODAY | Event scheduling |
| keywords | TEXT | Computed by NLTK | Event description tokens |
| score | FLOAT | 0-100 | Recommendation relevance % |
| action_type | VARCHAR | click/view/register | User interaction tracking |

---

### 2.4 Sequence Diagram: Recommendation Generation

```
Student        Frontend        Backend          NLTK Engine      Database
  │                │               │                │                │
  │                │               │                │                │
  │ Visit Dashboard│               │                │                │
  ├───────────────►│               │                │                │
  │                │ GET /dashboard│                │                │
  │                ├──────────────►│                │                │
  │                │               │ Query User     │                │
  │                │               │ Interests      │                │
  │                │               ├───────────────────────────────►│
  │                │               │◄───────────────────────────────┤
  │                │               │ User Profile Data              │
  │                │               │                │                │
  │                │               │ Get All Events │                │
  │                │               ├───────────────────────────────►│
  │                │               │◄───────────────────────────────┤
  │                │               │ Event List                     │
  │                │               │                │                │
  │                │               │ For each event:                │
  │                │               ├─────────────────┐              │
  │                │               │ Extract Keywords│              │
  │                │               │ (NLTK)          │              │
  │                │               ├───────────────►│              │
  │                │               │◄───────────────┤              │
  │                │               │ Keywords: [...]│              │
  │                │               │                │              │
  │                │               │ Calculate      │              │
  │                │               │ Similarity Score               │
  │                │               │(keyword match%)               │
  │                │               ├───────────────►│              │
  │                │               │◄───────────────┤              │
  │                │               │ Score: 78%     │              │
  │                │               │                │              │
  │                │               │ Repeat for all │              │
  │                │               │ events...      │              │
  │                │               │                │              │
  │                │               │ Sort & Rank    │              │
  │                │               │ Top 10 events  │              │
  │                │               │                │              │
  │                │               │ Cache Result   │              │
  │                │               ├───────────────────────────────►│
  │                │               │◄───────────────────────────────┤
  │                │               │                │                │
  │                │ Return JSON    │                │                │
  │                │ [Recommendations]               │                │
  │                │◄──────────────┤                │                │
  │                │               │                │                │
  │ Render Feed    │               │                │                │
  │◄───────────────┤               │                │                │
  │                │               │                │                │
```

---

## 3. PROTOTYPING & UI/UX OVERVIEW

### 3.1 User Interface Wireframes (ASCII Representation)

#### Screen 1: Student Dashboard (Post-Login)
```
┌──────────────────────────────────────────────────────┐
│  CERS - College Event Recommendation System  [👤 Menu]│
├──────────────────────────────────────────────────────┤
│  Welcome, Rahul!                                     │
│  ┌────────────────┐ ┌────────────────┐             │
│  │📊 My Stats     │ │⚙️  My Interests│             │
│  │ 12 Registered  │ │ Tech, Sports   │             │
│  │ Events         │ │ Cultural       │             │
│  └────────────────┘ └────────────────┘             │
├──────────────────────────────────────────────────────┤
│  🎯 PERSONALIZED FOR YOU                             │
│  ┌─────────────────────────────────────────────────┐ │
│  │ 1. 🖥️  AI/ML Workshop                    Score: 92│ │
│  │    Sat, Feb 1 | 2:00 PM | Room 201      [Register]│ │
│  ├─────────────────────────────────────────────────┤ │
│  │ 2. 🏃 Inter-College Sports Meet        Score: 87│ │
│  │    Sun, Feb 2 | 8:00 AM | Field         [Register]│ │
│  ├─────────────────────────────────────────────────┤ │
│  │ 3. 🎨 Art Exhibition                   Score: 75│ │
│  │    Fri, Feb 7 | 4:00 PM | Gallery       [Register]│ │
│  └─────────────────────────────────────────────────┘ │
├──────────────────────────────────────────────────────┤
│  [🔍 Search Events]  [📂 Browse by Category]        │
├──────────────────────────────────────────────────────┤
│ © CERS 2026 - Campus Connection Hub                │
└──────────────────────────────────────────────────────┘
```

#### Screen 2: Event Browsing Page
```
┌──────────────────────────────────────────────────────┐
│  CERS - All Events                        [👤 Menu] │
├──────────────────────────────────────────────────────┤
│  Filter: [Category ▼] [Date ▼] [Popularity ▼]      │
│  Search: [__________________] [🔍 Search]          │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────────┐  ┌──────────────────┐         │
│  │🖥️ AI Workshop    │  │🏃 Sports Meet    │         │
│  │Feb 1, 2:00 PM   │  │Feb 2, 8:00 AM   │         │
│  │Room 201          │  │Field            │         │
│  │ 24 Going         │  │ 156 Going       │         │
│  │[View More]       │  │[View More]      │         │
│  └──────────────────┘  └──────────────────┘         │
│                                                      │
│  ┌──────────────────┐  ┌──────────────────┐         │
│  │🎨 Art Exhibition │  │🎭 Theatre Show   │         │
│  │Feb 7, 4:00 PM   │  │Feb 8, 6:30 PM   │         │
│  │Gallery           │  │Auditorium        │         │
│  │ 12 Going         │  │ 87 Going         │         │
│  │[View More]       │  │[View More]       │         │
│  └──────────────────┘  └──────────────────┘         │
│                                                      │
│  [< Prev]  [1] [2] [3] [4] [Next >]                │
└──────────────────────────────────────────────────────┘
```

#### Screen 3: Event Detail Page
```
┌──────────────────────────────────────────────────────┐
│  🖥️  Artificial Intelligence & ML Workshop          │
├──────────────────────────────────────────────────────┤
│  📅 Saturday, February 1, 2026                       │
│  ⏰ 2:00 PM - 5:00 PM                                │
│  📍 Room 201, Engineering Block                      │
│  👥 24/50 Registered  ★★★★★ 4.8 (12 reviews)       │
├──────────────────────────────────────────────────────┤
│  📝 DESCRIPTION                                      │
│  Learn cutting-edge AI techniques, neural networks,  │
│  and practical ML implementation from industry       │
│  experts. Perfect for beginners to intermediate     │
│  developers interested in data science.             │
├──────────────────────────────────────────────────────┤
│  🏷️  CATEGORY: Technical | DIFFICULTY: Intermediate │
│  📌 ORGANIZED BY: Computer Science Club             │
│  🔗 Website: https://csclub.example.com             │
├──────────────────────────────────────────────────────┤
│  ✅ [Register Now]  ☆ [Save to My Events]           │
│  ⚠️  Free entry | No materials fee                  │
├──────────────────────────────────────────────────────┤
│  💬 REVIEWS                                          │
│  "Great workshop, learned a lot!" - Priya S.        │
│  "Excellent speakers" - Arjun M.                    │
│  [View All Reviews]                                 │
└──────────────────────────────────────────────────────┘
```

#### Screen 4: Admin Analytics Dashboard
```
┌──────────────────────────────────────────────────────┐
│  📊 Admin Dashboard                   [👤 Logout]   │
├──────────────────────────────────────────────────────┤
│  ┌─────────────────┐ ┌─────────────────┐            │
│  │ Total Events    │ │ Total Users     │            │
│  │      127        │ │     3,245       │            │
│  └─────────────────┘ └─────────────────┘            │
│  ┌─────────────────┐ ┌─────────────────┐            │
│  │ Total Registrations  │ Recommendation │          │
│  │      8,932      │ │ Accuracy       │            │
│  │                 │ │      78%        │            │
│  └─────────────────┘ └─────────────────┘            │
├──────────────────────────────────────────────────────┤
│  📈 Top 5 Categories                                 │
│  ■■■■■ Tech Events      (32 events)                │
│  ■■■■  Sports           (28 events)                │
│  ■■■   Cultural         (24 events)                │
│  ■■    Academic         (16 events)                │
│  ■     Social           (12 events)                │
├──────────────────────────────────────────────────────┤
│  📅 Events This Month: 23 | Next Month: 18         │
│  💾 [Export Report]  🔄 [Refresh]  ⚙️ [Settings]    │
└──────────────────────────────────────────────────────┘
```

### 3.2 Key UI/UX Principles

1. **Clean, Minimal Design:** Reduce cognitive load for quick event discovery
2. **Mobile-First:** 70% of users will access via mobile devices
3. **Personalization Visible:** Show recommendation scores/reasoning
4. **One-Click Registration:** Minimize friction to event signup
5. **Consistent Navigation:** Header menu on all pages
6. **Color Psychology:** Use category colors (Tech=Blue, Sports=Green, etc.)
7. **Accessibility:** WCAG 2.1 AA compliance (contrast, keyboard navigation)
8. **Responsive Grid:** Auto-adjust to screen sizes

### 3.3 Technology Choices - Justification

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Backend Framework** | Flask | Lightweight, perfect for learning, excellent documentation |
| **Database** | SQLite | Single-file setup, zero administration, sufficient for MVP scale |
| **Frontend** | Vanilla JS | No build process, easy debugging, great for learning |
| **Styling** | CSS Grid/Flexbox | Modern layout, no external dependencies |
| **NLP Library** | NLTK | Industry-standard, perfect for keyword extraction task |
| **Authentication** | Flask-Login + Bcrypt | Secure, simple implementation |
| **API Style** | REST | Standard, easy to test, frontend-agnostic |

---

## 4. SOFTWARE REQUIREMENTS SPECIFICATION (SRS)
### Early-Phase Document (IEEE-Inspired Format)

### 4.1 Introduction

#### 4.1.1 Purpose
This SRS document specifies the requirements for the College Event Recommendation System (CERS). It serves as a blueprint for developers, enables requirements traceability, and facilitates project scope management across a 4-member development team.

#### 4.1.2 Document Scope
- **System Scope:** Web-based event management and personalization platform
- **Project Scope:** 12-16 week semester project, university CSE coursework
- **Out of Scope:** Mobile native apps, payment processing, multi-language support (Phase 2)

#### 4.1.3 Definitions & Acronyms

| Term | Definition |
|------|-----------|
| **CERS** | College Event Recommendation System |
| **User** | Generic term for Student, Organizer, or Admin |
| **NLTK** | Natural Language Toolkit - Python library for NLP |
| **RSVP** | Respond (accepts/declines event invitation) |
| **TF-IDF** | Term Frequency-Inverse Document Frequency (ranking algorithm) |
| **MVP** | Minimum Viable Product (core features only) |
| **Session** | User login state maintained via server/browser |

### 4.2 Overall Description

#### 4.2.1 Product Perspective
CERS is a standalone web application for managing and discovering college events. It operates in the campus network environment and interacts with the college's existing user database (future phase: LDAP integration).

**System Context:**
```
┌──────────────────────────────────────┐
│  Web Browser (Chrome, Firefox, Edge)  │
└────────────────┬─────────────────────┘
                 │ HTTP/HTTPS
        ┌────────▼──────────┐
        │  CERS Web Server   │
        │  (Flask + Python)  │
        ├───────────────────┤
        │ - Event Manager    │
        │ - Recommendation   │
        │ - Auth System      │
        │ - Analytics        │
        └────────┬──────────┘
                 │
        ┌────────▼──────────────┐
        │  SQLite Database       │
        │  - Events              │
        │  - Users               │
        │  - Registrations       │
        │  - Recommendations     │
        └───────────────────────┘
```

#### 4.2.2 Product Features

**Feature List (Hierarchical):**

1. **Event Management**
   - Create, read, update, delete events
   - Categorize events
   - Set capacity & availability

2. **Event Discovery**
   - Browse all upcoming events
   - Search by keyword/title
   - Filter by category, date, organizer
   - Sort by popularity, date, relevance

3. **Recommendation Engine**
   - Analyze student profile interests
   - Extract event keywords (NLTK)
   - Calculate similarity scores
   - Generate personalized recommendations
   - Rank and display top-10 suggestions

4. **User Management**
   - Registration (email verification)
   - Authentication (login/logout)
   - Profile management (interest selection)
   - Role-based access (Student/Organizer/Admin)

5. **Registration & RSVP**
   - Register for events
   - Cancel registrations
   - View registered events
   - Track registration counts

6. **Analytics & Reporting**
   - Event performance metrics
   - Recommendation effectiveness
   - User engagement trends
   - Export capabilities

### 4.3 Functional Requirements

Organized by priority and actor:

#### **FR-1 User Authentication & Registration**

| ID | Requirement | Priority | Actor | Acceptance Criteria |
|-----|------------|----------|-------|-------------------|
| FR-1.1 | Student Registration | HIGH | Student | User can create account with email, password, name; confirm email; login success |
| FR-1.2 | Organizer Registration | HIGH | Organizer | Registration requires college email; email verification sends; organizer role confirmed |
| FR-1.3 | Login Functionality | HIGH | All | User enters email/password; session created; redirect to dashboard |
| FR-1.4 | Logout Functionality | HIGH | All | Session terminated; redirect to homepage; all cookies cleared |
| FR-1.5 | Password Recovery | MEDIUM | All | Email sent with reset link; link valid for 24 hours; new password set successfully |
| FR-1.6 | Interest Profile Setup | HIGH | Student | Student selects 3-5 interests from predefined list; interests saved to profile |

#### **FR-2 Event Management**

| ID | Requirement | Priority | Actor | Acceptance Criteria |
|-----|------------|----------|-------|-------------------|
| FR-2.1 | Create Event | CRITICAL | Organizer | Organizer fills form (title, desc, date, time, location, category); event saved in database |
| FR-2.2 | Edit Event | HIGH | Organizer | Organizer modifies event details; changes reflected immediately |
| FR-2.3 | Delete/Archive Event | HIGH | Organizer | Event marked as inactive; no longer appears in student views; kept in database for history |
| FR-2.4 | View Event Details | CRITICAL | Student | Clicking event shows title, description, date, time, location, organizer, capacity, reviews |
| FR-2.5 | Event Categorization | HIGH | Organizer | Organizer assigns category (Tech, Sports, Cultural, Academic, Social); categories searchable |
| FR-2.6 | Event Capacity Management | HIGH | Organizer | Set max capacity; system prevents registration beyond limit; waitlist option |

#### **FR-3 Event Discovery**

| ID | Requirement | Priority | Actor | Acceptance Criteria |
|-----|------------|----------|-------|-------------------|
| FR-3.1 | Browse All Events | CRITICAL | Student | Grid/list view of all upcoming events; loads within 2 seconds; pagination if >20 events |
| FR-3.2 | Search Events | CRITICAL | Student | Keyword search in title/description; results returned within 1 second |
| FR-3.3 | Filter by Category | HIGH | Student | Multi-select category filter; results update dynamically |
| FR-3.4 | Filter by Date Range | HIGH | Student | Date picker for start/end; shows events within range |
| FR-3.5 | Sort Events | MEDIUM | Student | Options: By date (ascending/descending), Popularity (attendees), Alphabetical |
| FR-3.6 | Event Recommendations | CRITICAL | Student | Dashboard shows top 10 personalized recommendations; includes relevance score |

#### **FR-4 Recommendation Engine**

| ID | Requirement | Priority | Technical Details |
|-----|------------|----------|------------------|
| FR-4.1 | Extract User Interests | HIGH | Read user_interest table; join with keywords |
| FR-4.2 | Tokenize Event Descriptions | HIGH | Use NLTK word_tokenize() on event descriptions; remove stopwords |
| FR-4.3 | Keyword Extraction | HIGH | Extract 10-15 keywords per event using NLTK or TF-IDF; store in event_keywords table |
| FR-4.4 | Calculate Similarity | HIGH | For each event, calculate keyword overlap with user interests; score = (matches/total_keywords)*100 |
| FR-4.5 | Filter & Rank | HIGH | Apply category/date filters; sort by score descending; return top 10 |
| FR-4.6 | Cache Recommendations | MEDIUM | Pre-compute recommendations hourly; store in recommendation_cache table; update on user interest change |
| FR-4.7 | Handle Cold-Start Problem | MEDIUM | New users show trending events + random category-based events until they set interests |

#### **FR-5 Registration & RSVP**

| ID | Requirement | Priority | Actor | Acceptance Criteria |
|-----|------------|----------|-------|-------------------|
| FR-5.1 | RSVP to Event | HIGH | Student | Click "Register"; entry added to registration table; user added to attendee count |
| FR-5.2 | Cancel Registration | HIGH | Student | Click "Cancel Registration"; entry removed; user removed from attendee count |
| FR-5.3 | View My Events | HIGH | Student | Shows list of events user registered for; sorted by date |
| FR-5.4 | View Registration Count | MEDIUM | Organizer | Event details page shows "12/50 registered"; updated in real-time |
| FR-5.5 | Duplicate Registration Prevention | HIGH | System | System prevents same user registering twice for same event; shows "Already registered" message |

#### **FR-6 Analytics & Admin Features**

| ID | Requirement | Priority | Actor | Acceptance Criteria |
|-----|------------|----------|-------|-------------------|
| FR-6.1 | Event Dashboard | HIGH | Admin | Shows total events, registrations, popular categories; KPIs visible |
| FR-6.2 | Recommendation Metrics | MEDIUM | Admin | Track recommendation accuracy: (registrations_from_recommendations / total_registrations) * 100 |
| FR-6.3 | User Engagement Trends | MEDIUM | Admin | Show users by category interest; participation rate by month |
| FR-6.4 | Export Reports | MEDIUM | Admin | Export to CSV: events, registrations, user list; includes timestamp |
| FR-6.5 | System Configuration | MEDIUM | Admin | Manage categories, keywords, system settings via admin panel |

### 4.4 Non-Functional Requirements

#### **NFR-1: Performance**

| ID | Requirement | Target | Measurement |
|-----|------------|--------|-------------|
| NFR-1.1 | Page Load Time | < 2 seconds | Load time for event grid/recommendations dashboard |
| NFR-1.2 | Search Response | < 1 second | Keyword search returns results |
| NFR-1.3 | Recommendation Generation | < 1 second | Personalized feed loads |
| NFR-1.4 | Database Query | < 500ms | Average query execution time |
| NFR-1.5 | Concurrent Users | Support 500 simultaneous | Load test baseline |

#### **NFR-2: Scalability**

| ID | Requirement | Target | Notes |
|-----|------------|--------|-------|
| NFR-2.1 | Event Capacity | 5000+ events | Database indexed on category, date |
| NFR-2.2 | User Capacity | 10,000+ users | SQLite performance tested; migration to PostgreSQL in Phase 2 |
| NFR-2.3 | Registration Volume | 50,000+ records | Database normalized; archival strategy for old registrations |

#### **NFR-3: Usability**

| ID | Requirement | Target | Validation |
|-----|------------|--------|-----------|
| NFR-3.1 | Mobile Responsive | Displays on 320px-1920px | CSS media queries; tested on mobile devices |
| NFR-3.2 | Accessibility | WCAG 2.1 AA | Keyboard navigation, color contrast, screen reader support |
| NFR-3.3 | Intuitive Navigation | User completes task in < 5 clicks | Usability testing with student sample |

#### **NFR-4: Security**

| ID | Requirement | Implementation |
|-----|------------|-----------------|
| NFR-4.1 | Password Hashing | Bcrypt with salt rounds = 12 |
| NFR-4.2 | SQL Injection Prevention | SQLAlchemy ORM (parameterized queries) |
| NFR-4.3 | Session Management | Flask-Login with secure cookies; timeout after 30 minutes |
| NFR-4.4 | CSRF Protection | Flask-WTF CSRF tokens on all forms |
| NFR-4.5 | Data Encryption | HTTPS for all communication; TLS 1.2+ |

#### **NFR-5: Maintainability**

| ID | Requirement | Target |
|-----|------------|--------|
| NFR-5.1 | Code Documentation | 100% of functions documented; docstrings for all modules |
| NFR-5.2 | Modular Architecture | Separation: models, views, controllers; reusable components |
| NFR-5.3 | Testing Coverage | Unit tests for all business logic; integration tests for API |
| NFR-5.4 | Version Control | Git with semantic versioning (v1.0.0, v1.1.0) |

### 4.5 Constraints & Dependencies

**Technical Constraints:**
- Must use Flask, SQLite, NLTK, Vanilla JS (non-negotiable per project requirements)
- No advanced ML models (transformers, deep learning) in MVP
- Single server deployment (no microservices)
- No real-time updates (batch processing acceptable)

**Resource Constraints:**
- 4-person team, 12-16 weeks
- Limited testing infrastructure (manual QA + basic automation)
- College server/hosting provided (specifics TBD)

**External Dependencies:**
- NLTK library version 3.8+
- Flask 2.3.0+
- Python 3.9+
- Modern browser with ES6 support

### 4.6 Requirements Traceability Matrix (RTM)

| Business Objective | Functional Requirement | NFR | Test Case |
|-------|-----|-----|-----|
| Centralize event info | FR-2.1, FR-3.1 | NFR-1.1 | TC-001: Create & display event |
| Personalize recommendations | FR-4.1 - FR-4.7 | NFR-1.2 | TC-025: Recommendation accuracy |
| Increase participation | FR-5.1 | NFR-3.2 | TC-050: One-click registration |
| Scale for future | FR-4.6 | NFR-2.1, NFR-2.2 | TC-075: Load test 5000 events |

---

## 5. WORK BREAKDOWN STRUCTURE & TASK DECOMPOSITION

### 5.1 Project Phases Overview

```
Phase 1: Requirements & Design (Weeks 1-2)
    ├─ Requirements Elicitation & Refinement
    ├─ System Design (DFD, Use Cases, ERD)
    ├─ Prototyping & Wireframes
    └─ SRS Documentation [← YOU ARE HERE]

Phase 2: Backend Development (Weeks 3-7)
    ├─ Database Schema & Setup
    ├─ User Management Module
    ├─ Event Management Module
    ├─ Recommendation Engine
    └─ API Endpoints Development

Phase 3: Frontend Development (Weeks 6-10)
    ├─ UI Component Development
    ├─ Frontend Integration with API
    ├─ Mobile Responsiveness
    └─ Dashboard & Admin Panel

Phase 4: Integration & Testing (Weeks 9-12)
    ├─ End-to-End Testing
    ├─ Performance Testing
    ├─ Security Testing
    ├─ Bug Fixes
    └─ Load Testing

Phase 5: Documentation & Deployment (Weeks 13-16)
    ├─ User Documentation
    ├─ Developer Documentation
    ├─ Deployment Setup
    └─ Final Presentation
```

### 5.2 Detailed Task Decomposition (Level-Wise)

#### **LEVEL 1: Work Packages (High-Level)**

| WP-ID | Work Package | Duration | Dependencies | Deliverable |
|-------|---------|----------|-------------|-------------|
| WP-1 | Requirements & Design | 2 weeks | None | SRS + Diagrams |
| WP-2 | Backend Core | 5 weeks | WP-1 | API endpoints, database |
| WP-3 | Frontend Development | 5 weeks | WP-2 (partially) | Web UI, responsive design |
| WP-4 | NLP Recommendation Engine | 3 weeks | WP-2 | Keyword extraction + matching |
| WP-5 | Testing & QA | 3 weeks | WP-2, WP-3, WP-4 | Test reports, bug fixes |
| WP-6 | Documentation & Deployment | 2 weeks | All previous | User guide, deployment guide |

---

#### **LEVEL 2: Task Breakdown by Role**

### **TRACK A: DATABASE & ORM LAYER** (Team Lead + 1 Dev)
**Duration:** Weeks 2-4

```
Task A1: Database Schema Design (Week 2)
├─ A1.1: Finalize ERD & normalize schema
├─ A1.2: Define all tables & relationships
├─ A1.3: Set up SQLite connection in Flask
└─ Deliverable: database.db with 8 tables

Task A2: ORM Model Implementation (Weeks 2-3)
├─ A2.1: Create User model (Flask-SQLAlchemy)
├─ A2.2: Create Event model
├─ A2.3: Create Registration & Interest models
├─ A2.4: Create Recommendation model
└─ Deliverable: models.py with all SQLAlchemy classes

Task A3: Database Migrations & Fixtures (Week 3)
├─ A3.1: Set up Flask-Migrate
├─ A3.2: Create sample data (seed.py)
├─ A3.3: Test schema validation
└─ Deliverable: Migration scripts, test data
```

**Skills Required:** Database design, SQLAlchemy, Flask basics

---

### **TRACK B: BACKEND API & AUTH** (Senior Dev + 1 Mid-Dev)
**Duration:** Weeks 3-7

```
Task B1: Authentication System (Weeks 3-4)
├─ B1.1: Implement user registration endpoint (POST /auth/register)
│   ├─ Email validation & uniqueness check
│   ├─ Password hashing (bcrypt)
│   └─ Response: {user_id, email, created_at}
│
├─ B1.2: Implement login endpoint (POST /auth/login)
│   ├─ Credential verification
│   ├─ Session/JWT token creation
│   └─ Response: {token, user_id, role}
│
├─ B1.3: Implement logout endpoint (POST /auth/logout)
│   └─ Session termination
│
├─ B1.4: Authentication middleware
│   ├─ @login_required decorator
│   └─ Role-based access control
│
└─ Deliverable: auth.py module with 4 endpoints

Task B2: Event Management API (Weeks 4-5)
├─ B2.1: GET /events - List all events
│   ├─ Pagination (limit, offset)
│   ├─ Filter by category, date
│   └─ Response: [{event_id, title, date, category, ...}]
│
├─ B2.2: GET /events/{event_id} - Event details
│   └─ Response: Full event object with attendee count
│
├─ B2.3: POST /events - Create event (Organizer only)
│   ├─ Input validation
│   ├─ Keyword extraction (NLTK)
│   └─ Response: {event_id, status: 'created'}
│
├─ B2.4: PUT /events/{event_id} - Update event
│   └─ Only organizer who created it
│
├─ B2.5: DELETE /events/{event_id} - Archive event
│   └─ Soft delete (mark as inactive)
│
└─ Deliverable: events.py module with 5 endpoints

Task B3: User Management API (Weeks 4-5)
├─ B3.1: GET /users/profile - Current user profile
├─ B3.2: PUT /users/profile - Update interests/details
├─ B3.3: GET /users/{user_id}/events - User's registered events
└─ Deliverable: users.py module

Task B4: Registration API (Week 5)
├─ B4.1: POST /events/{event_id}/register - RSVP
├─ B4.2: DELETE /events/{event_id}/register - Cancel RSVP
├─ B4.3: GET /events/{event_id}/attendees - Attendee list (admin only)
└─ Deliverable: registrations.py module

Task B5: Error Handling & Validation (Week 6)
├─ B5.1: Custom exception classes
├─ B5.2: Request validation schemas
├─ B5.3: Response error formatting
└─ Deliverable: errors.py & validators.py modules
```

**Skills Required:** Flask, REST API design, SQLAlchemy, authentication, input validation

---

### **TRACK C: NLP & RECOMMENDATION ENGINE** (Mid-Dev + 1 Junior Dev)
**Duration:** Weeks 4-7

```
Task C1: NLTK Setup & Keyword Extraction (Weeks 4-5)
├─ C1.1: Install NLTK & download required corpora
│   ├─ punkt tokenizer
│   ├─ stopwords
│   └─ (Optional: word2vec)
│
├─ C1.2: Implement keyword extraction function
│   ├─ Tokenize event description
│   ├─ Remove stopwords & punctuation
│   ├─ Extract top 15 keywords by frequency
│   └─ Function: extract_keywords(text) -> list
│
├─ C1.3: Implement student interest tokenization
│   └─ Function: tokenize_interests(interests_list) -> list
│
└─ Deliverable: nlp_utils.py module

Task C2: Similarity Scoring Algorithm (Weeks 5-6)
├─ C2.1: Implement simple keyword overlap scorer
│   ├─ Score = (matching_keywords / total_event_keywords) * 100
│   ├─ Minimum threshold for relevance (40%)
│   └─ Function: calculate_similarity(user_interests, event_keywords) -> float
│
├─ C2.2: Consider improvements
│   ├─ TF-IDF scoring (optional)
│   ├─ Weight by category match
│   └─ Date proximity bonus (events happening soon)
│
└─ Deliverable: recommendation_engine.py module

Task C3: Recommendation Generation Pipeline (Weeks 6-7)
├─ C3.1: Batch process function
│   ├─ For each user:
│   │   ├─ Get user interests
│   │   ├─ For each event:
│   │   │   ├─ Extract event keywords
│   │   │   ├─ Calculate similarity
│   │   │   └─ Store score
│   │   └─ Rank top 10
│   └─ Function: generate_recommendations_for_user(user_id) -> list
│
├─ C3.2: Caching strategy
│   ├─ Store results in recommendation table
│   ├─ Invalidate cache on user interest change
│   └─ Refresh cache hourly (batch job)
│
├─ C3.3: Cold-start handling
│   ├─ New users: show trending events + category-based
│   └─ Function: get_bootstrap_recommendations(user_id) -> list
│
└─ Deliverable: recommendation_service.py + tests

Task C4: API Endpoint for Recommendations (Week 7)
├─ C4.1: GET /recommendations - Get personalized recommendations
│   ├─ Query recommendation cache
│   ├─ Fallback to real-time generation if cache miss
│   └─ Response: [{event_id, title, score, reason}, ...]
│
└─ Deliverable: Integrated into events.py API
```

**Skills Required:** NLTK, Python, algorithms, natural language processing fundamentals

**Algorithm Reference:**
```python
def recommend_events(user_id):
    user = User.query.get(user_id)
    user_interests = get_user_keywords(user)
    
    all_events = Event.query.filter_by(is_active=True).all()
    scores = []
    
    for event in all_events:
        event_keywords = extract_keywords(event.description)
        score = calculate_similarity(user_interests, event_keywords)
        
        if score >= MIN_THRESHOLD:
            scores.append((event.id, score, event))
    
    # Sort by score descending, get top 10
    top_recommendations = sorted(scores, key=lambda x: x[1], reverse=True)[:10]
    return top_recommendations
```

---

### **TRACK D: FRONTEND & UI** (2 Junior Devs working in parallel)
**Duration:** Weeks 6-10

```
Task D1: HTML Structure & Base Templates (Weeks 6-7)
├─ D1.1: Base template with header/footer/nav
├─ D1.2: Dashboard template (main landing page)
├─ D1.3: Event browsing template
├─ D1.4: Event detail template
├─ D1.5: Login/signup templates
├─ D1.6: Admin panel templates
└─ Deliverable: 6+ Jinja2 templates

Task D2: CSS Styling & Mobile Responsiveness (Weeks 7-8)
├─ D2.1: Global styles (typography, colors, spacing)
│   ├─ CSS variables for theming
│   ├─ Mobile-first approach
│   └─ Media queries for breakpoints: 320px, 768px, 1024px
│
├─ D2.2: Component styles
│   ├─ Buttons, cards, forms
│   ├─ Navigation bar
│   └─ Event grid/list layout
│
├─ D2.3: Testing on mobile devices
│   └─ Chrome DevTools, real device testing (iPhone, Android)
│
└─ Deliverable: 3-5 CSS files, >500 lines total

Task D3: JavaScript Interactivity (Weeks 8-9)
├─ D3.1: Event filtering & search
│   ├─ Client-side filters (category, date)
│   ├─ Keyword search with live results
│   └─ File: search.js
│
├─ D3.2: Registration functionality
│   ├─ RSVP button interaction
│   ├─ Confirmation dialogs
│   ├─ Loading states
│   └─ File: registration.js
│
├─ D3.3: Dashboard interactivity
│   ├─ Recommendation card carousel
│   ├─ Interest selection UI
│   └─ File: dashboard.js
│
├─ D3.4: Admin panel functionality
│   ├─ Event creation form
│   ├─ Analytics chart rendering
│   └─ File: admin.js
│
└─ Deliverable: 4+ JS modules

Task D4: API Integration (Weeks 9-10)
├─ D4.1: Fetch wrapper for API calls
│   ├─ Error handling
│   ├─ Authentication token management
│   └─ File: api.js
│
├─ D4.2: Fetch integration into each page
│   ├─ GET /events integration
│   ├─ GET /recommendations integration
│   ├─ POST /register integration
│   └─ Update pages with backend data
│
└─ Deliverable: All pages connected to backend
```

**Skills Required:** HTML, CSS, JavaScript (Vanilla), REST API consumption, responsive design

---

### **TRACK E: TESTING & QA** (1 QA Engineer + Developers assist)
**Duration:** Weeks 9-12

```
Task E1: Unit Testing (Weeks 9-10)
├─ E1.1: Test NLTK keyword extraction
│   └─ test_nlp_utils.py (10+ test cases)
│
├─ E1.2: Test recommendation algorithm
│   └─ test_recommendation_engine.py (15+ test cases)
│
├─ E1.3: Test API endpoints
│   └─ test_api.py (20+ test cases for CRUD operations)
│
└─ Deliverable: unittest/pytest suite, >80% coverage

Task E2: Integration Testing (Weeks 10-11)
├─ E2.1: End-to-end user flows
│   ├─ Signup → Login → Browse → Register → View Recommendations
│   └─ test_e2e.py (5+ scenarios)
│
├─ E2.2: Database integrity
│   └─ Foreign key constraints, data consistency
│
└─ Deliverable: E2E test suite

Task E3: Performance Testing (Week 11)
├─ E3.1: Load testing with 100+ concurrent users
├─ E3.2: Database query optimization
├─ E3.3: Profiling & bottleneck identification
└─ Deliverable: Performance report

Task E4: Security Testing (Week 11)
├─ E4.1: SQL injection attempts
├─ E4.2: XSS vulnerability testing
├─ E4.3: CSRF token validation
├─ E4.4: Session hijacking prevention
└─ Deliverable: Security audit report

Task E5: Bug Tracking & Fixes (Weeks 11-12)
├─ E5.1: Log all bugs in GitHub Issues
├─ E5.2: Prioritize & assign
├─ E5.3: Regression testing after fixes
└─ Deliverable: Bug-free build for deployment
```

**Skills Required:** Testing frameworks (pytest, unittest), QA methodology, performance profiling

---

### **TRACK F: DOCUMENTATION & DEPLOYMENT** (Team Lead)
**Duration:** Weeks 12-16

```
Task F1: User Documentation (Weeks 12-13)
├─ F1.1: Student user guide
│   ├─ Screenshots with annotations
│   ├─ Step-by-step tutorials
│   └─ Deliverable: user_guide_student.pdf
│
├─ F1.2: Organizer guide
│   └─ How to create & manage events
│
├─ F1.3: Admin guide
│   └─ Dashboard, settings, analytics
│
└─ Deliverable: 3 user guides (20+ pages total)

Task F2: Developer Documentation (Weeks 13-14)
├─ F2.1: API documentation
│   ├─ Endpoint reference (all 15+ endpoints)
│   ├─ Request/response examples
│   ├─ Error codes & messages
│   └─ Deliverable: API_DOCS.md (50+ pages)
│
├─ F2.2: Architecture documentation
│   ├─ System design overview
│   ├─ Module descriptions
│   ├─ Data flow diagrams
│   └─ Deliverable: ARCHITECTURE.md
│
├─ F2.3: Setup & installation guide
│   ├─ Prerequisites
│   ├─ Virtual environment setup
│   ├─ Dependencies installation
│   ├─ Database initialization
│   ├─ Running the application
│   └─ Deliverable: SETUP.md
│
├─ F2.4: Code documentation
│   ├─ Docstrings for all functions
│   ├─ Module-level comments
│   └─ Code comments for complex logic
│
└─ Deliverable: Complete dev documentation

Task F3: Deployment Setup (Week 14-15)
├─ F3.1: Production environment preparation
│   ├─ Server configuration
│   ├─ Database backup strategy
│   └─ SSL/TLS setup
│
├─ F3.2: Deployment script
│   ├─ Automated database migration
│   ├─ Asset compilation
│   └─ Service restart
│
├─ F3.3: Monitoring & logging
│   ├─ Error logging setup
│   ├─ Performance monitoring
│   └─ Deliverable: deployment_guide.md
│
└─ Deliverable: Production-ready environment

Task F4: Project Presentation (Week 16)
├─ F4.1: Live demo preparation
├─ F4.2: Presentation slides (30 slides)
├─ F4.3: Project report (40+ pages)
└─ Deliverable: Presentation materials + final report
```

**Skills Required:** Technical writing, DevOps basics, presentation skills

---

### 5.3 Resource Allocation Matrix

**Team Size:** 4 members

```
┌─────────────────────────────────────────────────────────┐
│                 CERS PROJECT TEAM (4 Members)           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  👤 MEMBER 1: Backend Lead / Database Architect        │
│     Tracks: A (Database), B (Backend API)              │
│     Weeks 2-10 (Full-time)                             │
│     Skills: Python, Flask, Database design, ORM        │
│     Output: 2 Major modules (models, APIs)             │
│                                                         │
│  👤 MEMBER 2: NLP/Recommendation Engineer              │
│     Tracks: C (NLP & Recommendations), B (assist)      │
│     Weeks 3-8 (Full-time), 9-10 (Part-time support)   │
│     Skills: Python, NLTK, Algorithms, NLP basics       │
│     Output: Recommendation engine + optimization       │
│                                                         │
│  👤 MEMBER 3: Frontend Developer #1                     │
│     Tracks: D (Frontend), E (assist testing)           │
│     Weeks 6-10 (Full-time), 11 (Part-time testing)     │
│     Skills: HTML, CSS, JavaScript, Responsive design  │
│     Output: Dashboard, event pages, styling            │
│                                                         │
│  👤 MEMBER 4: Frontend/QA Developer #2                  │
│     Tracks: D (Frontend), E (QA Lead)                  │
│     Weeks 6-12 (Full-time), 13-16 (Documentation)     │
│     Skills: Frontend, Testing, Documentation           │
│     Output: Admin panel, tests, deployment             │
│                                                         │
│  ⏱️  PROJECT MANAGER (Optional - can be rotated)        │
│     Coordinates: Task allocation, weekly standup       │
│     Weekly meetings every Monday 3:00 PM               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### 5.4 Task Allocation by Seniority Level

#### **LEVEL 1 TASKS: Junior Developers (Learning Focus)**

These tasks are designed to teach fundamentals while contributing value:

**D1: HTML Structure & Templates** (Week 6-7)
- **Why:** Learn templating, HTML semantics
- **Ownership:** Junior Dev (Frontend #1)
- **Complexity:** Low
- **Learning Outcome:** Jinja2 syntax, template inheritance, DRY principle

**D2: CSS Styling** (Weeks 7-8)
- **Why:** Learn responsive design, CSS Grid/Flexbox
- **Ownership:** Junior Dev (Frontend #2)
- **Complexity:** Low-Medium
- **Learning Outcome:** Mobile-first, CSS variables, media queries, accessibility

**E1: Unit Testing** (Weeks 9-10)
- **Why:** Learn testing frameworks, test-driven thinking
- **Ownership:** Junior Dev (QA #2)
- **Complexity:** Low
- **Learning Outcome:** pytest/unittest, assertions, test organization

**C1: Keyword Extraction** (Weeks 4-5)
- **Why:** Learn NLTK, NLP concepts from scratch
- **Ownership:** Junior Dev (NLP) with senior oversight
- **Complexity:** Medium
- **Learning Outcome:** Tokenization, stopwords, text preprocessing

---

#### **LEVEL 2 TASKS: Mid-Level Developers (Skill Building)**

These tasks require some existing knowledge but offer growth:

**B2: Event Management API** (Weeks 4-5)
- **Why:** Learn REST API design, CRUD operations
- **Ownership:** Mid-Dev (Backend)
- **Complexity:** Medium
- **Learning Outcome:** Endpoint design, request validation, response formatting

**D3: JavaScript Interactivity** (Weeks 8-9)
- **Why:** Learn event handling, DOM manipulation
- **Ownership:** Mid-Dev (Frontend #1)
- **Complexity:** Medium
- **Learning Outcome:** Event listeners, async/await, state management

**C2: Similarity Scoring** (Weeks 5-6)
- **Why:** Learn algorithm design, optimization
- **Ownership:** Mid-Dev (NLP)
- **Complexity:** Medium-High
- **Learning Outcome:** Algorithm design, scoring functions, edge cases

---

#### **LEVEL 3 TASKS: Senior Developers (Complex Ownership)**

These tasks require experience and architectural thinking:

**A2: ORM Model Implementation** (Weeks 2-3)
- **Why:** Design database layer; impacts entire project
- **Ownership:** Backend Lead
- **Complexity:** High
- **Learning Outcome:** N/A (teaching moment)

**B1: Authentication System** (Weeks 3-4)
- **Why:** Security-critical; requires best practices
- **Ownership:** Backend Lead
- **Complexity:** High
- **Learning Outcome:** N/A (security architecture)

**E3-E4: Performance & Security Testing** (Week 11)
- **Why:** Requires system thinking, technical depth
- **Ownership:** QA Lead (Backend Lead assist)
- **Complexity:** High
- **Learning Outcome:** N/A (project-level perspective)

**F2: Developer Documentation** (Weeks 13-14)
- **Why:** Requires clear communication of complex systems
- **Ownership:** Backend Lead / Project Manager
- **Complexity:** High
- **Learning Outcome:** N/A (knowledge transfer)

---

### 5.5 Milestone Planning

| Milestone | End Date | Key Deliverables | Success Criteria |
|-----------|----------|------------------|-----------------|
| **M1: Design Freeze** | End Week 2 | SRS + All diagrams | Stakeholder approval |
| **M2: Backend MVP** | End Week 5 | User API + Event API | All CRUD endpoints working |
| **M3: NLP Engine Ready** | End Week 7 | Recommendation endpoint | Top-10 recommendations generated |
| **M4: Frontend UI Complete** | End Week 10 | All pages responsive | Pixel-perfect on 3 breakpoints |
| **M5: Testing Complete** | End Week 11 | Test reports, 0 critical bugs | >80% code coverage |
| **M6: Documentation & Deploy** | End Week 16 | User guides, API docs, live demo | System running in production |

---

### 5.6 Communication & Collaboration Plan

**Weekly Standup:**
- **When:** Every Monday, 3:00 PM (synchronous) + Daily async updates in Slack
- **Duration:** 15 minutes
- **Format:** Each member shares: (1) What I completed, (2) What I'm doing, (3) Blockers
- **Owner:** Project Manager

**Bi-Weekly Code Review:**
- **When:** Wednesdays after standup
- **Format:** Pull request reviews in GitHub
- **Owner:** Backend Lead reviews backend, Frontend Lead reviews frontend

**Documentation Updates:**
- **Timeline:** Update SRS weekly during development
- **Owner:** Team Lead maintains master documentation

**Conflict Resolution:**
- **Low Priority:** Discuss in Slack, @Backend Lead decides
- **Medium Priority:** Schedule 30-min sync call with relevant team members
- **High Priority:** Team meeting with all 4 members + any external stakeholders

---

## 6. RISK ANALYSIS & MITIGATION

### 6.1 Identified Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|-----------|
| Scope creep (feature requests) | HIGH | HIGH | Stick to MVP; document all requests for Phase 2 |
| Team member unavailability | MEDIUM | HIGH | Cross-training on critical modules; documentation |
| NLTK performance issues | LOW | MEDIUM | Early POC in Week 2; fallback to simple keyword matching |
| Database scaling issues | MEDIUM | MEDIUM | Denormalization; caching strategy; indexed queries |
| Frontend-Backend API mismatch | MEDIUM | HIGH | Detailed API contract by Week 3; mock API for parallel dev |
| Insufficient testing coverage | MEDIUM | MEDIUM | QA track runs parallel to dev; continuous integration |

### 6.2 Mitigation Strategies

**Scope Management:**
- Maintain "Won't Do" list visible to all team members
- Any feature requests documented in BACKLOG.md
- Weekly review of scope with stakeholders (professor/client)

**Timeline Buffers:**
- 10% buffer time per track (1 week total across 10-week dev cycle)
- Critical path identified: Backend API → Frontend Integration

**Knowledge Transfer:**
- Each developer documents their module as they build
- Code review comments explain "why", not just "what"
- Pair programming on critical modules (recommendation engine)

---

## 7. APPENDICES

### 7.1 Glossary

| Term | Definition |
|------|-----------|
| **Cold-Start Problem** | Difficulty recommending to new users with no history |
| **Tokenization** | Breaking text into individual words/tokens |
| **Stopwords** | Common words (the, a, and) removed from analysis |
| **TF-IDF** | Scoring algorithm measuring word importance |
| **NLTK** | Natural Language Toolkit - Python NLP library |
| **ORM** | Object-Relational Mapping - maps DB rows to Python objects |
| **RSVP** | Respond with formal acceptance/decline (event registration) |
| **JWT** | JSON Web Token - stateless authentication |
| **CSRF** | Cross-Site Request Forgery - security vulnerability |

### 7.2 References & Resources

**NLTK Documentation:**
- https://www.nltk.org/howto/tokenize.html
- https://www.nltk.org/howto/rst.html

**Flask Best Practices:**
- https://flask.palletsprojects.com/
- https://flask-sqlalchemy.palletsprojects.org/

**Recommendation Systems:**
- Jannach et al., "Recommender Systems: An Introduction" (textbook reference)
- Content-based filtering overview: https://en.wikipedia.org/wiki/Recommender_system

**Project Management:**
- https://agilemanifesto.org/ (Agile principles)
- Scrum guide for sprint planning

### 7.3 Document Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Jan 2026 | Project Team | Initial SRS + all sections |

---

**END OF SDLC DOCUMENTATION**

---

## USAGE GUIDE FOR YOUR TEAM

### How to Use This Document:

1. **For Week 1-2:** Read Sections 1-2 (Requirements & Modeling) as a team. Validate all requirements with your professor/advisor.

2. **For Week 2 onwards:** Use Section 5 (Task Decomposition) to assign tasks. Create GitHub Issues with descriptions matching each task.

3. **For Weekly Standup:** Reference Section 5.6 (Communication Plan) for meeting format.

4. **As Development Progresses:** Update Sections 1-2 if requirements change. Keep RTM current.

5. **For Documentation Phase:** Use Section 7.2 (References) to build your deployment guide.

6. **Portfolio Value:** Sections 1-5 are excellent portfolio materials showing understanding of SDLC methodology.

---

**This document is a living artifact. Update it as your project evolves. It will be your greatest reference during development and your proof of thoughtful engineering to future employers/universities.**

Good luck with your project! 🚀

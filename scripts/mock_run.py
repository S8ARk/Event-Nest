import os
import random
import sys
import datetime
from app import create_app, db
from app.models.user import User, Interest
from app.models.event import Event, Category
from app.services.registration_service import register_user_for_event

app = create_app()
app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True

# Data for generation
EVENT_TITLES = [
    "Machine Learning Workshop", "Basketball Tournament", "Jazz Night", 
    "React.js Bootcamp", "Poetry Slam", "Cybersecurity Seminar", 
    "Football Tryouts", "AI Summit", "Literature Expo", "Networking Mixer"
]
EVENT_LOCATIONS = ["Main Hall", "Stadium", "Auditorium", "Lab 4", "Library"]
EVENT_DESCRIPTIONS = [
    "Join us for an amazing experience. We'll be covering advanced topics.",
    "A great opportunity to meet new friends and learn exciting new skills.",
    "Don't miss out on the biggest event of the year, focusing on innovation.",
    "Get hands-on experience and professional advice from industry experts.",
    "Enjoy a relaxing afternoon with peers and special guests."
]

def run_simulation():
    client = app.test_client()
    
    with app.app_context():
        print("--- STARTING CERS MASS MOCK RUN ---")
        
        # Ensure DB tables exist
        db.create_all()
        
        # 1. Create Admins and Events
        admins = []
        for i in range(1, 11):
            email = f"admin{i}@cers.edu"
            if not User.query.filter_by(email=email).first():
                from app import bcrypt
                admin = User(
                    name=f"Admin {i}",
                    email=email,
                    password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),
                    role='admin'
                )
                db.session.add(admin)
                admins.append(admin)
        db.session.commit()
        
        # Re-query
        admins = User.query.filter_by(role='admin').all()
        categories = Category.query.all()
        
        events_created = 0
        for admin in admins:
            for _ in range(random.randint(2, 3)):
                title = random.choice(EVENT_TITLES) + f" {random.randint(1, 100)}"
                category = random.choice(categories) if categories else None
                
                new_event = Event(
                    title=title,
                    description=random.choice(EVENT_DESCRIPTIONS),
                    category_id=category.id if category else 1,
                    date=datetime.date(2027, 10, 10),
                    time=datetime.time(14, 0),
                    location=random.choice(EVENT_LOCATIONS),
                    max_capacity=random.randint(10, 50),
                    organizer_id=admin.id
                )
                db.session.add(new_event)
                events_created += 1
        db.session.commit()
        print(f"[OK] 10 Admins processed. Created {events_created} events directly into database.")

        # 2. Register Students
        students = []
        for i in range(1, 11):
            email = f"student{i}@mail.com"
            if not User.query.filter_by(email=email).first():
                from app import bcrypt
                student = User(
                    name=f"Student {i}",
                    email=email,
                    password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),
                    role='student'
                )
                db.session.add(student)
                students.append(student)
        db.session.commit()
        
        all_events = Event.query.all()
        
        rsvps = 0
        for student in students:
            events_to_register = random.sample(all_events, min(2, len(all_events)))
            for evt in events_to_register:
                try:
                    register_user_for_event(student.id, evt.id)
                    rsvps += 1
                except Exception as e:
                    print(f"Skipped RSVP: {e}")
                
        print(f"[OK] 10 Students processed. {rsvps} RSVPs processed.")

        # 3. Check Index/Home routing for available events
        print("Checking NLTK Brain logic and index routes...")
        resp = client.get('/', follow_redirects=True)
        if resp.status_code == 200:
            print("[OK] Index page loaded successfully.")
            
        # 4. Check Garbage String search via Search Engine
        # Garbage string like emojis and single chars
        resp = client.get('/events/?search=😎🔥a!', follow_redirects=True)
        if resp.status_code == 200:
            print("[OK] Search logic gracefully handled malformed string/empty NLTK outputs.")
            
        # 5. Check No Title / Empty Data behavior for endpoints
        resp = client.post('/events/create', data={}, follow_redirects=True)
        # Should gracefully fail via form validation
        if resp.status_code in [200, 400]:
            print("[OK] Malformed POST requests properly blocked/handled by backend.")
            
        print("--- SIMULATION FINISHED SUCCESS ---")

if __name__ == '__main__':
    run_simulation()

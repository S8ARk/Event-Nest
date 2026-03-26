from app import create_app, db
from app.models.user import User, Interest
from app.models.event import Category
import os

app = create_app()

def seed_data():
    if not Category.query.first():
        categories = ['Academics', 'Sports', 'Arts & Culture', 'Technology', 'Social']
        for c in categories:
            db.session.add(Category(name=c))
            
    if not Interest.query.first():
        interests = [
            'Computer Science', 'Basketball', 'Music', 'Networking', 'Literature', 
            'Coding', 'Artificial Intelligence', 'Robotics', 'Graphic Design', 
            'Finance', 'Entrepreneurship', 'Photography', 'Volunteering', 
            'Theater Arts', 'Data Science', 'Startups', 'Film Production'
        ]
        for i in interests:
            db.session.add(Interest(name=i))
            
    # Add an admin user for testing
    if not User.query.filter_by(email='admin@cers.edu').first():
        from app import bcrypt
        admin = User(
            name='System Admin', 
            email='admin@cers.edu', 
            password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            role='admin',
            has_completed_onboarding=True
        )
        db.session.add(admin)

    db.session.commit()
    print("Database seeded with Categories, Interests, and an Admin user.")

if __name__ == '__main__':
    with app.app_context():
        # Ensure database and tables are created
        if not os.path.exists(os.path.join(app.instance_path, 'cers.db')):
            db.create_all()
            print("Database tables created successfully.")
        
        seed_data()
            
    app.run(debug=True, use_reloader=False)

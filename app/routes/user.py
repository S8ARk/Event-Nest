from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.utils.decorators import role_required
from app import db
from app.models.user import Interest, UserInterest

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'student':
        from app.services.recommender import generate_recommendations_for_user, get_cached_recommendations
        
        # Proactively re-calculate recommendations to capture newly created events
        # or fresh onboarding interests instantly
        generate_recommendations_for_user(current_user.id)
        
        # Load the freshly computed recommendations
        recommendations = get_cached_recommendations(current_user.id)
        return render_template('dashboard/student.html', recommendations=recommendations)
    elif current_user.role == 'organizer':
        return render_template('dashboard/organizer.html')
    elif current_user.role == 'admin':
        from app.services.analytics import get_system_metrics, get_popular_events
        metrics = get_system_metrics()
        popular_events = get_popular_events()
        return render_template('dashboard/admin.html', metrics=metrics, popular_events=popular_events)
    else:
        return redirect(url_for('main.index'))

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
@role_required('student', 'organizer', 'admin')
def profile():
    if request.method == 'POST':
        # Handling name update
        current_user.name = request.form.get('name')
        
        # If student, handle interests update
        if current_user.role == 'student':
            selected_interests = request.form.getlist('interests')
            
            # Clear old interests
            for ui in current_user.user_interests:
                db.session.delete(ui)
            
            # Add new interests
            for interest_id in selected_interests:
                ui = UserInterest(user_id=current_user.id, interest_id=int(interest_id))
                db.session.add(ui)
                
        db.session.commit()
        
        # Module 5: Re-calculate personalized recommendations on interest change
        from app.services.recommender import generate_recommendations_for_user
        generate_recommendations_for_user(current_user.id)
        
        flash('Profile updated successfully! Recommendations have been refreshed.', 'success')
        return redirect(url_for('user.profile'))
        
    all_interests = Interest.query.all()
    user_interest_ids = [ui.interest_id for ui in current_user.user_interests]
    
    return render_template('user/profile.html', interests=all_interests, user_interest_ids=user_interest_ids)

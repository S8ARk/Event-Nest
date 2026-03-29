from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.models.user import User, Interest, UserInterest
from app.forms.auth import RegistrationForm, LoginForm

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Processes new user registrations, gracefully hashing passwords and verifying uniqueness constraints.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            name=form.name.data,
            email=form.email.data,
            password_hash=hashed_password,
            role=form.role.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! You are now able to log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/login_register.html', title='Register', form=form, mode='register')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Authenticates existing users via bcrypt hash comparisons and establishes an encrypted session.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    return render_template('auth/login_register.html', title='Login', form=form, mode='login')

@bp.route('/logout')
def logout():
    """
    Terminates the active user session and redirects to the landing page.
    """
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

@bp.route('/onboarding', methods=['GET', 'POST'])
@login_required
def onboarding():
    """Onboarding workflow to force users to capture their event interests."""
    if current_user.has_completed_onboarding:
        return redirect(url_for('main.index'))
        
    if request.method == 'POST':
        selected_ids = request.form.getlist('interests')
        if not selected_ids:
            flash('Please select at least one interest to proceed.', 'warning')
            return redirect(url_for('auth.onboarding'))
            
        # Clear existing interests if they somehow exist
        UserInterest.query.filter_by(user_id=current_user.id).delete()
        
        for interest_id in selected_ids:
            user_interest = UserInterest(user_id=current_user.id, interest_id=int(interest_id))
            db.session.add(user_interest)
            
        current_user.has_completed_onboarding = True
        db.session.commit()
        
        flash('Onboarding complete! We have initialized your Recommendation Engine.', 'success')
        return redirect(url_for('events.catalog'))
        
    interests = Interest.query.all()
    return render_template('auth/onboarding.html', interests=interests)

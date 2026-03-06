from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Please log in to access this page.", "warning")
                return redirect(url_for('auth.login'))
            if current_user.role not in roles:
                flash("You do not have permission to view this page.", "danger")
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def student_required(f):
    return role_required('student')(f)

def organizer_required(f):
    return role_required('organizer', 'admin')(f)

def admin_required(f):
    return role_required('admin')(f)

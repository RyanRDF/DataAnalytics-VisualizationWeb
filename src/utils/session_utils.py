"""
Session validation utilities for Flask routes
"""
from flask import session, redirect, url_for, jsonify
from functools import wraps
from typing import Callable, Any
from core.database import UserSession
from utils.timezone_utils import jakarta_now


def get_valid_user_session():
    """
    Get and validate user session from Flask session
    
    Returns:
        tuple: (user_id, user_session) or (None, None) if invalid
    """
    user_id = session.get('user_id')
    session_token = session.get('session_token')
    
    if not user_id or not session_token:
        return None, None
    
    # Verify session is still valid
    user_session = UserSession.query.filter_by(
        user_id=user_id,
        session_token=session_token,
        is_active=True
    ).filter(UserSession.expires_at > jakarta_now()).first()
    
    if not user_session:
        session.clear()
        return None, None
    
    return user_id, user_session


def login_required(redirect_on_fail=True):
    """
    Decorator factory for routes that require login
    
    Args:
        redirect_on_fail: If True, redirects to login page. If False, returns JSON error.
    
    Returns:
        Decorator function
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_id, user_session = get_valid_user_session()
            
            if not user_id or not user_session:
                if redirect_on_fail:
                    return redirect(url_for('login'))
                else:
                    return jsonify({
                        'success': False,
                        'message': 'Anda harus login terlebih dahulu!'
                    }), 401
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def api_login_required(f: Callable) -> Callable:
    """
    Decorator for API routes that require login (returns JSON)
    """
    return login_required(redirect_on_fail=False)(f)





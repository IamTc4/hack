import os
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from firebase_admin import initialize_app, credentials, firestore

# Import configuration and shared database object
from config import Config
from models import db # Import the SQLAlchemy db object
from models.user import User

# Import blueprints
from routes.public import public_bp
from routes.admin import admin_bp

# Import utils
from utils import youtube_video_id

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'

    @login_manager.user_loader
    def load_user(user_id):
        # Since the user ID is just the primary key, we can query for it directly
        return User.query.get(int(user_id))
    
    # --- FIREBASE CLIENT-SIDE SETUP NOTE ---
    # The client-side code in index.html handles the Firestore connection using
    # the global variables (__firebase_config). The Flask backend uses SQLAlchemy
    # for structured data storage (Winners, Tally).

    # Register Blueprints
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Register custom template filters
    app.jinja_env.filters['youtube_video_id'] = youtube_video_id

    # Basic Home Route
    @app.route('/')
    def index():
        # Redirect to the main leaderboard/live view
        return redirect(url_for('public.home'))

    # Context processor to make APP_ID available in all templates
    @app.context_processor
    def inject_global_vars():
        return dict(APP_ID=app.config['APP_ID'])

    return app

if __name__ == '__main__':
    # Add simple .env instructions
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write("SECRET_KEY='your_strong_secret_key_here'\n")
            f.write("FLASK_ENV='development'\n")
            f.write("FLASK_APP='app.py'\n")
            f.write("DATABASE_URI='postgresql://user:password@host:port/dbname'\n")
        print("\n*** Created a basic .env file. Please review and run 'pip install -r requirements.txt'. ***\n")

    app = create_app()

    @app.cli.command("create-admin")
    def create_admin():
        """Creates a default admin user."""
        from models.user import User
        from werkzeug.security import generate_password_hash
        with app.app_context():
            db.create_all()
            if not User.query.filter_by(username="admin").first():
                admin_user = User(username="admin", password=generate_password_hash("admin"))
                db.session.add(admin_user)
                db.session.commit()
                print("Admin user created.")
            else:
                print("Admin user already exists.")

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        print("Database tables created.")

    app.run(debug=True)
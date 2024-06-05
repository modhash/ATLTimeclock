from flask import Flask, render_template
from models import db
from routes import setup_routes
from auth import setup_auth
from export import setup_export
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret_key')

db.init_app(app)
setup_routes(app)
setup_auth(app)
setup_export(app)

@app.route('/')
def index():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)

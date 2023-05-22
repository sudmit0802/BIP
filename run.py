import secrets
from auth import LoginManager, login_required, logout_user, Flask, render_template, redirect, url_for, request, verify_user
from database import create_database, reg_new_user, get_user_from_db, login_user_proxy
from api_interface import get_buildings_routine, get_faculties_routine, get_teachers_routine
from flasgger import Swagger
import asyncio
import sys

app = Flask(__name__)
swagger = Swagger(app)
login_manager = LoginManager()
login_manager.login_view = 'signin'


@login_manager.user_loader
def load_user(user_id):
    return get_user_from_db(user_id)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User registration endpoint.
    ---
    responses:
      200:
        description: User registered successfully.
    """
    return reg_new_user()


@app.route("/", methods=["GET", "POST"])
def signin():
    """
    User login endpoint.
    ---
    responses:
      200:
        description: User logged in successfully.
    """
    return login_user_proxy(request.remote_addr)


@app.route("/verify", methods=["GET", "POST"])
def verify():
    """
    User verification endpoint.
    ---
    parameters:
      - name: username
        in: query
        type: string
        required: true
        description: Username to verify.
    responses:
      200:
        description: User verified successfully.
      302:
        description: Redirect to sign-in page if username is missing.
    """
    username = request.args.get('username')
    if not username:
        return redirect(url_for('signin'))
    return verify_user(username, request.remote_addr)


@app.route("/main", methods=["GET"])
@login_required
def main():
    """
    Main page endpoint.
    ---
    responses:
      200:
        description: Main page rendered successfully.
    """
    return render_template('main.html')


@app.route("/teachers", methods=["GET"])
@login_required
def teachers():
    """
    Teachers endpoint.
    ---
    responses:
      200:
        description: Teachers data retrieved successfully.
    """
    result = asyncio.run(get_teachers_routine())
    return render_template('teachers_template.html', teachers=result)


@app.route("/faculties", methods=["GET"])
@login_required
def faculties():
    """
    Faculties endpoint.
    ---
    responses:
      200:
        description: Faculties data retrieved successfully.
    """
    result = asyncio.run(get_faculties_routine())
    return render_template('faculties_template.html', faculties=result)


@app.route("/buildings", methods=["GET"])
@login_required
def buildings():
    """
    Buildings endpoint.
    ---
    responses:
      200:
        description: Buildings data retrieved successfully.
    """
    result = asyncio.run(get_buildings_routine())
    return render_template('buildings_template.html', buildings=result)


@app.route('/logout')
@login_required
def logout():
    """
    User logout endpoint.
    ---
    responses:
      200:
        description: User logged out successfully.
    """
    logout_user()
    return redirect(url_for('signin'))


if __name__ == "__main__":
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app.secret_key = str(secrets.token_hex(32))
    login_manager.init_app(app)
    create_database()
    app.run(debug=True)

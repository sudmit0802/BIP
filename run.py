import secrets
from functools import wraps
from auth import LoginManager, login_required, logout_user, Flask, render_template, redirect, url_for, request, verify_user, current_user
from database import create_database, reg_new_user, get_user_from_db, login_user_proxy, get_sessions_from_db
from api_interface import get_buildings_routine, get_faculties_routine, get_teachers_routine
from ui import update_sessions, update_main, create_plan, set_deadlines
from flasgger import Swagger
import asyncio
import sys
from flask import send_from_directory

app = Flask(__name__)
swagger = Swagger(app)
login_manager = LoginManager()
login_manager.login_view = 'signin'


def second_factor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        sessions = get_sessions_from_db(current_user.id)
        ips = list()
        if sessions is None:
            return redirect(url_for('signin'))
        for s in sessions:
            ips.append(s['ip'])
        if request.remote_addr not in ips:
            return redirect(url_for('signin'))
        return f(*args, **kwargs)
    return decorated_function


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
    if username and request.referrer:
        if request.referrer.startswith('https://spbstu-ruz-manager.ru'):
            return verify_user(username, request.remote_addr)
    return redirect(url_for('signin'))


@app.route("/main",  methods=["GET", "POST"])
@login_required
@second_factor_required
def main():
    """
    Main page endpoint.
    ---
    responses:
      200:
        description: Main page rendered successfully.
    """
    return update_main(request)


@app.route("/teachers", methods=["GET"])
@login_required
@second_factor_required
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
@second_factor_required
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
@second_factor_required
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


@app.route("/sessions", methods=["GET", "POST"])
@login_required
@second_factor_required
def sessions():
    """
    Session control endpoint.
    ---
    responses:
      200:
        description: success.
    """
    return update_sessions(request)


@app.route("/instruction", methods=["GET"])
def instruction():
    """
    Instruction endpoint.
    ---
    responses:
      200:
        description: success.
    """
    if current_user.is_authenticated:
        sessions = get_sessions_from_db(current_user.id)
        ips = list()
        if sessions is not None:
            for s in sessions:
                ips.append(s['ip'])
            if request.remote_addr in ips:
                return render_template('wide_instruction.html')
    return render_template('instruction.html')


@app.route('/.well-known/acme-challenge/<path:filename>')
def serve_challenge_file(filename):
    return send_from_directory('.well-known/acme-challenge', filename)


@app.route("/new_plan", methods=["GET", "POST"])
@login_required
@second_factor_required
def new_plan():
    """
    New plan endpoint.
    ---
    responses:
      302:
        description: redirection (problems occured)
      200:
        description: plan successfully created.
    """
    return create_plan(request)


@app.route("/new_plan/subjects", methods=["GET", "POST"])
@login_required
@second_factor_required
def subjects():
    """
    Subjects endpoint.
    ---
    responses:
      302:
        description: redirection (problems occured)
      200:
        description: subjects successfully saved.
    """
    return set_deadlines(request)


if __name__ == "__main__":
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app.secret_key = str(secrets.token_hex(32))
    login_manager.init_app(app)
    create_database()

context = ('/etc/letsencrypt/live/spbstu-ruz-manager.ru/fullchain.pem',
           '/etc/letsencrypt/live/spbstu-ruz-manager.ru/privkey.pem')
app.run(port=443, host='10.128.0.11', debug=True, ssl_context=context)

import secrets
from auth import LoginManager, login_required, logout_user, Flask, render_template, redirect, url_for, request, verify_user
from database import create_database, reg_new_user, select_auth, login_user_proxy
from api_interface import get_buildings_routine, get_faculties_routine, get_teachers_routine

app = Flask(__name__)
login_manager = LoginManager()
login_manager.login_view = 'signin'

@login_manager.user_loader
def load_user(user_id):
    return select_auth(user_id)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return reg_new_user()

@app.route("/", methods=["GET", "POST"])
def signin():
    return login_user_proxy()


@app.route("/verify", methods=["GET", "POST"])
def verify():
    username = request.args.get('username')
    #allowed_referrer = url_for('signin')
    #referrer = request.referrer
    #if referrer != allowed_referrer or username == None:
    #    return redirect(url_for('signin'))
    #TODO:"запретить произвольный вход"
    print("пизда ебаная")
    print(username)
    if not username:
        return redirect(url_for('signin'))
    print("пизда")
    print(username)
    return verify_user(username)


@app.route("/main", methods=["GET"])
@login_required
def main():
    return render_template('main.html',
                            teachers_url = url_for('teachers'),
                                faculties_url=url_for('faculties'),
                                    buildings_url=url_for('buildings'))

@app.route("/teachers", methods=["GET"])
@login_required
async def teachers():
    result = await get_teachers_routine()
    return render_template('teachers_template.html', teachers=result)

@app.route("/faculties", methods=["GET"])
@login_required
async def faculties():
    result = await get_faculties_routine()
    return render_template('faculties_template.html', faculties=result)

@app.route("/buildings", methods=["GET"])
@login_required
async def buildings():
    result = await get_buildings_routine()
    return render_template('buildings_template.html', buildings=result)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('signin'))

if __name__ == "__main__":
    app.secret_key = str(secrets.token_hex(32))
    login_manager.init_app(app)
    create_database()
    app.run(debug=True)
import ApiSpbStuRuz
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, current_user
import secrets
import os
import database

app = Flask(__name__)
login_manager = LoginManager()
# определяем страницу входа
login_manager.login_view = 'signin'

@login_manager.user_loader
def load_user(user_id):
    return database.select_auth(user_id)

async def get_teachers_routine():
    res = "teachers"
    async with ApiSpbStuRuz.ApiSpbStuRuz() as api:  
        res = await api.get_teachers()
    return res

async def get_faculties_routine():
    res = "teachers"
    async with ApiSpbStuRuz.ApiSpbStuRuz() as api:  
        res = await api.get_faculties()
    return res

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


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        # Get the submitted login and password
        login = request.form.get("login")
        password = request.form.get("password")

        return database.login_user.login_user_proxy(login, password)
    else:
        cur_file_path = os.path.dirname(__file__)
        file = open(cur_file_path+"/routes/html/signin.html", "r", encoding="utf-8")
        res = file.read()
        file.close()
        return res

@app.route("/main", methods=["GET"])
@login_required
def main():
    cur_file_path = os.path.dirname(__file__)
    file = open(cur_file_path+"/routes/html/main.html", "r", encoding="utf-8")
    res = file.read()
    file.close()
    return res

@app.route("/", methods=["GET"])
def hello():
    cur_file_path = os.path.dirname(__file__)
    file = open(cur_file_path+"/routes/html/hello.html", "r", encoding="utf-8")
    res = file.read()
    file.close()
    return res

@app.route('/signup', methods=['GET', 'POST'])
def register_new():
    return database.reg_new_user()

if __name__ == "__main__":
    app.secret_key = str(secrets.token_hex(32))
    login_manager.init_app(app)
    database.create_database()
    app.run(debug=True)
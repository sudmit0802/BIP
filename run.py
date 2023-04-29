import ApiSpbStuRuz
import secrets
import os
from flask import Flask, render_template, request
from auth import LoginManager, login_required
from database import create_database, reg_new_user, select_auth, login_user_proxy


app = Flask(__name__)
login_manager = LoginManager()
# определяем страницу входа
login_manager.login_view = 'signin'

@login_manager.user_loader
def load_user(user_id):
    return select_auth(user_id)

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

@app.route('/signup', methods=['GET', 'POST'])
def register_new():
    return reg_new_user()

@app.route("/signin", methods=["GET", "POST"])
def signin():
    return login_user_proxy()
    

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

if __name__ == "__main__":
    app.secret_key = str(secrets.token_hex(32))
    login_manager.init_app(app)
    create_database()
    app.run(debug=True)
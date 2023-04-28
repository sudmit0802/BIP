import ApiSpbStuRuz
from flask import Flask, render_template
from flask_login import LoginManager, login_required
import secrets
import auth

app = Flask(__name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return None
    return User(row[0], row[1], row[2], row[3])

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
async def teachers():
    result = await get_teachers_routine()
    return render_template('teachers_template.html', teachers=result)

@app.route("/faculties", methods=["GET"])
async def faculties():
    result = await get_faculties_routine()
    return render_template('faculties_template.html', faculties=result)


@app.route("/signin", methods=["GET"])
def signin():
    file = open("routes/html/signin.html", "r", encoding="utf-8")
    res = file.read()
    file.close()
    return res

@app.route("/signin/confirm", methods=["GET"])
def signin_confirm():
    return "TODO: база данных (Константин)\
            TODO:Бэкэнд входа в систему (Даниил)"

@app.route("/signup", methods=["GET"])
def signup():
    file = open("routes/html/signup.html", "r", encoding="utf-8")
    res = file.read()
    file.close()
    return res

@app.route("/signup/confirm", methods=["GET"])
def signup_confirm():
    return "TODO: база данных (Константин)\
            TODO:Бэкэнд регистрации (Дмитрий)"


@app.route("/main", methods=["GET"])
@login_required
def main():
    file = open("routes/html/main.html", "r", encoding="utf-8")
    res = file.read()
    file.close()
    return res

@app.route("/", methods=["GET"])
def hello():
    file = open("routes/html/hello.html", "r", encoding="utf-8")
    res = file.read()
    file.close()
    return res



if __name__ == "__main__":
    print()
    app.secret_key = str(secrets.token_hex(32))
    login_manager.init_app(app)
    app.run(debug=True)
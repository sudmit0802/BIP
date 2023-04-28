import ApiSpbStuRuz
from flask import Flask, render_template

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






















app = Flask(__name__)

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
    file = open("routes/signin.html", "r", encoding="utf-8")
    res = file.read()
    file.close()
    return res

@app.route("/signin/confirm", methods=["GET"])
def signin_confirm():
    return "TODO: база данных (Константин)\
            TODO:Бэкэнд входа в систему (Даниил)"

@app.route("/signup", methods=["GET"])
def signup():
    file = open("routes/signup.html", "r", encoding="utf-8")
    res = file.read()
    file.close()
    return res

@app.route("/signup/confirm", methods=["GET"])
def signup_confirm():
    return "TODO: база данных (Константин)\
            TODO:Бэкэнд регистрации (Дмитрий)"


@app.route("/main", methods=["GET"])
def main():
    file = open("routes/main.html", "r", encoding="utf-8")
    res = file.read()
    file.close()
    return res

@app.route("/", methods=["GET"])
def hello():
    file = open("routes/hello.html", "r", encoding="utf-8")
    res = file.read()
    file.close()
    return res

if __name__ == "__main__":
    app.run(debug=True)
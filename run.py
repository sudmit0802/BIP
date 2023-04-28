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

@app.route("/", methods=["GET"])
def main_page():
    file = open("index.html", "r", encoding="utf-8")
    res = file.read()
    file.close()
    return res

if __name__ == "__main__":
    app.run(debug=True)
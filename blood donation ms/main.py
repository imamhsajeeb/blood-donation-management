from flask import Flask, request, redirect, render_template, session
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["bloodbankdb"]
users_table = mydb["users"]
blood_table = mydb["bloodinfo"]

#admindict = { "username": "admin", "password": "123456" }

#x = users_table.insert_one(admindict)

app = Flask(__name__)

app.secret_key = 'super secret key'

@app.route('/login', methods=['GET', "POST"])
def login():
    if request.method == "POST":
        form_data = dict(request.form)
        form_username = form_data["username"]
        form_password = form_data["password"]
        db_user = users_table.find_one({"username": form_username})
        if db_user is None:
            return "Username not found"
        if form_password != db_user["password"]:
            return "password did not match"
        session["logged_in"] = True
        session["username"] = form_username

    if "logged_in" in session:
        return redirect("/admin")
    return render_template("login.html", **locals())

@app.route('/bloodcollection', methods=['GET', "POST"])
def bloodcollection():
    if request.method == "POST":
        form_data = dict(request.form)
        x = blood_table.insert_one(form_data)
    return render_template("bloodcollection.html", **locals())

@app.route('/logout', methods=['GET', "POST"])
def logout():
    session.clear()
    return redirect("/")

@app.route('/admin', methods=['GET', "POST"])
def admin():
    return render_template("admin.html")

@app.route('/deleteblood', methods=['GET', "POST"])
def deleteblood():
    if request.method == "POST":
        form_unit = dict(request.form)
        form_unitid = form_unit["unitid"]
        dlt = blood_table.delete_one({"unitid":form_unitid})
    return render_template("deleteblood.html", **locals())


@app.route('/', methods=['GET', "POST"])
def home():
    if request.method=="POST":
        if request.form["search"]=="A+ve":
            return redirect("/resultsA+ve")
        if request.form["search"]=="A-ve":
            return redirect("/resultsA-ve")
        if request.form["search"]=="B+ve":
            return redirect("/resultsB+ve")
        if request.form["search"]=="B-ve":
            return redirect("/resultsB-ve")
        if request.form["search"]=="O+ve":
            return redirect("/resultsO+ve")
        if request.form["search"]=="O-ve":
            return redirect("/resultsO-ve")
        if request.form["search"]=="AB+ve":
            return redirect("/resultsAB+ve")
        if request.form["search"]=="AB-ve":
            return redirect("/resultsAB-ve")
        return request.form
    output = []
    for document in blood_table.find():
        output.append(document)

    if "logged_in" in session:
        return render_template("admin.html")
    return render_template("home.html", **locals() )


@app.route("/resultsA+ve", methods=["GET"])
def resultsApositive():
    output = []
    for document in blood_table.find({"blood": "A+ve"}):
        output.append(document)
    return render_template("search_result.html", output=output)


@app.route("/resultsA-ve", methods=["GET"])
def resultsAnegative():
    output = []
    for document in blood_table.find({"blood": "A-ve"}):
        output.append(document)
    return render_template("search_result.html", output=output)


@app.route("/resultsB+ve", methods=["GET"])
def resultsBpositive():
    output = []
    for document in blood_table.find({"blood": "B+ve"}):
        output.append(document)
    return render_template("search_result.html", output=output)


@app.route("/resultsB-ve", methods=["GET"])
def resultsBnegative():
    output = []
    for document in blood_table.find({"blood": "B-ve"}):
        output.append(document)
    return render_template("search_result.html", output=output)


@app.route("/resultsO+ve", methods=["GET"])
def resultsOpositive():
    output = []
    for document in blood_table.find({"blood": "O+ve"}):
        output.append(document)
    return render_template("search_result.html", output=output)


@app.route("/resultsO-ve", methods=["GET"])
def resultsOnegative():
    output = []
    for document in blood_table.find({"blood": "O-ve"}):
        output.append(document)
    return render_template("search_result.html.html", output=output)


@app.route("/resultsAB+ve", methods=["GET"])
def resultsABpositive():
    output = []
    for document in blood_table.find({"blood": "AB+ve"}):
        output.append(document)
    return render_template("search_result.html", output=output)


@app.route("/resultsAB-ve", methods=["GET"])
def resultsABnegative():
    output = []
    for document in blood_table.find({"blood": "AB-ve"}):
        output.append(document)
    return render_template("search_result.html", output=output)
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002)
    # serve(app, host='127.0.0.1', port=5002)
    # serve(app, host='0.0.0.0', port=80)
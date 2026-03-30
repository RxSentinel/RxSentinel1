from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Load dataset
with open("data.json") as f:
    interactions = json.load(f)


# 🌟 Welcome Page
@app.route("/")
def welcome():
    return render_template("welcome.html")


# 👤 Patient Details Page
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")

        return redirect(url_for("check", name=name, age=age, gender=gender))

    return render_template("home.html")


# 💊 Medicine Check Page
@app.route("/check", methods=["GET", "POST"])
def check():
    result = None

    if request.method == "POST":
        try:
            d1 = request.form.get("drug1", "").strip().lower()
            d2 = request.form.get("drug2", "").strip().lower()
            d3 = request.form.get("drug3", "").strip().lower()

            drugs = [d1, d2]
            if d3:
                drugs.append(d3)

            found = None

            for i in range(len(drugs)):
                for j in range(i + 1, len(drugs)):
                    for item in interactions:
                        if (drugs[i] == item["drug1"] and drugs[j] == item["drug2"]) or \
                           (drugs[i] == item["drug2"] and drugs[j] == item["drug1"]):
                            found = item
                            break

            if found:
                result = found
            else:
                result = {
                    "risk": "Low",
                    "reason": "No major interaction found in current dataset"
                }

        except Exception as e:
            result = {
                "risk": "Error",
                "reason": "Something went wrong. Please try again."
            }

    return render_template("result.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Load dataset
with open("data.json") as f:
    interactions = json.load(f)

# Store history (temporary)
history = []


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

    name = request.args.get("name")
    age = request.args.get("age")
    gender = request.args.get("gender")

    if request.method == "POST":
        try:
            input_drugs = request.form.get("drugs", "")
            drugs = [d.strip().lower() for d in input_drugs.split(",") if d.strip()]

            results = []

            # Pairwise checking
            for i in range(len(drugs)):
                for j in range(i + 1, len(drugs)):
                    for item in interactions:
                        if (drugs[i] == item["drug1"] and drugs[j] == item["drug2"]) or \
                           (drugs[i] == item["drug2"] and drugs[j] == item["drug1"]):
                            results.append({
                                "pair": f"{drugs[i]} + {drugs[j]}",
                                "risk": item["risk"],
                                "reason": item["reason"]
                            })

            # If no interactions found
            if results:
                result = results
            else:
                result = [{
                    "pair": "No major interaction",
                    "risk": "Low",
                    "reason": "No major interaction found in current dataset"
                }]

            # Save history
            history.append({
                "drugs": drugs,
                "risk": result[0]["risk"]
            })

        except Exception as e:
            result = [{
                "pair": "Error",
                "risk": "Error",
                "reason": "Something went wrong. Please try again."
            }]

    return render_template(
        "result.html",
        result=result,
        history=history,
        name=name,
        age=age,
        gender=gender
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
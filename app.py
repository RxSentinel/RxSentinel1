from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

with open("data.json") as f:
    interactions = json.load(f)

history = []

@app.route("/", methods=["GET"])
def welcome():
    return render_template("welcome.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")

        return redirect(url_for("check", name=name, age=age, gender=gender))

    return render_template("home.html")

@app.route("/check", methods=["GET", "POST"])
def check():
    name = request.args.get("name")
    age = request.args.get("age")
    gender = request.args.get("gender")

    result = []

    if request.method == "POST":
        drugs = request.form.get("drugs", "").strip()
        file = request.files.get("file")

        # Simulated OCR
        if not drugs and file:
            drugs = "paracetamol, ibuprofen"

        drug_list = [d.strip().lower() for d in drugs.split(",") if d.strip()]

        for i in range(len(drug_list)):
            for j in range(i + 1, len(drug_list)):
                d1, d2 = drug_list[i], drug_list[j]

                found = False
                for item in interactions:
                    if (d1 == item["drug1"] and d2 == item["drug2"]) or \
                       (d1 == item["drug2"] and d2 == item["drug1"]):

                        result.append({
                            "pair": f"{d1} + {d2}",
                            "risk": item["risk"],
                            "reason": item["reason"]
                        })
                        found = True
                        break

                if not found:
                    result.append({
                        "pair": f"{d1} + {d2}",
                        "risk": "Low",
                        "reason": "No major interaction found"
                    })

        # Save history
        history.append({
            "drugs": drugs,
            "risk": result[0]["risk"] if result else "Low"
        })

    return render_template("result.html",
                           result=result,
                           history=history,
                           name=name,
                           age=age,
                           gender=gender)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Frontend: postrezi index.html iz mape 'frontend'
@app.get("/")
def home():
    return send_from_directory("frontend", "index.html")

# API: prejmi JSON iz frontenda in IZPIŠI VSE VREDNOSTI
@app.post("/api/calc")
def api_calc():
    data = request.get_json(force=True, silent=True) or {}

    initial = data.get("initial")
    monthly = data.get("monthly")
    index_key = data.get("index")
    interval = data.get("interval")



    # ...
    print("\n" + "=" * 40)
    print("📊 PREJETI PODATKI IZ FRONTENDA")
    print("=" * 40)
    print(f"💰 Začetna investicija : {initial} €")
    print(f"💸 Mesečni vložek      : {monthly} €")
    print(f"📈 Indeks              : {index_key}")
    print(f"⏳ Interval            : {interval} let")
    print("=" * 40 + "\n")

    # (opcijsko) preveri številke
    
    # osnovna validacija index-a (po želji strožja)
    if index_key not in {"sp500", "nasdaq100", "nasdaqcomposite"}:
        return jsonify({"ok": False, "error": "Neveljavna izbira indeksa."}), 400

    # vrni echo nazaj frontendu
    return jsonify({
        "ok": True,
        "echo": {
            "initial": initial,
            "monthly": monthly,
            "index": index_key,
            "interval": interval
        }
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)

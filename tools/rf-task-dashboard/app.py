"""RF EC-screen conversion task board - small local Flask app.

Run: py -m pip install -r requirements.txt && py app.py
Then open http://localhost:5057/
"""
from flask import Flask, jsonify, render_template, request

import models

app = Flask(__name__)
models.init_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tasks", methods=["GET"])
def api_list_tasks():
    status = request.args.get("status")
    return jsonify(models.list_tasks(status=status))


@app.route("/api/tasks", methods=["POST"])
def api_add_task():
    body = request.get_json(force=True) or {}
    screen_name = (body.get("screen_name") or "").strip()
    if not screen_name:
        return jsonify({"error": "screen_name is required"}), 400
    pattern = (body.get("pattern") or "UNKNOWN").strip().upper()
    try:
        task_id = models.add_task(screen_name, pattern)
    except Exception as exc:  # noqa: BLE001 - surface a clean 400 for dup names etc.
        return jsonify({"error": str(exc)}), 400
    return jsonify(models.get_task(task_id)), 201


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def api_get_task(task_id):
    task = models.get_task(task_id)
    if not task:
        return jsonify({"error": "not found"}), 404
    task["history"] = models.get_history(task_id)
    return jsonify(task)


@app.route("/api/tasks/<int:task_id>/claim", methods=["POST"])
def api_claim_task(task_id):
    body = request.get_json(force=True) or {}
    claimed_by = (body.get("claimed_by") or "").strip()
    if not claimed_by:
        return jsonify({"error": "claimed_by is required"}), 400
    task, error = models.claim_task(task_id, claimed_by)
    if error:
        return jsonify({"error": error}), 409
    return jsonify(task)


@app.route("/api/tasks/<int:task_id>/status", methods=["POST"])
def api_update_status(task_id):
    body = request.get_json(force=True) or {}
    new_status = (body.get("status") or "").strip()
    note = body.get("note")
    pr_number = body.get("pr_number")
    task, error = models.update_status(task_id, new_status, note=note, pr_number=pr_number)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(task)


@app.route("/api/summary", methods=["GET"])
def api_summary():
    return jsonify(models.summary())


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5057, debug=False)

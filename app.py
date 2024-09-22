from flask import Flask, jsonify, request, render_template
import json
import os
import yaml
from datetime import datetime

app = Flask(__name__)

# Paths to the JSON and YAML files
TASKS_FILE = "tasks.json"
CATEGORIES_FILE = "categories.yaml"

# Ensure the tasks.json file exists
if not os.path.exists(TASKS_FILE):
    with open(TASKS_FILE, "w") as f:
        json.dump([], f)


# Load tasks from the JSON file
def load_tasks():
    with open(TASKS_FILE, "r") as file:
        tasks = json.load(file)
    return tasks


# Save tasks to the JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file)


# Load categories from the YAML file
def load_categories():
    with open(CATEGORIES_FILE, "r") as file:
        data = yaml.safe_load(file)
    return data.get("categories", [])


# Serve the HTML page
@app.route("/")
def index():
    categories = load_categories()
    return render_template("index.html", categories=categories)


# Endpoint to get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)


# Endpoint to add/update tasks
@app.route("/tasks", methods=["POST"])
def save_task():
    tasks = request.json.get("tasks", [])

    # Automatically add completion date when a task is marked as completed
    for task in tasks:
        if task.get("completed") and not task.get("completedDate"):
            # Set the completedDate to today's date when the task is marked as completed
            task["completedDate"] = datetime.now().strftime("%Y-%m-%d")
        elif not task.get("completed"):
            # If the task is unchecked, remove the completedDate
            task["completedDate"] = None

    save_tasks(tasks)
    return jsonify({"status": "success"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=42069, debug=True)

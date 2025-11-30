from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# ---- your existing logic, slightly simplified ----
tasks = []
FILE_NAME = "tasks.txt"

def load_tasks():
    global tasks
    tasks = []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|", 2)
                done_str = parts[0]
                title = parts[1]
                due_str = parts[2] if len(parts) > 2 else ""
                done = (done_str == "1")
                tasks.append({"title": title, "done": done, "due": due_str})
    except FileNotFoundError:
        tasks = []

def save_tasks():
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        for task in tasks:
            done_str = "1" if task["done"] else "0"
            due_str = task.get("due", "")
            f.write(f"{done_str}|{task['title']}|{due_str}\n")

# ---- HTML template (very simple, all in one file for now) ----
PAGE = """
<!doctype html>
<html>
  <head>
    <title>Smart Task Manager</title>
    <style>
      body { font-family: sans-serif; max-width: 600px; margin: 20px auto; }
      h1 { text-align: center; }
      .done { text-decoration: line-through; color: gray; }
      ul { list-style: none; padding: 0; }
      li { margin: 5px 0; }
      form { margin-top: 15px; }
      button { margin-left: 5px; }
    </style>
  </head>
  <body>
    <h1>Smart Task Manager</h1>

    {% if tasks %}
    <ul>
      {% for i, task in enumerate(tasks) %}
        <li>
          {% if task.done %}
            ✅ <span class="done">{{ i+1 }}. {{ task.title }}</span>
          {% else %}
            ⬜ {{ i+1 }}. {{ task.title }}
          {% endif %}
          {% if task.due %}
            <small>(due: {{ task.due }})</small>
          {% endif %}
          <form action="{{ url_for('complete_task', index=i) }}" method="post" style="display:inline;">
            <button type="submit">Complete</button>
          </form>
          <form action="{{ url_for('delete_task', index=i) }}" method="post" style="display:inline;">
            <button type="submit">Delete</button>
          </form>
        </li>
      {% endfor %}
    </ul>
    {% else %}
      <p>No tasks yet.</p>
    {% endif %}

    <h2>Add Task</h2>
    <form action="{{ url_for('add_task') }}" method="post">
      <input type="text" name="title" placeholder="Task title" required>
      <input type="text" name="due" placeholder="Due date (optional)">
      <button type="submit">Add</button>
    </form>
  </body>
</html>
"""

# ---- Flask routes ----

@app.route("/")
def index():
    load_tasks()
    return render_template_string(PAGE, tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    load_tasks()
    title = request.form.get("title", "").strip()
    due = request.form.get("due", "").strip()
    if title:
        tasks.append({"title": title, "done": False, "due": due})
        save_tasks()
    return redirect(url_for("index"))

@app.route("/complete/<int:index>", methods=["POST"])
def complete_task(index):
    load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["done"] = True
        save_tasks()
    return redirect(url_for("index"))

@app.route("/delete/<int:index>", methods=["POST"])
def delete_task(index):
    load_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks()
    return redirect(url_for("index"))

if __name__ == "__main__":
    print("starting task_app...")
    app.run(debug=True)


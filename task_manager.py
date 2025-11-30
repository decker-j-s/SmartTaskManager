from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
from rich.prompt import Prompt, IntPrompt
import datetime
from pathlib import Path

console = Console()
tasks = []
FILE_NAME = "tasks.txt"

def load_tasks():
    global tasks
    tasks = []
    path = Path(FILE_NAME)
    if not path.exists(): return
    try:
        lines = path.read_text(encoding="utf-8").strip().split("\n")
        for line in lines:
            if not line.strip(): continue
            parts = line.split("|", 2)
            done = parts[0] == "1"
            title = parts[1]
            due = parts[2] if len(parts) > 2 else ""
            tasks.append({"title": title, "done": done, "due": due})
    except:
        pass

def save_tasks():
    lines = []
    for task in tasks:
        done_str = "1" if task["done"] else "0"
        due_str = task.get("due", "")
        lines.append(f"{done_str}|{task['title']}|{due_str}")
    Path(FILE_NAME).write_text("\n".join(lines), encoding="utf-8")

def show_tasks():
    if not tasks:
        console.print(Panel("No tasks yet. Add some!", title="📝 Tasks", style="bold cyan"))
        return
    
    table = Table(title="📋 Your Tasks", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Status", style="green", no_wrap=True)
    table.add_column("Task", style="white")
    table.add_column("Due", style="yellow")
    
    for i, task in enumerate(tasks, 1):
        status = "✅" if task["done"] else "⬜"
        due = task.get("due", "None")
        table.add_row(str(i), status, task["title"], due)
    
    console.print(table)

def add_task():
    title = Prompt.ask("📝 Task title")
    due = Prompt.ask("📅 Due date (YYYY-MM-DD)", default="")
    tasks.append({"title": title, "done": False, "due": due})
    save_tasks()
    console.print(f"✨ [bold green]'{title}' added![/bold green]")

def complete_task():
    show_tasks()
    if not tasks: return
    try:
        num = IntPrompt.ask("✅ Task number to complete")
        tasks[num-1]["done"] = True
        save_tasks()
        console.print("[bold green]✅ Marked complete![/bold green]")
    except:
        console.print("[bold red]❌ Invalid number[/bold red]")

def delete_task():
    show_tasks()
    if not tasks: return
    try:
        num = IntPrompt.ask("🗑️ Task number to delete")
        deleted = tasks.pop(num-1)
        save_tasks()
        console.print(f"[bold red]🗑️ Deleted '{deleted['title']}'[/bold red]")
    except:
        console.print("[bold red]❌ Invalid number[/bold red]")

def main():
    console.print(Panel("🚀 Smart Task Manager", style="bold blue on yellow"))
    load_tasks()
    
    while True:
        console.print("\n[bold cyan]1. 📋 Show tasks[/]  2. ➕ Add  3. ✅ Complete  4. 🗑️ Delete  5. 🚪 Exit")
        choice = Prompt.ask("Choose")
        
        if choice == "1": show_tasks()
        elif choice == "2": add_task()
        elif choice == "3": complete_task()
        elif choice == "4": delete_task()
        elif choice == "5": 
            console.print("[bold green]👋 Goodbye![/]")
            break
        else: console.print("[bold red]❌ Invalid choice[/bold red]")

if __name__ == "__main__":
    main()

import argparse
import sys
import os
import json

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE) or os.path.getsize(TASKS_FILE) == 0:
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_task(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Hack Club Task Manager")
    parser.add_argument("task", type=str, nargs="?", help="Task description to add")
    parser.add_argument("-l", "--list", action="store_true", help="List all tasks")
    parser.add_argument("-c", "--complete", type=int, help="Mark task complete by ID")
    parser.add_argument("-d", "--delete", type=int, help="Delete a task by ID")
    parser.add_argument("-p", "--priority", choices=["low", "medium", "high"], default="medium", help="Priority level")
    parser.add_argument("--version", action="version", version="TaskCLI 0.1.0")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

   
    if args.list:
        tasks = load_tasks()
        if not tasks:
            print("📭 No tasks found. Add one: python main.py 'Task Name'")
            return

        priority_order = {"high": 3, "medium": 2, "low": 1}
        tasks.sort(key=lambda t: priority_order.get(t["priority"], 2), reverse=True)

        print(f"\n{'ID':<3} | {'Status':<8} | {'Priority':<8} | {'Task'}")
        print("-" * 40)
        for t in tasks:
            status = "✅ Done" if t["done"] else "⏳ Pending"
            print(f"{t['id']:<3} | {status:<8} | {t['priority']:<8} | {t['task']}")


    elif args.complete:
        tasks = load_tasks()
        found = False
        for t in tasks:
            if t["id"] == args.complete:
                t["done"] = True
                found = True
                break
        
        if found:
            save_task(tasks)
            print(f"✔️ Task {args.complete} marked as complete!")
        else:
            print(f"❌ Error: Task ID {args.complete} not found.")

    elif args.delete:
        tasks = load_tasks()
        initial_count = len(tasks)
        new_tasks = [t for t in tasks if t["id"] != args.delete]

        if len(new_tasks) < initial_count:
            save_task(new_tasks)
            print(f"🗑️ Task {args.delete} deleted.")
        else:
            print(f"❌ Error: Task ID {args.delete} not found.")

  
    elif args.task:
        tasks = load_tasks()
        
        new_id = max([t["id"] for t in tasks], default=0) + 1

        tasks.append({
            "id": new_id,
            "task": args.task,
            "done": False,
            "priority": args.priority
        })
        save_task(tasks)
        print(f"➕ Added: '{args.task}' (ID: {new_id}, Priority: {args.priority})")

if __name__ == "__main__":
    main()
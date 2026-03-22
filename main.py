from task_manager import Task, ChecklistTask
from time_tracker import AutoTimeEntry, ManualTimeEntry
from datetime import datetime, timedelta
from task_manager import Project
import time

def main():
    study_project = "Study"
    meals_project = "Meals"
    exercise_project = "Exercise"
    sleep_project = "Sleep"

    subjects = ["IT111", "IT135", "EET131"]
    study_tasks = []
    for sub in subjects:
        task = Task(sub, study_project, f"Study {sub}")
        study_tasks.append(task)

    meals = ["Breakfast", "Lunch", "Dinner"]
    meal_tasks = []
    for meal in meals:
        task = Task(meal, meals_project, f"Eat {meal}")
        meal_tasks.append(task)

    exercise_task = Task("Exercise", exercise_project, "One hour workout")

    walk_tasks = []
    for i in range(2):
        task = Task(f"Walk {i+1}", exercise_project, "15 minute walk")
        walk_tasks.append(task)

    
    sleep_task = Task("Sleep", sleep_project, "8 hours of sleep")

    
    print("=== Task Management System ===")

    all_tasks = study_tasks + meal_tasks + [exercise_task] + walk_tasks + [sleep_task]
    for task in all_tasks:
        print(f"{task.name} ({task.project}) – {task.description}")

    print("\n--- Time Tracking Demo ---")
    test_task = study_tasks[0]
    auto = AutoTimeEntry(test_task)
    auto.start()
    time.sleep(2)
    auto.stop()
    print(f"Auto duration: {auto.get_duration()}")

    start = datetime.now() - timedelta(hours=1)
    end = start + timedelta(minutes=45)
    manual = ManualTimeEntry(test_task, start, end)
    manual.start()
    print(f"Manual duration: {manual.get_duration()}")

if __name__ == "__main__":
    main()
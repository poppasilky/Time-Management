class Task:
    def __init__(self, name, project, description=""):
        self.name = name
        self.project = project
        self.description = description
        self.done = False

    def summary(self):
        status = "✓" if self.done else "✗"
        return f"{self.name} [{self.project}] {status} – {self.description}"

class ChecklistTask(Task):
    def __init__(self, name, project, description=""):
        super().__init__(name, project, description)
        self._subtasks = []   

    def add_subtask(self, description):
        self._subtasks.append({"desc": description, "done": False})

    def complete_subtask(self, index):
        if 0 <= index < len(self._subtasks):
            self._subtasks[index]["done"] = True

    def is_complete(self):
        return all(item["done"] for item in self._subtasks)
    
    def progress(self):
        if not self._subtasks:
            return 0.0
        done_count = sum(1 for s in self._subtasks if s.done)
        return (done_count / len(self._subtasks)) * 100
    
    def summary(self):
        base = super().summary()
        subtask_status = ", ".join(
            f"{item['desc']} ({'✓' if item['done'] else '✗'})"
            for item in self._subtasks
        )
        return f"{base} Subtasks: [{subtask_status}]"

class Project:
    def __init__(self, name, description=""):
        self._name = name
        self._description = description
        self._tasks = []

    def get_name(self):
        return self._name

    def get_description(self):
        return self._description

    def add_task(self, task):
        if task not in self._tasks:
            self._tasks.append(task)

    def remove_task(self, task):
        if task in self._tasks:
            self._tasks.remove(task)

    def get_tasks(self):
        return self._tasks.copy()
    
    def completion_percentage(self):
        if not self._tasks:
            return 0.0
        done_count = sum(1 for task in self._tasks if task.done)
        return (done_count / len(self._tasks)) * 100

    def summary(self):
        return f"Project: {self._name} – {self._description} ({len(self._tasks)} tasks)"     


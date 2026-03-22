from datetime import datetime

class Task:
    def __init__(self, name, project, description="", planned_time=None, duration_minutes=None):
        self.name = name
        self.project = project
        self.description = description
        self.done = False
        self.planned_time = planned_time
        self.duration_minutes = duration_minutes

    def summary(self):
        status = "✓" if self.done else "✗"
        parts = [f"{self.name} [{self.project.get_name()}]"]
        if self.planned_time:
            parts.append(self.planned_time.strftime("@ %H:%M"))
        if self.duration_minutes:
            parts.append(f"({self.duration_minutes} min)")
        parts.append(status)
        if self.description:
            parts.append("– " + self.description)
        return " ".join(parts)

    def time_sort_key(self):
        if self.planned_time:
            return self.planned_time.timestamp()
        return float('inf')

class ChecklistTask(Task):
    def __init__(self, name, project, description="", planned_time=None, duration_minutes=None):
        super().__init__(name, project, description, planned_time, duration_minutes)
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
        done_count = sum(1 for s in self._subtasks if s["done"])
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

class TimeEntry:
    def __init__(self, task):
        self._task = task
        self._start_time = None
        self._end_time = None

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def get_duration(self):
        if self._start_time and self._end_time:
            return self._end_time - self._start_time
        return None

    def format_duration(self):
        delta = self.get_duration()
        if not delta:
            return "Not completed"
        total_seconds = int(delta.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def get_task(self):
        return self._task

class AutoTimeEntry(TimeEntry):
    def start(self):
        self._start_time = datetime.now()
        print(f"Started {self.get_task().name} at {self._start_time}")

    def stop(self):
        self._end_time = datetime.now()
        print(f"Stopped {self.get_task().name}. Duration: {self.get_duration()}")

class ManualTimeEntry(TimeEntry):
    def __init__(self, task, start_time, end_time):
        super().__init__(task)
        self._start_time = start_time
        self._end_time = end_time

    def start(self):
        print(f"Manual entry for {self.get_task().name} from {self._start_time.strftime('%H:%M:%S')} to {self._end_time.strftime('%H:%M:%S')} – Duration: {self.format_duration()}")

    def stop(self):
        pass
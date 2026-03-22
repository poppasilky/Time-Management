from datetime import datetime
from task_manager import Task

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
    

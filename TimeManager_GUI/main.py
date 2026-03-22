import sys
import os
import requests
import numpy as np
import pandas as pd
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                               QVBoxLayout, QListWidget, QLineEdit, QHBoxLayout,
                               QComboBox, QTimeEdit, QListWidgetItem, QDialog,
                               QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt, QTime, QTimer
from time_manager import Task, Project

class ReportDialog(QDialog):
    """Dialog showing a table of total planned time per project."""
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Time Allocation Report")
        self.setGeometry(150, 150, 400, 300)
        layout = QVBoxLayout()
        self.setLayout(layout)

        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Project", "Total Hours"])
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        table.setRowCount(len(data))
        for row, (project, hours) in enumerate(data.items()):
            table.setItem(row, 0, QTableWidgetItem(project))
            table.setItem(row, 1, QTableWidgetItem(f"{hours:.2f}"))

        layout.addWidget(table)

class TimeManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Daily Planner")
        self.setGeometry(100, 100, 600, 650)
        self.light_style = """
            QWidget {
                background-color: #f0f2f5;
                color: #333;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 12px;
    }
            QListWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 4px;
    }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
    }
            QPushButton:hover {
                background-color: #3b7ac2;
    }
            QLineEdit, QTimeEdit, QComboBox {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 4px;
                background: white;
    }
            QLabel {
                color: #333;
    }
"""

        self.dark_style = """
            QWidget {
                background-color: #2b2b2b;
                color: #f0f0f0;
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-size: 12px;
    }
            QListWidget {
                background-color: #3c3c3c;
                border: 1px solid #555;
                border-radius: 4px;
    }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
    }
            QPushButton:hover {
                background-color: #6a1b9a;
    }
            QLineEdit, QTimeEdit, QComboBox {
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px;
                background: #3c3c3c;
                color: #f0f0f0;
    }
            QLabel {
                color: #f0f0f0;
    }
""" 
        self.setStyleSheet(self.light_style)
  
        self.projects = []
        self.setup_sample_tasks()

        # Task list
        self.task_list = QListWidget()
        self.task_list.itemChanged.connect(self.on_task_toggled)
        self.refresh_task_list()

        # Input area for new task
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("New Task:"))
        self.new_task_name = QLineEdit()
        self.new_task_name.setPlaceholderText("e.g., Study IT111")
        input_layout.addWidget(self.new_task_name)

        input_layout.addWidget(QLabel("Time:"))
        self.new_task_time = QTimeEdit()
        self.new_task_time.setTime(QTime.currentTime())
        self.new_task_time.setDisplayFormat("HH:mm")
        input_layout.addWidget(self.new_task_time)

        self.add_button = QPushButton("Add Task")
        self.add_button.clicked.connect(self.add_task)
        input_layout.addWidget(self.add_button)

        # Report button
        button_row = QHBoxLayout()
        self.report_button = QPushButton("Show Report")
        self.report_button.clicked.connect(self.show_report)
        self.toggle_theme_button = QPushButton("Dark Mode")
        self.toggle_theme_button.clicked.connect(self.toggle_theme)
        button_row.addWidget(self.report_button)
        button_row.addWidget(self.toggle_theme_button)
        
        # ----- Weather Section -----
        # City row
        city_layout = QHBoxLayout()
        city_layout.addWidget(QLabel("City:"))
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("e.g., Seattle")
        self.city_input.setText("Seattle")
        city_layout.addWidget(self.city_input)

        # Units & Weather button row (units on left, clock, then button on right)
        units_weather_layout = QHBoxLayout()
        units_weather_layout.addWidget(QLabel("Units:"))
        self.unit_combo = QComboBox()
        self.unit_combo.addItem("Metric (°C, km/h)", "metric")
        self.unit_combo.addItem("Imperial (°F, mph)", "imperial")
        self.unit_combo.currentIndexChanged.connect(self.on_unit_changed)
        units_weather_layout.addWidget(self.unit_combo)

        # Add the clock label
        self.clock_label = QLabel()
        self.clock_label.setAlignment(Qt.AlignRight)
        units_weather_layout.addWidget(self.clock_label)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)
        self.update_clock()
        units_weather_layout.addStretch()

        self.weather_button = QPushButton("Get Weather")
        self.weather_button.setFixedWidth(120)
        self.weather_button.clicked.connect(self.fetch_weather)
        units_weather_layout.addWidget(self.weather_button)

        # Weather label
        self.weather_label = QLabel("Enter a city and click 'Get Weather'")
        self.weather_label.setWordWrap(True)
        self.weather_label.setAlignment(Qt.AlignCenter)

        # ----- Main Layout -----
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Today's Plan (sorted by time):"))
        layout.addWidget(self.task_list)
        layout.addLayout(input_layout)
        layout.addLayout(button_row)
        layout.addLayout(city_layout)
        layout.addLayout(units_weather_layout)   # new combined row
        layout.addWidget(self.weather_label)
        self.setLayout(layout)

        self.last_city = ""
        self.last_units = None

    def setup_sample_tasks(self):
        from datetime import datetime, time

        study_project = Project("Study", "Study related tasks")
        meals_project = Project("Meals", "Meal times")
        exercise_project = Project("Exercise", "Physical activity")
        sleep_project = Project("Sleep", "Rest")

        today = datetime.today().date()

        # Schedule with durations (in minutes)
        t1 = Task("Breakfast", meals_project, "Eat breakfast",
                  datetime.combine(today, time(7, 30)), duration_minutes=30)
        meals_project.add_task(t1)

        t2 = Task("IT111", study_project, "Study IT111",
                  datetime.combine(today, time(8, 0)), duration_minutes=120)
        study_project.add_task(t2)

        t3 = Task("Walk 1", exercise_project, "15 min walk",
                  datetime.combine(today, time(10, 0)), duration_minutes=15)
        exercise_project.add_task(t3)

        t4 = Task("IT135", study_project, "Study IT135",
                  datetime.combine(today, time(10, 15)), duration_minutes=120)
        study_project.add_task(t4)

        t5 = Task("Lunch", meals_project, "Eat lunch",
                  datetime.combine(today, time(12, 15)), duration_minutes=45)
        meals_project.add_task(t5)

        t6 = Task("EET131", study_project, "Study EET131",
                  datetime.combine(today, time(13, 0)), duration_minutes=120)
        study_project.add_task(t6)

        t7 = Task("Exercise", exercise_project, "1 hour workout",
                  datetime.combine(today, time(15, 30)), duration_minutes=60)
        exercise_project.add_task(t7)

        t8 = Task("Dinner", meals_project, "Eat dinner",
                  datetime.combine(today, time(18, 30)), duration_minutes=30)
        meals_project.add_task(t8)

        t9 = Task("Walk 2", exercise_project, "15 min walk",
                  datetime.combine(today, time(20, 30)), duration_minutes=15)
        exercise_project.add_task(t9)

        t10 = Task("Sleep", sleep_project, "8 hours sleep",
                   datetime.combine(today, time(22, 0)), duration_minutes=480)
        sleep_project.add_task(t10)

        self.projects = [study_project, meals_project, exercise_project, sleep_project]

    def toggle_theme(self):
        if self.toggle_theme_button.text() == "Dark Mode":
            self.setStyleSheet(self.dark_style)
            self.toggle_theme_button.setText("Light Mode")
        else:
            self.setStyleSheet(self.light_style)
            self.toggle_theme_button.setText("Dark Mode")

    def refresh_task_list(self):
        self.task_list.clear()
        all_tasks = []
        for proj in self.projects:
            for task in proj.get_tasks():
                all_tasks.append(task)

        all_tasks.sort(key=lambda t: t.time_sort_key())

        for task in all_tasks:
            item = QListWidgetItem(task.summary())
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if task.done else Qt.Unchecked)
            item.setData(Qt.UserRole, task)
            self.task_list.addItem(item)

    def on_task_toggled(self, item):
        task = item.data(Qt.UserRole)
        if task:
            task.done = (item.checkState() == Qt.Checked)
            item.setText(task.summary())

    def add_task(self):
        name = self.new_task_name.text().strip()
        if not name:
            return
        target_project = self.projects[0]
        qtime = self.new_task_time.time()
        from datetime import datetime, time
        planned = datetime.combine(datetime.today(), time(qtime.hour(), qtime.minute()))
        new_task = Task(name, target_project, description="", planned_time=planned)
        target_project.add_task(new_task)
        self.new_task_name.clear()
        self.refresh_task_list()

    def show_report(self):
        data = []
        for proj in self.projects:
            for task in proj.get_tasks():
                if task.duration_minutes:
                    data.append({
                        'project': proj.get_name(),
                        'duration_minutes': task.duration_minutes
                    })
        if not data:
            return
        df = pd.DataFrame(data)
        project_hours = df.groupby('project')['duration_minutes'].sum() / 60.0
        plot_data = project_hours.to_dict()
        dlg = ReportDialog(plot_data, self)
        dlg.setStyleSheet(self.styleSheet())
        dlg.exec()

    def get_coordinates(self, city):
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        try:
            resp = requests.get(geo_url)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("results"):
                    result = data["results"][0]
                    lat = result["latitude"]
                    lon = result["longitude"]
                    name = result["name"]
                    country = result.get("country", "")
                    return lat, lon, f"{name}, {country}"
        except:
            pass
        return None, None, None

    def on_unit_changed(self):
        city = self.city_input.text().strip()
        if city and self.last_city == city:
            self.fetch_weather()

    def get_weather_emoji(self, code):
        if code == 0:
            return "☀️"
        elif code in [1, 2, 3]:
            return "⛅"
        elif code in [45, 48]:
            return "🌫️"
        elif code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]:
            return "🌧️"
        elif code in [71, 73, 75, 77, 85, 86]:
            return "❄️"
        elif code in [95, 96, 99]:
            return "⛈️"
        else:
            return "🌈"

    def fetch_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.weather_label.setText("Please enter a city name.")
            return
        unit = self.unit_combo.currentData()
        self.last_city = city
        self.last_units = unit
        lat, lon, display_name = self.get_coordinates(city)
        if lat is None:
            self.weather_label.setText(f"Could not find coordinates for '{city}'.")
            return
        if unit == "metric":
            temp_unit = "celsius"
            wind_unit = "kmh"
            temp_label = "°C"
            wind_label = "km/h"
        else:
            temp_unit = "fahrenheit"
            wind_unit = "mph"
            temp_label = "°F"
            wind_label = "mph"
        weather_url = (f"https://api.open-meteo.com/v1/forecast"
                       f"?latitude={lat}&longitude={lon}"
                       f"&current_weather=true"
                       f"&temperature_unit={temp_unit}"
                       f"&wind_speed_unit={wind_unit}")
        try:
            resp = requests.get(weather_url)
            if resp.status_code == 200:
                data = resp.json()
                weather = data['current_weather']
                temp = weather['temperature']
                wind = weather['windspeed']
                code = weather['weathercode']
                emoji = self.get_weather_emoji(code)
                if code == 0:
                    condition = "Clear"
                elif code in [1, 2, 3]:
                    condition = "Partly cloudy"
                elif code in [45, 48]:
                    condition = "Foggy"
                elif code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]:
                    condition = "Rainy"
                elif code in [71, 73, 75, 77, 85, 86]:
                    condition = "Snowy"
                elif code in [95, 96, 99]:
                    condition = "Thunderstorm"
                else:
                    condition = "Unknown"
                self.weather_label.setText(
                    f"{emoji}  {display_name}\n"
                    f"{condition}\n"
                    f"Temperature: {temp}{temp_label}\n"
                    f"Wind: {wind} {wind_label}"
                )
            else:
                self.weather_label.setText("Could not fetch weather data.")
        except Exception as e:
            self.weather_label.setText(f"Error: {e}")
        
    def update_clock(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.clock_label.setText(current_time)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimeManagerApp()
    window.show()
    sys.exit(app.exec())
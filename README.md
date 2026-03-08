# Time Manager

A personal task scheduler designed to help manage daily school workload by planning tasks and breaks. Built as part of the IT111 Programming Fundamentals course.

## Features

- **Pre‑planned daily schedule** – tasks with set times (breakfast, study blocks, walks, exercise, dinner, sleep).
- **Interactive task list** – check off tasks as you complete them; tasks are automatically sorted by time.
- **Weather integration** – fetch current weather for any city using the free Open‑Meteo API.
- **Unit toggle** – switch between metric (°C, km/h) and imperial (°F, mph).
- **Time report** – view a summary of total planned hours per project (e.g., Study, Meals, Exercise, Sleep).

## Project Structure

- `TimeManager_GUI/` – the graphical user interface version.
  - `main.py` – runs the GUI application.
  - `time_manager.py` – contains the core classes (`Task`, `Project`, `TimeEntry`, etc.).
- `main.py` – original console‑based version (kept for reference).
- `task_manager.py`, `time_tracker.py` – modules used by the console version.
- `.gitignore` – ensures `__pycache__` folders and bytecode files are not tracked.
- `LICENSE.md` – MIT License.

## Dependencies

- Python 3.13 or later
- [PySide6](https://pypi.org/project/PySide6/) – for the GUI
- [requests](https://pypi.org/project/requests/) – for API calls
- [numpy](https://pypi.org/project/numpy/) – used implicitly by pandas
- [pandas](https://pypi.org/project/pandas/) – for data aggregation in the report

Install all dependencies with:

```bash
pip install PySide6 requests numpy pandas

How to Run
GUI Version

Navigate to the TimeManager_GUI folder and run:
bash

python main.py

Console Version (original)

From the project root, run:
bash

python main.py

Usage Tips

    The task list displays each task with its time, duration (if set), and a checkbox.

    To see the weather, enter a city name, choose units, and click Get Weather.

    Click Show Report to open a window with total planned hours per project.

Notes

    The app uses the Open‑Meteo API (no API key required). It first geocodes the city name to coordinates, then fetches current weather.

    Tasks without a specified time appear at the bottom of the list.

    The report groups tasks by project and sums durations (converted to hours).

Acknowledgments

    Instructor: Poul Nichols

    Course: IT111 Programming Fundamentals

    Based on a class discussion: "Name something that could be useful in your daily life."

    AI Assistance: Some code refinements and this README were created with the help of DeepSeek, an AI assistant.

License

This project is licensed under the MIT License – see the LICENSE.md file for details.

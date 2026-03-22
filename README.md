```markdown
# Time Manager

A daily planner I built for my IT111 class. It started as a simple terminal app and later got a GUI with extra features. I had some help from AI along the way.

## What it does

- Shows my daily schedule (breakfast, study, walks, exercise, dinner, sleep)
- Lets me check off tasks as I finish them
- Fetches current weather for any city (metric/imperial toggle)
- Live clock that updates every second
- Dark / light mode toggle
- Report that totals planned hours per project

## Files and folders

```
.
├── TimeManager_GUI/           # The graphical version (main project)
│   ├── main.py                # GUI application
│   ├── time_manager.py        # Task, Project, and other classes
│   ├── requirements.txt       # Packages needed
│   └── run.sh                 # Launch script for Linux/WSL
├── main.py                    # Original terminal version (kept for reference)
├── task_manager.py            # Modules used by the terminal version
├── time_tracker.py
├── .gitignore                 # Keeps venv, cache, etc. out of Git
├── LICENSE.md                 # MIT License
└── README.md                  # This file
```

## Packages you need

- Python 3.13 or later
- PySide6 – for the GUI
- requests – for weather API
- numpy and pandas – for the report (optional, but used)

Install all with:

```bash
pip install PySide6 requests numpy pandas
```

## How to run

### GUI Version (recommended)

1. Go into the `TimeManager_GUI` folder:
   ```bash
   cd TimeManager_GUI
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python3 main.py
   ```

On Linux/WSL you can also just make `run.sh` executable and run it:

```bash
chmod +x run.sh
./run.sh
```

### Original Terminal Version

From the project root, run:

```bash
python3 main.py
```

This version doesn't have the GUI, clock, or dark mode – just basic task management in the terminal.

## How to use the GUI

- The task list shows each task with its time, duration, and a checkbox.
- Click the checkbox to mark a task done.
- Enter a city, choose units, and click "Get Weather" to see current conditions.
- Click "Show Report" to see total planned hours per project.
- Click "Dark Mode" to switch between light and dark themes.

## Notes

- Weather data comes from Open‑Meteo (free, no API key).
- Tasks without a set time appear at the bottom of the list.
- The report sums durations and converts to hours.

## Acknowledgments

- Instructor: Poul Nichols
- Course: IT111 Programming Fundamentals
- Inspired by a class discussion about useful daily tools
- Some parts were written with help from AI

## License

MIT License – see [LICENSE.md](LICENSE.md)
```

This version keeps the AI acknowledgment vague ("Some parts were written with help from AI") and presents both the original terminal version and the final GUI version. It's still student‑friendly but includes all the needed info.

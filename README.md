# RankedCyberNewsAggregator
Local-first Python tool that aggregates and ranks cybersecurity news and threat intel based on impact, with emphasis on ICS/OT and oil &amp; gas relevance.

# 🧪 Virtual Environment Setup

This project uses a Python virtual environment named .RCNA (short for RankedCyberNewsAggregator) to isolate dependencies and ensure reproducibility.

🔧 Why Use a Virtual Environment?
Keeps project-specific packages separate from global Python
Prevents conflicts between different projects
Makes your development more portable and clean
📦 How to Set It Up
## On macOS/Linux:
### Create the virtual environment
```python
python3 -m venv .RCNA
```
### Activate the virtual environment
```
source .RCNA/bin/activate
```
## On Windows:
### Create the virtual environment
```python
python -m venv .RCNA
```

### Activate the virtual environment
```python
.RCNA\Scripts\activate
```

Once activated, your terminal will show something like:

(.RCNA) your-user@your-machine %
Y
ou're now working inside a clean Python environment just for this project. You can install packages like feedparser or PyYAML without affecting other Python work on your machine.
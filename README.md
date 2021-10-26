# HipStrengthTesterGUI

Software for the DIY hip strength tester.

### How to run

Install requirements and package:
```bash
pip install -r requirements.txt
pip install .
```

Run module:
```bash
python -m hst
```

### How to build

Install build requirements:
```bash
pip install -r requirements-dev.txt
```

To create the exe run:
```bash
pyinstaller --name hst --paths=src\hst --windowed --onefile hst_gui.py
```
# HipStrengthTesterGUI
Software for the DIY hip strength tester.

### Build
Copy everything from hst/*.py in to hst.py so you don't need to
create a python package.

Currently working: Python3.6 and cx_Freeze==6.0

Run:
``` bash
python to_exe_setup.py build
```

This creates a new directory `build\exe.win32-3.6\` where you can find
the executable to run. There is bug in cx_Freeze==6.0 that is currently
resolved on their master but is not yet realest. That means you have
to manually copy `python3.dll` from the python directory to where
the exe is located for it to work.

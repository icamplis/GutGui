# GutGui

## Instructions

Go into the terminal,
navigate to this directory (GutGui),
and run the command

```python3 GutGui.py```

Note: `Select Data Superdirectory` refers to
the folder that contains all the other folders containing the data cubes.

Note: When multiple data cubes are selected,
the topmost one will be displayed.

<!--  TODO-->

## Development Notes
### Regarding Performance
For every folder uploaded, it's scanned for a data cube,
and that data cube is processed fully for all of the analysis patterns.
Similarly, for every change in mode (Normal vs Original, Masked vs. Whole, etc.),
every data cube will be updated accordingly.
Also, when switching between data cubes,
all the images will be re-rendered, which also takes time.

You can see the progress of the calculations in the logs.

**Currently, it's not advisable to run more than ~10 data cube directories at a time.**

If the program hangs or bugs out, press `Ctrl-C` in the console to shut it down.
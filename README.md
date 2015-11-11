# SC15-SVols-ICS
Generates an ics file for Student Volunteers from Linkings exported data. Go to submissions.supercomputing.org and log in. Click the "My Schedule" tab, and in the window that opens, click "My Shifts". Then, in the bottom right corner, click export, and choose tab delimited. Save this to a file. This will be the input to this script. The second parameter is the desired output file. This should have an .ics extension.

# Dependencies
pytz, ics

These can be installed with pip.

# Installing Dependencies on Linux
```bash
pip install --user pytz
pip install --user ics
```

# Installing Dependencies on Mac OS X
Install pip through either macports or homebrew: ```port install pip``` or ```brew install pip```

```bash
pip install pytz
pip install ics
```

# Installing Dependencies on Windows
Neither of the authors run Windows. If any of the other volunteers have instructions that work on Windows, open an issue or a pull request on GitHub and we will integrate them. In the meantime, this may be of help: [Windows Instructions](http://www.ubuntu.com/download/desktop/install-ubuntu-desktop)

# Usage
```bash 
python SVolICS.py --help
```

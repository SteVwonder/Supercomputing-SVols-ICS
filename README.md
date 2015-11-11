# SC15-SVols-ICS
Generates an ics file for Student Volunteers from Linkings exported data. Go to submissions.supercomputing.org and log in. Click the "My Schedule" tab, and in the window that opens, click "My Shifts". Then, in the bottom left corner, click export, and choose tab delimited. Save this to a file. This will be the input to this script. The second parameter is the desired output file. This should have an .ics extension.

# Dependencies
pytz, ics

These can be installed with pip.

# Installing Dependencies on Linux
pip install pytz
pip install ics

# Installing Dependencies on Mac OS X
Install pip through either macports or homebrew: port install pip | brew install pip
pip install pytz
pip install ics

# Installing Dependencies on Windows
See documentation here: [Windows Instructions](http://www.ubuntu.com/download/desktop/install-ubuntu-desktop)

# Usage
python SVolICS.py --help

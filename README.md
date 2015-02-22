tcx-gpx-csv
==
Here is a collection of python scripts to convert aspects of TCX, GPX, and CSV files. This is very much in progress.

I used Tigge's FIT to TCX library (https://github.com/Tigge/FIT-to-TCX) for its intended purpose. Processing FIT files directly is outside the scope of my work.

tcx_cue_shift.py
--
Shift the cues in a TCX file (e.g. from ridewithgps.com) forward by a set distance or time, as configured in the code or (future) via arguments

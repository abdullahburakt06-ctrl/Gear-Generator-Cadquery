*NOTE*: This was mostly a learning project. I am not a professional, and the code is likely to be prone to bugs.

This is a simple script designed to streamline the process of generating gears of helical and spur type without being dependent on CAD software extensions or add-ons.
The script uses the numpy library to define 10 points on the involute curve, 
which are then connected with a spline and a single gear tooth is produced. Afterwards a loop is utilized to complete the gear model.

Certain library conflicts regarding python-occ and cadquery had been an issue in the earliest stages. Properly install CadQuery to your python environment before using the script.

*TODO*: This project has not been thoroughly tested yet, and its export functionalities are still not added. There may be bugs and unexpected behavior within the script.


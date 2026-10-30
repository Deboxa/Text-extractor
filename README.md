Text Extractor

The program collects all text files from a specified folder into one large txt file. 
It is used to feed the entire project code to AI models in a single file.

Files:
extractor.py - main script.
RunExtractor.bat - Windows launcher.

How to run:
1. Run RunExtractor.bat (double click).
2. Enter the path to the project folder and press Enter. 
   (You can also just drag and drop the folder into the console window).
3. Wait for it to finish and press any key to close the window.

Or via console:
python extractor.py "D:\Path\To\Project"

Where it is saved:
In the results/YearMonthDay/ folder next to the script. 
The file name format is HHoursMMinutesSSeconds.txt

console log:
[+] - file added to the final txt.
[-] - file skipped.

skip reasons:
[tmp] - temporary file
[dir] - file inside a system folder (like .git, build)
[self] - the script itself or the output file
[bin] - binary file (image, archive, exe)
[size] - file is larger than 2 MB
[lines] - file has more than 1000 lines
[err] - read error or unknown encoding

Requirements:
Installed Python 3.
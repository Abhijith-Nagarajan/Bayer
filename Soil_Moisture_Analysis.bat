@echo off

rem Set the path to your Python executable
set pythonPath="C:\Users\abhij\AppData\Local\Programs\Python\Python311\python.exe"

rem Set the path to your VS Code executable
set codePath="C:\Users\abhij\AppData\Local\Programs\Microsoft VS Code\Code.exe"

rem Set the path to your Python file
set pythonFile="E:\Bayer\Soil_Moisture_Analysis_Test.py"

rem Use the "start" command to open VS Code with the Python file
set command=""%codePath%"" "%pythonFile%"
%command%




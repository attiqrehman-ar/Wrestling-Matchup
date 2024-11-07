# Wrestling Match-Up Program

## Overview
The **Wrestling Match-Up Program** is a Python application designed to assist in organizing wrestling match-ups based on wrestler attributes such as weight, age, and experience. The program imports wrestler data from CSV or Excel files, generates match-ups using two different systems (Fixed Weight Classes and Maddison System), and allows users to export the results to an Excel file. Additionally, it provides functionality to add notes, display them, and print the exported match-up data.

## Features
- **Data Import**: Import wrestler data from CSV or Excel files.
- **Match-Up Systems**: Generate match-ups based on:
  - Fixed Weight Classes
  - Maddison System
- **Export Data**: Export match-ups to an Excel file.
- **Notes**: Add and display notes for the session.
- **Print Exported Data**: Open a print dialog for printing match-up data.
- **Interactive GUI**: Easy-to-use interface built using Tkinter.

## Requirements
Before running the application, ensure that the following Python libraries are installed:
- `tkinter` (for GUI interface)
- `Pillow` (for image processing)
- `pywin32` (for printer functions on Windows)
- `pandas` (for data manipulation)
- `xlsxwriter` (for exporting data to Excel)

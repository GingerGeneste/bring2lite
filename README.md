# bring2lite
## About the original project
This code has been forked from [bring2lite](https://github.com/bring2lite/bring2lite) . Also see the published paper by the original author of this tool: [bring2lite: A Structural Concept and Tool for Forensic Data Analysis and Recovery of Deleted SQLite Records](https://www.sciencedirect.com/science/article/pii/S1742287619301677).

The tool was developed to process SQLite databases in respect of deleted records. Therefore, bring2lite is able to analyse the structures within the main database, WAL and journal files.

## About the modifications
My contributions are as follows (checked if already done): 
- [x] Removed the GUI as this is a lot of overhad
- [ ] Update the way log files are written (escape ',')
- [ ] Make the code a module

## Requirements
- Python3

## Licence
Licence is copied from the original author:
- CC-BY-NC

## Installation
1. Clone the repository
2. cd into the repository
3. ````python3 setup.py install````
## Usage

- **Process a single database main file:**
````bash
main.py --filename /path/to/file --out /path/to/output/folder
````

- **Process a single journal file:**
````bash
main.py --journal /path/to/journal/file --out /path/to/output/folder
````

- **Process a single WAL file:**
````bash
main.py --wal /path/to/wal/file --out /path/to/output/folder
````

- **Process a single database main file:**
````bash
main.py --filename /path/to/database/file --out /path/to/output/folder
````

- **Process all files within a single folder and all sub-folders:**
````bash
main.py --folder /path/to/folder --out /path/to/output/folder
````



## Used libraries
- [tqdm](https://github.com/tqdm/tqdm) - a library which can be used to created progress bars
- [sqlparse](https://github.com/andialbrecht/sqlparse) - this library allows to easily process SQLite statements

## Changelog
- 14-03-2019 - publication of version 0.1 by original author
- 07-04-2022 - Forked project from [bring2lite](https://github.com/bring2lite/bring2lite)


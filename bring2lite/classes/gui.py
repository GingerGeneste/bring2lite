#print a console help
import argparse
#logging all events in the gui class
import logging
#system
import sys
import os
from pathlib import Path
#statusbar

from tqdm import tqdm
#own classes
from .sqlite_parser import SQLiteParser
from .WAL_parser import WALParser
from .journal_parser import JournalParser

class GUI:
    def __init__(self):
        self.logger = logging.getLogger("parser.gui")
        self.sqlites = []
        self.sqlp = None
        self.wals = []
        self.walp = None
        self.journals = []
        self.journalp = None
        self.output = None
        self.format = 0
        argparser = argparse.ArgumentParser(description='Parsing a folder with a whole bunch of SQLite databases in it '
                                                        'or just a single databases, WAL files or journal files', add_help=True)
        argparser.add_argument("--folder", default="", help='path to the location where the SQLite databases '
                                                                    'are stored', nargs='*')
        argparser.add_argument("--filename", default="", help='path(s) to the SQLite database file(s)', nargs='*')
        argparser.add_argument("--wal", default="", help='path(s) to the WAL file(s)', nargs='*')
        argparser.add_argument("--journal", default="", help='name of the SQLite database file', nargs='*')
        argparser.add_argument("--out", help='where you want to place the results of this process', nargs='?')
        argparser.add_argument("--format", default="CSV", help='output format XML, JSON, CSV - defualt: CSV', nargs='?')
        args = argparser.parse_args()
        if len(sys.argv) == 1:
            argparser.print_help()
            exit()

        for f in args.folder:
            if os.path.exists(os.path.abspath(f)) and len(f) > 0:
                for subdir, dirs, files in os.walk(os.path.abspath(f)):
                    for file in files:
                        filepath = subdir + os.sep + file
                        if filepath.endswith(".sqlite") or filepath.endswith(".db"):
                            self.sqlites.append(filepath)
                        elif filepath.endswith("-wal"):
                            self.wals.append(filepath)
                        elif filepath.endswith("-journal"):
                            self.journals.append(filepath)

        for f in args.filename:
            if (Path(os.path.abspath(f))).is_file():
                self.sqlites.append(os.path.abspath(f))

        for f in args.wal:
            if (Path(os.path.abspath(f))).is_file():
                self.wals.append(os.path.abspath(f))

        for f in args.journal:
            if (Path(os.path.abspath(f))).is_file():
                self.journals.append(os.path.abspath(f))

        if not (len(self.sqlites) > 0 or len(self.wals) > 0 or len(self.journals) > 0):
            exit("No files to parse")

        if os.path.exists(os.path.abspath(args.out)):
            self.output = os.path.abspath(args.out)
        else:
            os.makedirs(os.path.abspath(args.out))
            self.output = os.path.abspath(args.out)

        #CSV = 0 | XML = 1 | JSON = 2
        if args.format is 'XML':
            self.format = 1
        elif args.format is 'JSON':
            self.format = 2

    def process(self):
        self.start_processing_sqlite()
        self.start_processing_journal()
        self.start_processing_wal()

    def start_processing_sqlite(self):
        self.d = None
        if len(self.sqlites) > 0:
            tqdm.write("Processing main files")
            self.sqlp = SQLiteParser()
            for i in tqdm(self.sqlites):
                self.d = self.sqlp.parse(i, self.output, self.format)

        self.logger.debug("end of parsing")

    def start_processing_wal(self):
        if len(self.wals) > 0:
            tqdm.write("Processing WAL files")
            self.walp = WALParser()

            for i in tqdm(self.wals):
                if i[0:-4] in self.sqlites:
                    self.walp.parse(i, self.output, self.format, True)
                else:
                    self.walp.parse(i, self.output, self.format, False)

    def start_processing_journal(self):
        if len(self.journals) > 0:
            tqdm.write("Processing journal files")
            self.sqlp = SQLiteParser()
            self.journalp = JournalParser()
            for i in tqdm(self.journals):
                try:
                    if i[0:-8] in self.sqlites:
                        self.journalp.parse(i, self.output, self.format, self.sqlp.get_page_size(i[0:-8]))
                    else:
                        self.journalp.parse(i, self.output, self.format, 0)
                        #exit("No related sqlite file with this journal " + i)
                except ValueError:
                    print("No page size are available")

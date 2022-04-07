import os
import hashlib
import csv
from tqdm import tqdm


class ReportGenerator:
    def __init__(self):
        self.my_path = ""

    def generateReport(self, path, filename, data, schema=["No schema found"]):
        """
        Alternate results writer, using a CSV module to avoid not escaping comma's e.d.
        :param path: path to directory to write the log files to
        :param filename: name of the logfile (without .log postfix)
        :param data: a list of lists containing carved records
        :param schema: possibly found a database schema to be added on top of the log file
        :return: None
        """
        if data is None:
            return

        if not os.path.exists(path):
            os.makedirs(path)

        # Iterator to create CSV from
        out = []
        # If a schema is found, add the column types to the top of the log file:
        out.append(schema)
        # A 'frame' is actually a possible carved record
        # Represented as a list where each element is a list containing the type of
        # column value and the column value itself
        for frame in data:
            csv_row = []
            if isinstance(frame, list):
                for column in frame:
                    # If the carved record column is of type 'TEXT' try to decode it
                    if self.is_text(column[0]):
                        try:
                            csv_row.append(column[1].decode('utf-8'))
                        except UnicodeDecodeError:
                            csv_row.append(column[1])
                    # Otherwise just add the value as it is:
                    else:
                        csv_row.append(column[1])
            out.append(csv_row)

        # Write results
        self.write_to_file(filename, path, out)

    def write_to_file(self, filename, path, out):
        file_out = f'{path}/test_{filename}.log'
        if os.path.exists(file_out):
            tqdm.write(f"Logfile {filename} already exists! Overwriting the results.")
        try:
            with open(file_out, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerows(out)

        except UnicodeEncodeError:
            tqdm.write("can not write the record because of unicode errors")

        self.print_hash(file_out)

    def generate_schema_report(self, path, filename, data, csv):
        if data is None:
            return

        if not os.path.exists(path):
            os.makedirs(path)

        out = ""
        with open(path + "/" + filename + '.log', "a") as f:
            for key, value in data.items():
                # out += str(key) + ", "
                if isinstance(value, list):
                    for y in value:
                        out += str(y) + ", "
                out += "\n"
            out += "++++++++++++++++++++++++++++\n"

            f.write(out)

        self.print_hash(path + "/" + filename + '.log')

    def generate_freeblock_report(self, path, filename, freeblocks):
        if freeblocks is None:
            return

        if not os.path.exists(path):
            os.makedirs(path)

        with open(path + "/" + filename + '.log', "a") as f:
            for solutions in freeblocks:
                for s in solutions:
                    if isinstance(s[0], list):
                        f.write(str(s) + ",")
                    else:
                        if self.is_text(s[0]):
                            f.write(str(s[1].decode('utf-8')) + ",")
                        else:
                            f.write(str(s[1]) + ",")
                f.write("\n" + "###################" + "\n")

        self.print_hash(path + "/" + filename + '.log')

    def is_text(self, tester):
        return tester == 'TEXT'

    def print_hash(self, filename):
        with open(filename, "rb") as f:
            d = f.read()
            tqdm.write("sha-256: " + filename + '\t => \t' + str(hashlib.sha256(d).hexdigest()))

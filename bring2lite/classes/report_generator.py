import os
import hashlib
import csv
from tqdm import tqdm

class ReportGenerator:
    def __init__(self):
        self.my_path = ""

    def generateCSV(self, path, filename, data, schema=["No schema found"]):
        """
        Alternate results writer, using a CSV module to avoid not escaping comma's e.d.
        :param path: path to directory to write the log files to
        :param filename: name of the logfile (without .log postfix)
        :param data:
        :param schema:
        :return:
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
                    # If the carved record column is of type 'text' try to decode it
                    if column[0] == 'TEXT':
                        try:
                            csv_row.append(column[1].decode('utf-8'))
                        except UnicodeDecodeError:
                            csv_row.append(column[1])
                    # Otherwise just add the value as it is:
                    else:
                        csv_row.append(column[1])
            out.append(csv_row)

        # Write results
        try:
            with open(f'{path}/test_{filename}.log', 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerows(out)

        except UnicodeEncodeError:
            tqdm.write("can not write the record because of unicode errors")
        return out


    def generateReport(self, path, filename, data, format="CSV", schema=["No schema found"]):
        if data is None:
            return

        if not os.path.exists(path):
            os.makedirs(path)

        out = ""
        for datatype in schema:
            out += str(datatype) + ","
        out += "\n"
        test = self.generateCSV(path, filename, data, schema)

        for frame in data:
            if isinstance(frame, list):
                for y in frame:
                    if self.is_text(y[0]):
                        try:
                            out += str(y[1].decode('utf-8')) + ","
                        except UnicodeDecodeError:
                            out +=str(y[1]) + ","
                            continue
                    else:
                        out += str(y[1]) + ","
            out += "\n"
        out += "++++++++++++++++++++++++++++\n"
        try:
            with open(path + "/" + filename + '.log', "a") as f:
                f.write(out)
        except UnicodeEncodeError:
            tqdm.write("can not write the record because of unicode errors")

        self.print_hash(path + "/" + filename + '.log')

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
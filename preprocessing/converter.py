import os


def convertNASSCropDataToCsv(file_name_in: str, file_name_out: str):
    pass


def genCreateTableCommand(file_path_in: str) -> str:
    command = "CREATE TABLE crop_data ("
    with open(file_path_in) as fin:
        first_line = fin.readline().strip('\n')
    first_line = first_line.split('\t')
    for line in first_line:
        command += '"' + line + '"' + " varchar, "
    command = command[:len(command) - 2]  # remove extra ", "
    command += ");"
    return command


if __name__ == "__main__":
    file_name = "qs_crops_20240203.txt"
    file_path_in = os.getcwd().replace("preprocessing", "data") + "\\" + file_name
    print(genCreateTableCommand(file_path_in))
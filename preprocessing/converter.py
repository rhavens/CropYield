import os


def preprocess_crop_file(file_path, file_name):
    chunksize = 16384
    count = 0
    with open(file_path + file_name, 'rb') as data_reader:
        while True:
            count += 1
            if count % 10000 == 0:
                print(str(count * chunksize / 1000000) + "MB processed")

            chunk = data_reader.read(chunksize)
            if len(chunk) == 0:
                return

            chunk = chunk.replace(b'\00', b'')  # the null characters in the input cause issues in postgres
            with open(file_path + file_name + "_nullremoved", 'ab') as fout:
                fout.write(chunk)


def gen_create_table_command(file_path: str, file_name: str) -> str:
    command = "CREATE TABLE crop_data ("
    with open(file_path + file_name) as fin:
        first_line = fin.readline().strip('\n')
        second_line = fin.readline().strip('\n')
    for line in first_line:
        command += '"' + line + '"' + " varchar, "
    command = command[:len(command) - 2]  # remove extra ", "
    command += ");"
    return command


if __name__ == "__main__":
    file_name = "qs.crops_20240203.txt"
    file_path = os.getcwd().replace("preprocessing", "data") + "\\"
    preprocess_crop_file(file_path, file_name)

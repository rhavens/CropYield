import os


def preprocess_crop_file(file_path: str, file_name: str) -> None:
    chunk_size = 16384
    count = 0
    outfile_name = file_name + "_preprocessed"
    if os.path.exists(file_path + outfile_name):
        os.remove(file_path + outfile_name)

    with open(file_path + file_name, 'rb') as data_reader:
        while True:
            count += 1
            if count % 10000 == 0:
                print(str(count * chunk_size / 1000000) + "MB processed")

            chunk = data_reader.read(chunk_size)
            if len(chunk) == 0:
                print("Finished preprocessing")
                return

            chunk = chunk.replace(b'\00', b'')  # the null characters in the input cause issues in postgres
            with open(file_path + outfile_name, 'ab') as fout:
                fout.write(chunk)


def gen_create_table_command(file_path: str, file_name: str) -> None:
    command = "CREATE TABLE crop_data ("
    with open(file_path + file_name) as fin:
        first_line = fin.readline().strip('\n')
    for line in first_line:
        command += '"' + line + '"' + " varchar, "
    command = command[:len(command) - 2]  # remove extra ", "
    command += ");"
    print(command)


"""
TO USE:
Place the qscrop file in the /data folder
Set "file_name" to the name of the qs crop file
The output will be a new file named "<filename>_preprocessed" in the /data folder
"""
if __name__ == "__main__":
    file_name = "qs.crops_20240203.txt"
    file_path = os.getcwd().replace("preprocessing", "") + os.path.sep + "data" + os.path.sep
    preprocess_crop_file(file_path, file_name)

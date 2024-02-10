import os


def preprocess_crop_file(file_path: str, file_name: str) -> None:
    chunk_size = 16384
    count = 0
    outfile_name = file_name + "_preprocessed"

    # new file is written to using append mode, so must delete the new file if it already exists
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


def gen_select_into_command():
    columns_to_keep = [
        "SOURCE_DESC",
        "SECTOR_DESC",
        "GROUP_DESC",
        "COMMODITY_DESC",
        "PRODN_PRACTICE_DESC",
        "UTIL_PRACTICE_DESC",
        "STATISTICCAT_DESC",
        "UNIT_DESC",
        "SHORT_DESC",
        "DOMAIN_DESC",
        "DOMAINCAT_DESC",
        "AGG_LEVEL_DESC",
        "STATE_ANSI",
        "STATE_FIPS_CODE",
        "STATE_ALPHA",
        "STATE_NAME",
        "ASD_CODE",
        "ASD_DESC",
        "COUNTY_ANSI",
        "COUNTY_CODE",
        "COUNTY_NAME",
        "LOCATION_DESC",
        "YEAR",
        "FREQ_DESC",
        "REFERENCE_PERIOD_DESC",
        "VALUE"
    ]
    command = "SELECT "
    for column in columns_to_keep:
        command += '"' + column + '", '
    command = command[:len(command) - 2]  # remove extra ", "
    command += " INTO crop_data_pruned FROM public.crop_data;"
    print(command)


def gen_create_table_command(file_path: str, file_name: str) -> None:
    command = "CREATE TABLE crop_data ("
    with open(file_path + file_name) as fin:
        first_line = fin.readline().strip('\n')
    first_line = first_line.split('\t')
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
    # preprocess_crop_file(file_path, file_name)
    # gen_create_table_command(file_path, file_name)
    # gen_select_into_command()

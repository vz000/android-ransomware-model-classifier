import os
import csv

class parse_static_data:
    def __init__(self, apk_path: str) -> None:
        self.apk_path = apk_path
        self.apk_tags = []
        self.__get_data_from_apk__()
        self.__parse_permissions__()

    def __get_data_from_apk__(self) -> None:
        print("Analyzing package...")
        out_dir_names = ["./out","./out/static/"]
        if not os.path.isdir(out_dir_names[1]):
            for dir_names in out_dir_names:
                os.mkdir(dir_names)
        
        if ".apk" in self.apk_path:
            os.system("aapt dump permissions " + self.apk_path + " > " + out_dir_names[1] +"/aapt_output.txt")

    def __parse_permissions__(self) -> None:
        with open('./out/static/aapt_output.txt',"r", newline='') as out:
            apk_permissions = []
            apk_name = []
            for data in out:
                if "package" in data:
                    try:
                        apk_name.append(data.rstrip().split(' ')[1])
                    except:
                        apk_name.append("")
                if "uses-permission:" in data or "permission:" in data:
                    try:
                        permission = data.split(" ")[1].split("=")[1][1:-3].split(".")[-1]
                        apk_permissions.append(permission)
                    except:
                        permission = apk_permissions.append("")
            file_name = "./out/permissions.csv"
            apk_permissions.append(apk_name[0])
            with open(file_name, 'w+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(apk_permissions)

class parse_dynamic_data:
    def __init__(self) -> None:
        self.parsed = []
        self.file_names = []
        self.__parse_logs__()

    def __parse_logs__(self) -> None:
        folderName = "./"
        fileList = os.listdir(folderName)
        for dataFile in fileList:
            if "logs.txt" in dataFile:
                fileName = folderName + dataFile
                with open(fileName) as file:
                    line = file.readlines()
                    log = []
                    cropCalls = line[:3000]
                    for call in cropCalls:
                        parseLine = call.split("(") # get only the call name. Returns a list of the calls
                        log.append(parseLine[0])
                    self.parsed.append(log)
    def parsed_logs(self) -> list:
        return self.parsed

def parse_freq_data(data_type : str) -> list:
    parsed_values = []
    with open('./model/syscalls-freq-'+data_type+'.csv',"r") as freq:
        for row in freq:
            calls = []
            get_values = [row.split('"')[1],row.split('"')[3]]
            sequence = get_values[0][1:-1].split(",")
            freq_range = [int(f) for f in get_values[1][1:-1].split(",")]
            calls.append(sequence[0][1:-1])
            for i in range(1, len(sequence)):
                calls.append(sequence[i][2:-1])
            parsed_values.append([calls,freq_range])
    return parsed_values
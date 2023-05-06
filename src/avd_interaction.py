import os
import sys
from threading import Thread

def start_strace(pid, file_logs):
    os.system('adb shell "timeout 10 strace -p ' + str(pid) + ' -o '+ file_logs + '"')

apkLocation = sys.argv[1] # equals sample_name
os.system('aapt dump badging ' + apkLocation +' > aapt_output.txt')
get_line = open('aapt_output.txt','r',encoding="utf8")
first_line = get_line.readlines()[0] # processing that doesn't fit rust.
pkg_name = first_line.split(' ')[1].split('=')[1].strip("'")

try:
    os.system("adb shell monkey -p " + pkg_name + " 1")
    os.system('adb shell "ps -e | grep ' + pkg_name + '" > pid.txt')
    get_line = open("pid.txt",'r',encoding="utf8")
    first_line = get_line.readlines()[0] # processing that doesn't fit rust.
    process_output = first_line.split(' ')
    pid = [x for x in process_output if x != '']
    file_name = '/data/app/logs.txt'
    ex_strace = Thread(target=start_strace, args=(pid[1], file_name)) # launch strace
    ex_strace.start()
    os.system("adb shell monkey -p " + pkg_name + " --throttle 200 --pct-touch 100 50")
    ex_strace.join() # Waits for strace to finish.
    os.system("adb pull "+file_name)

except Exception as e:
    print(e)

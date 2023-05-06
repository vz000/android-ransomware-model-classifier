from main import launch
import sys
import os

result = []

try:
    apk_path = sys.argv[1] # Example: ./packages/Wuhan_b673844f96518d87407d0793e4c7abf3.apk
    apk_list = os.listdir(apk_path)
    for apk in apk_list:
        result.append(launch(apk_path+apk))
    print("\n\nRESULT: ")
    print(result)

except IndexError:
    print("A path for the apk to be analyzed must be provided.")
    sys.exit(1)
except FileNotFoundError:
    print("File does not exist.")
except Exception as e:
    print("Unhandled exception: ", e)
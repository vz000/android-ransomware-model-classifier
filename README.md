# Ransomware detection model
This model helps to identify ransomware applications for Android.
This is the trained version and includes the files needed to classify .apk samples.

## How to use
1. Rust (version >= 1.68) and Python (version >= 3.9) must be installed.
2. Create a virtual environment:
   ```
   pip install virtualenv
   python -m venv <virtual-env-name>
   ./<virtual-env-name>/Scripts/activate
   ```
3. Install maturin to run Rust.
```
pip install maturin
```
4. Build the crate and install it as a python module in the current virtualenv:
```
maturin develop
```
5. Create a folder with the name `files` INSIDE THE ROOT DIRECTORY. And add files as needed, with different extensions, such as .png, .jpeg, .txt.
6. Run the script:
```
python ./model/model.py <path_to_folder_with_apk_files>
```
It is recommended to place the folder at the same level as `files`.

For more details about dynamic data extraction, see: [automated-execution](https://github.com/vz000/automated-execution)

## Notes
* Data, such as applications and system call logs, is not provided.

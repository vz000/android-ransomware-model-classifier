use std::process::{Command, Stdio};
use std::thread;
use std::time::Duration;
use std::fs;
use pyo3::wrap_pyfunction;
use pyo3::prelude::*;

// GLOBAL VARIABLES
const FILES_PATH: &str = "storage/self/primary/Download/";

fn get_avd_name() -> String {
    let emulator = Command::new("./Android/Sdk/emulator/emulator").arg("-list-avds").stdout(Stdio::piped())
    .output().expect("\'emulator\' was not found.");
    let avd_name = String::from_utf8_lossy(&emulator.stdout).to_string();
    avd_name.trim().to_string()
}

fn launch_device(emulator_output: String) -> String {
    let avd = if emulator_output.is_empty() {
        println!("An AVD image must be created first."); // Cannot resolve to create avds with avdmanager: Batch script of Windows and .sh for Linux.
        "".to_string()
    } else {
        let avd_name = format!("{}",emulator_output.trim());
        let avd_name_out = emulator_output.trim().clone();
        Command::new("./Android/Sdk/emulator/emulator").arg("-avd").arg(avd_name).arg("-wipe-data").spawn().unwrap();
        thread::sleep(Duration::from_secs(50)); // This time may vary depending on the computer specs.
        avd_name_out.to_string()
    };
    avd
}

fn add_files() {
    // Keep it simple. Files are pushed to ../Download/.
    let files =  fs::read_dir("./files/").unwrap();

    for file in files {
        let push_file = file.unwrap().path().display().to_string();
        Command::new("adb").arg("push").arg(push_file).arg(FILES_PATH).spawn().unwrap();
    }
}

#[pyfunction]
fn start_analysis(apk_path_name: String) {
    launch_device(get_avd_name());

    Command::new("adb").arg("root").spawn().unwrap(); // Start as root
    thread::sleep(Duration::from_secs(5));

    add_files();
    let apk_path = apk_path_name.clone();
    println!("Package {} to be installed.", apk_path_name);
    Command::new("adb").arg("install").arg(apk_path).spawn().unwrap();
    thread::sleep(Duration::from_secs(1)); // Give 5 seconds for app to be installed.
    execute_apk(apk_path_name);
    Command::new("adb").arg("emu").arg("kill").spawn().unwrap();
    thread::sleep(Duration::from_secs(10));
}

fn execute_apk(apk_path: String) {
    let _py_call = Command::new("python").arg("src/avd_interaction.py").arg(apk_path)
            .stdout(Stdio::piped()).output();
}

#[pymodule]
fn rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(start_analysis, m)?)?;
    Ok(())
}
# Automation & Scripting - Mandatory Assignment 2

## Introduction
You have been given the assignment to create a Windows service. You must choose one
service to create, from several different options.

Your service must be written in PowerShell.

The service should have complete functionality, with options for starting and stopping
using **_WinSW_** , **_NSSM_** or **_Task Scheduler_** (although this method is considered low effort).

The service should be logging relevant details about its operations to the appropriate
system logging directory.


## Options
1. **Simple backup/sync script:**
    Periodically copies files from a source folder to a backup folder.
    Only copies changed files (compare timestamps or sizes).
    Logs number of files copied, skipped, and any errors.  
2. **Wallpaper rotator service:**
    A background service that periodically changes the user’s desktop wallpaper. It
    selects a random image from a specified folder and applies it at a fixed interval. The
    service logs each wallpaper change and any errors (e.g., missing files).
3. **Clipboard logger (“malware”-like behavior):**
    A monitoring service that checks the clipboard every few seconds. If the clipboard
    content has changed since the last check, it logs the new content to a log file.
4. **“Paranoid Canary File” Tamper Detector:**
    A background service that watches a special “canary file” in the user’s folder.
    If the file is modified, deleted, or copied elsewhere, the service logs the event and
    silently restores the original file from a backup.
5. **Custom:**
    Pitch your idea and we might accept it!


## Requirements
- **Robustness:**  
    Your service must be able to recover from a crash.
- **Logging:**  
    Your service should output relevant logging details with timestamps, in case of a
    crash, restart, startup, or warnings during runtime.
- **Programming language:**  
    Your service must be written in PowerShell.


## Deliverables
- A .zip file containing:
    - The source code for your service
    - A script or readme.txt detailing installation
    - Any extra config files necessary
    - An example logfile from the output of your service
- A short report and summary about what your service does and how it works, preferably with some screenshots. **Maximum 5 pages**.


## Using Task Scheduler (Easiest)
1. Open the “Task Scheduler” program in Windows
2. On the right hand side, click “Create Task”
3. Name your service and configure the appropriate settings for each of the 5 tabs:  
    a. General, Triggers, Actions, Conditions, Settings


## Using WinSW (Realist)

### Installing WinSW
1. Go to https://github.com/winsw/winsw/releases and download latest version  
    a. “WinSW-x 64.exe” for 64-bit and “WinSW-x86.exe” for 32-bit
2. Place it next to your script
3. Rename it to something meaningful, fx. “MyService.exe”

### Usage
1. Create an XML file with the same name as the .exe (in this case “MyService.xml”)  
    a. You can find an example XML on itsLearning (you will have to change it!)
2. Place the XML file next to the .exe
3. Open an Administrator PowerShell terminal
4. Run: “MyService.exe install”
5. Run: “MyService.exe start”


## Using NSSM (Jankiest)

### Installing NSSM
1. Go to https://nssm.cc/download and download the latest stable version.
2. Unzip it and extract correct version (32-bit or 64-bit) depending on your system.
3. Place “nssm.exe” next to your script.  
    a. (Advanced) Alternatively place it in a tools folder and add it to your PATH

### Using NSSM
1. Open an Administrator PoweShell terminal
2. Using GUI  
    a. Run “nssm.exe install”  
    b. Enter service name, path to PowerShell and arguments to PowerShell  
    c. Run “nssm.exe start”
3. Using CLI  
    a. You can find an example install script on itsLearning (you have to change it!)

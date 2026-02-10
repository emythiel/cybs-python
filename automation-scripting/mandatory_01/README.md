# Automation & Scripting - Mandatory Assignment 1

## Introduction
You have been given the assignment to create a Linux service. You must choose one service to create, from several different options. You must also choose which programming language you will be using to create the service.

The service should have complete functionality, with options for starting and stopping using `systemd` or similar.

The service should be logging relevant details about its operations to the appropriate system logging directory.

## Options
1. **Housekeeping service:**
A service to monitor CPU usage, memory usage, disk space and network activity (speed), and output warnings in a log file.

2. **Weather service:**
A service to check the weather at a certain interval for a user-defined location and put the results in a log file or in the terminal.

3. **A log maintenance service:**
Monitor and check logs in a specified directory, compress them if they get too large, and clean them up if they get too old.

4. **Security service:**
Check relevant system logs for intrusion and login attempts to the system, as well as malicious commands.

5. **ADVANCED:**
Make a webserver without using any http libraries - raw text only.

6. **Custom:**
Pitch your idea and it might be accepted!

## Requirements
- **Robustness:**
Your service must be able to recover from a crash, start on its own when the system is started.

- **Logging:**
Your service should output relevant logging details with timestamps, in case of a crash, restart, startup, or warnings during runtime.

- **Unit file:**
The service should have a unit file with configuration and relevant variables depending on the service of your choice.

- **Programming language:**
You must choose Bash or Python for your service.

## Deliverables
- A .zip file containing:
  - Source code for the service
  - Unit file for the service
  - Example logfile from the output of the service
- A short report and summary about what your service does and how it works, preferably with some screenshots. **Maximum 5 pages.**

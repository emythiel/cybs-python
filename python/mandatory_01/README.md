# Mandatory 1 - Cybersecurity 1. Semester

### Introduction
Oh no! Our company "SECO" had an incident, and we are not mature enough to sort through the alerts! We need your help. Luckily, we use the standard Microsoft alert format that comes in JSON, that you already know!

We want you to sort through the alert and help us get specific data about what happened.

Finally, we want you to give us a specific formatted output, because the tools we are currently using does not support JSON. We expect you to make a program that can follow our specified requirements, as well as a presentation for the board to show your results. Please see the detailed requirements in the description below.

### Description
We will provide you with an incident file. This file is named “**incident.json**”.

The file contains multiple alerts for an incident, and detailed metadata about the alerts such as IP addresses and domain names.

Your task in this assignment is to create a program that can parse the JSON incident file and export several CSV files per our requirements.CSV is short for Comma Separated Values.

### Program requirements
- Your program must parse the JSON incident file so that you can work with it as a JSON object in Python
- Some alerts have multiple values for a field, your program must therefore output **4** different CSV files, each with a focus on different data as part of the alerts.
    - CSV File 1 headers: `alertId`, `machineId`, `firstActivity`, `domains`
    - CSV File 2 headers: `alertId`, `machineId`, `firstActivity`, `fileHashes`
    - CSV File 3 headers: `alertId`, `machineId`, `firstActivity`, `ips`
    - CSV File 4 headers: `alertId`, `machineId`, `firstActivity`, `processes`
We expect quotations ("") surrounding each header as well as value.  
We expect headers and values separated by commans (,).

To help you get started, we have included an example output csv file for "CSV File 3":
```
"alertId","machineId","firstActivity","ips"
"ALT1000-0","machine-76","2025-08-25T08:05:11.385954+00:00","185.220.100.240"
"ALT1000-0","machine-76","2025-08-25T08:05:11.385954+00:00","13.107.42.14"
"ALT1000-1","machine-100","2025-08-25T08:04:11.385954+00:00","192.168.1.100"
"ALT1000-1","machine-100","2025-08-25T08:04:11.385954+00:00","91.189.88.142"
"ALT1000-1","machine-100","2025-08-25T08:04:11.385954+00:00","172.16.5.23"
"ALT1000-2","machine-12","2025-08-25T07:56:11.385954+00:00","13.107.42.14"
"ALT1000-3","machine-34","2025-08-25T08:42:11.385954+00:00","10.0.0.15"
"ALT1000-3","machine-34","2025-08-25T08:42:11.385954+00:00","192.168.1.100"
"ALT1000-3","machine-34","2025-08-25T08:42:11.385954+00:00","172.16.5.23"
```
As you can see, the same alert has **multiple IP addresses**, which is why we expect you to keep track of the alert ID and machine ID for each file.

It is very important that you follow our specifications exactly for the CSV output, as we otherwise cannot process it in our alert database. You should familiarizeyourself with the CSV standard which can be found here: https://datatracker.ietf.org/doc/html/rfc4180.

### Modules
Python modules required to complete the project are "**json**" and "**csv**". You are allowed to use other modules that you might be familiar with.

### Requirements for deliverable
The project should be completed in groups.

Handing in th eproject is a requirement to attend the exam.

Handing in will be done through **itsLearning**, where you will also be able to register your groups. The deliverable will be a **.zip** file containing the following:

1. Source code for the program following the specifications as described above
2. Output of four CSV files, following the specifications as described above
3. A presentation of about **10 minutes** to be presented as part of the project, the presentation could be about one or several of the following topics:
    a. Showing the source code and explaining the choices you made
    b. A short demo of your program in action
    c. Challenges you had to solve as part of your project
    d. Ideas on how to improve your program in the future

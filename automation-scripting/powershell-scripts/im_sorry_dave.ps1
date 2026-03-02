# I'm Sorry Dave
# Write a script that allows users to create files and write to them
#
# - Take filename as user input (Read-Host)
# - Get the path to the current directory (Get-Location + Join-Path)
# - Try to create file with the given filename (New-Item + ErrorAction)
# - Handle thrown exception if already exists and display as warning
# - Take user input that will be written to the file (Read-Host)
# - Throw exception if the contents contain "open" *and* "door"
# - The program must run continuously until exited (While)
# - The program should exit if the filename given is "exit" or "quit"

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

function helloDave {
    param (
        [ConsoleColor]$fgColor = "White",
        [ConsoleColor]$bgColor = "Black"
    )
    Write-Host "                                                 " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "    __  __     ____         ____                 " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "   / / / /__  / / /___     / __ \____ __   _____ " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "  / /_/ / _ \/ / / __ \   / / / / __ \/ | / / _ \" -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host " / __  /  __/ / / /_/ /  / /_/ / /_/ /| |/ /  __/" -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "/_/ /_/\___/_/_/\____/  /_____/\__,_/ |___/\___/ " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "                                                 " -ForegroundColor $fgColor -BackgroundColor $bgColor
}

function goodbyeDave {
    param (
        [ConsoleColor]$fgColor = "White",
        [ConsoleColor]$bgColor = "Black"
    )
    Write-Host "                                                                    " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "   ______                ____                  ____                 " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "  / ____/___  ____  ____/ / /_  __  _____     / __ \____ __   _____ " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host " / / __/ __ \/ __ \/ __  / __ \/ / / / _ \   / / / / __ \/ | / / _ \" -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "/ /_/ / /_/ / /_/ / /_/ / /_/ / /_/ /  __/  / /_/ / /_/ /| |/ /  __/" -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "\____/\____/\____/\__,_/_.___/\__, /\___/  /_____/\__,_/ |___/\___/ " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "                             /____/                                 " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "                                                                    " -ForegroundColor $fgColor -BackgroundColor $bgColor
}

function imSorryDave {
    param (
        [ConsoleColor]$fgColor = "White",
        [ConsoleColor]$bgColor = "Black"
    )
    Write-Host "                                                                                                        " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host " ██▓ ███▄ ▄███▓     ██████  ▒█████   ██▀███   ██▀███ ▓██   ██▓   ▓█████▄  ▄▄▄    ██▒   █▓▓█████         " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "▓██▒▓██▒▀█▀ ██▒   ▒██    ▒ ▒██▒  ██▒▓██ ▒ ██▒▓██ ▒ ██▒▒██  ██▒   ▒██▀ ██▌▒████▄ ▓██░   █▒▓█   ▀         " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "▒██▒▓██    ▓██░   ░ ▓██▄   ▒██░  ██▒▓██ ░▄█ ▒▓██ ░▄█ ▒ ▒██ ██░   ░██   █▌▒██  ▀█▄▓██  █▒░▒███           " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "░██░▒██    ▒██      ▒   ██▒▒██   ██░▒██▀▀█▄  ▒██▀▀█▄   ░ ▐██▓░   ░▓█▄   ▌░██▄▄▄▄██▒██ █░░▒▓█  ▄         " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "░██░▒██▒   ░██▒   ▒██████▒▒░ ████▓▒░░██▓ ▒██▒░██▓ ▒██▒ ░ ██▒▓░   ░▒████▓  ▓█   ▓██▒▒▀█░  ░▒████▒        " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "░▓  ░ ▒░   ░  ░   ▒ ▒▓▒ ▒ ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░ ▒▓ ░▒▓░  ██▒▒▒     ▒▒▓  ▒  ▒▒   ▓▒█░░ ▐░  ░░ ▒░ ░        " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host " ▒ ░░  ░      ░   ░ ░▒  ░ ░  ░ ▒ ▒░   ░▒ ░ ▒░  ░▒ ░ ▒░▓██ ░▒░     ░ ▒  ▒   ▒   ▒▒ ░░ ░░   ░ ░  ░        " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host " ▒ ░░      ░      ░  ░  ░  ░ ░ ░ ▒    ░░   ░   ░░   ░ ▒ ▒ ░░      ░ ░  ░   ░   ▒     ░░     ░           " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host " ░         ░            ░      ░ ░     ░        ░     ░ ░           ░          ░  ░   ░     ░  ░        " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "                                                      ░ ░         ░                  ░                  " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host " ██▓    ▄████▄   ▄▄▄       ███▄    █ ▄▄▄█████▓   ▓█████▄  ▒█████     ▄▄▄█████▓ ██░ ██  ▄▄▄     ▄▄▄█████▓" -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "▓██▒   ▒██▀ ▀█  ▒████▄     ██ ▀█   █ ▓  ██▒ ▓▒   ▒██▀ ██▌▒██▒  ██▒   ▓  ██▒ ▓▒▓██░ ██▒▒████▄   ▓  ██▒ ▓▒" -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "▒██▒   ▒▓█    ▄ ▒██  ▀█▄  ▓██  ▀█ ██▒▒ ▓██░ ▒░   ░██   █▌▒██░  ██▒   ▒ ▓██░ ▒░▒██▀▀██░▒██  ▀█▄ ▒ ▓██░ ▒░" -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "░██░   ▒▓▓▄ ▄██▒░██▄▄▄▄██ ▓██▒  ▐▌██▒░ ▓██▓ ░    ░▓█▄   ▌▒██   ██░   ░ ▓██▓ ░ ░▓█ ░██ ░██▄▄▄▄██░ ▓██▓ ░ " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "░██░   ▒ ▓███▀ ░ ▓█   ▓██▒▒██░   ▓██░  ▒██▒ ░    ░▒████▓ ░ ████▓▒░     ▒██▒ ░ ░▓█▒░██▓ ▓█   ▓██▒ ▒██▒ ░ " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "░▓     ░ ░▒ ▒  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒   ▒ ░░       ▒▒▓  ▒ ░ ▒░▒░▒░      ▒ ░░    ▒ ░░▒░▒ ▒▒   ▓▒█░ ▒ ░░   " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host " ▒ ░     ░  ▒     ▒   ▒▒ ░░ ░░   ░ ▒░    ░        ░ ▒  ▒   ░ ▒ ▒░        ░     ▒ ░▒░ ░  ▒   ▒▒ ░   ░    " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host " ▒ ░   ░          ░   ▒      ░   ░ ░   ░          ░ ░  ░ ░ ░ ░ ▒       ░       ░  ░░ ░  ░   ▒    ░      " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host " ░     ░ ░            ░  ░         ░                ░        ░ ░               ░  ░  ░      ░  ░        " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "       ░                                          ░                                                     " -ForegroundColor $fgColor -BackgroundColor $bgColor
    Write-Host "                                                                                                        " -ForegroundColor $fgColor -BackgroundColor $bgColor
}

helloDave -fgColor Cyan

While ($true) {

    Write-Host "Please choose a filename:"
    $filename = Read-Host

    if ($filename -match "exit" -or $filename -match "quit") {
        goodbyeDave -fgColor DarkCyan
        Exit
    }

    Write-Host "Filename chosen: $filename"

    $currentDir = Get-Location

    try {
        New-Item -Path "$currentDir" -Name "$filename" -ItemType "File" -ErrorAction Stop
    } catch {
        if ($_.Exception.Message -like "*already exists*") {
            Write-Host "I'm sorry Dave, that file seems to already exist" -ForegroundColor Red
            Continue
        } else {
            Write-Host "I'm sorry Dave, I'm afraid I can't do that" -ForegroundColor Red
            Continue
        }
    }

    $filePath = Join-Path -Path "$currentDir" -ChildPath "$filename"
    Write-Host "File created at: $filePath"

    try {
        Write-Host "What do you want to put into this file?"
        $fileInput = Read-Host

        if ($fileInput -match "open" -and $fileInput -match "door") {
            Throw "open doors"
        }

        Add-Content -Path $filePath -Value "$fileInput" -ErrorAction Stop
    } catch {
        if ($_.Exception.Message -like "*open doors*") {
            imSorryDave -fgColor Green
            Continue
        } else {
            Write-Host "Why are you like this, Dave?"
            Continue
        }
    }
}

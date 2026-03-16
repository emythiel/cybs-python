@echo off
powershell -Command "Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File \"%~dp0service.ps1\"' -Verb RunAs"

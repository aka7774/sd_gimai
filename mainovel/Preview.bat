@echo off
PowerShell -Version 5.1 -ExecutionPolicy RemoteSigned -File "%~dp0LaunchPreviewServer.ps1" "%~dp0mainovel.json" 0

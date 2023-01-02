@echo off
pushd %~dp0..\..\..
set PYTHON=%CD%
popd
set PYTHON=%PYTHON%\venv\Scripts\Python.exe
%PYTHON% -m http.server 8080 --bind 127.0.0.1

rem Windows batch script to setup the azure environment on windows machines.
rem Author: James Bruno
rem Date: 5/27/2018

@echo off

rem See if python is installed
python --version 2>1 1>NUL
if %ERRORLEVEL% NEQ 0 (
	echo Python does not seem to be installed on this machine.
	echo Please install Python. 
	goto :eof ) 

rem see if it's python 3
for /f "tokens=*" %%a in ('python --version 2^>^&1') do ( set pyversion=%%a )

echo %pyversion% | findstr /C:"Python 3" 
if %ERRORLEVEL% NEQ 0 (
	echo Only python 2 detected.  Please install Python 3. 
	goto :eof )

rem setup new envrionment
echo Creating azure environment
python -m venv azure_environment

echo activating azure_environment and installing from requirements.txt
echo azure_environment\Scripts\activate > activate.bat
activate.bat & pip install -r requirements.txt & python -m nltk.downloader perluniprops & deactivate


if %ERRORLEVEL% NEQ 0 ( 
	echo Installation Successfull.
	echo To begin using the azure environemnt, type "activate".
	echo When you are finished, type "deactivate" )

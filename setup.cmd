@echo off
chcp 65001 > nul
setlocal

REM Get the directory where setup.cmd is located (User project root)
set "USER_ROOT=%~dp0"
if "%USER_ROOT:~-1%"=="\" set "USER_ROOT=%USER_ROOT:~0,-1%"

REM Set target Agents path to one directory up from the user project root
set "AGENTS_DIR=%USER_ROOT%\..\Agents"

REM Convert to absolute path
for %%i in ("%AGENTS_DIR%") do set "AGENTS_DIR=%%~fi"

set "REPO_URL=git@github.com:jackutea/Agents.git"

REM Step 1: Clone or update Agents repo
if exist "%AGENTS_DIR%\.git" (
    echo [INFO] Agents repository found, updating...
    pushd "%AGENTS_DIR%"
    git pull
    popd
) else (
    echo [INFO] Agents repository not found, cloning...
    pushd "%USER_ROOT%\.."
    git clone "%REPO_URL%" Agents
    popd
)

REM Step 2: Copy .github directory
set "SOURCE=%AGENTS_DIR%\.github"
set "TARGET=%USER_ROOT%\.github"

if not exist "%SOURCE%" (
    echo [ERROR] Source directory "%SOURCE%" not found. Check if clone/update succeeded.
    pause
    exit /b 1
)

echo [INFO] Copying all contents from "%SOURCE%" to "%TARGET%" ...

REM /E Copies directories and subdirectories, including empty ones.
REM /I If destination does not exist and copying more than one file, assumes that destination must be a directory.
REM /Y Suppresses prompting to confirm you want to overwrite an existing destination file.
REM /H Copies hidden and system files also.
REM /R Overwrites read-only files.
xcopy "%SOURCE%\*" "%TARGET%\" /E /I /Y /H /R

echo [INFO] Copy complete!
pause

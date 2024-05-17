@echo off
setlocal enabledelayedexpansion

:: Function to check if a virtual environment is already active
set VENV_ACTIVE=0
if defined VIRTUAL_ENV (
    set VENV_ACTIVE=1
)

:: Check if a virtual environment is already active
if %VENV_ACTIVE%==1 (
    echo A virtual environment is already active: %VIRTUAL_ENV%
) else (
    :: Check if virtual environment directory exists in the current or parent directory
    if exist "env\" (
        set VENV_DIR=env
    ) else if exist "..\env\" (
        set VENV_DIR=..\env
    ) else (
        :: Ask user where to create the virtual environment
        set /p create_venv=No virtual environment found. Do you want to create one in the current directory (.\env)? [y/N]: 
        if /i "!create_venv!"=="y" (
            set VENV_DIR=env
            python -m venv %VENV_DIR%
            call %VENV_DIR%\Scripts\activate
            echo Created and activated virtual environment: %VENV_DIR%
        ) else (
            echo Virtual environment not created. Exiting.
            exit /b 1
        )
    )

    :: Activate the virtual environment
    call %VENV_DIR%\Scripts\activate
    echo Activated virtual environment: %VENV_DIR%

    :: Upgrade pip
    pip install --upgrade pip
    echo Upgraded pip to the latest version.

    :: Check for requirements.txt in various locations and install packages
    if exist "requirements.txt" (
        pip install -r "requirements.txt"
    ) else if exist "..\requirements.txt" (
        pip install -r "..\requirements.txt"
    ) else (
        echo requirements.txt not found in the current or parent directory!
        exit /b 1
    )
)

:: Navigate to the project directory and run the Streamlit app
set SCRIPT_DIR=%~dp0
set APP_DIR=%SCRIPT_DIR%app

if exist "%APP_DIR%" (
    cd "%APP_DIR%" || (echo Failed to navigate to app directory: %APP_DIR% & exit /b 1)
    streamlit run app.py
) else (
    echo App directory not found: %APP_DIR%
    exit /b 1
)

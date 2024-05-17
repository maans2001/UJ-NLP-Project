# How to Run Your Project

This guide provides instructions on how to set up and run your project on Windows, macOS, and Linux operating systems.

## Prerequisites

Before running the scripts, ensure you have the following installed on your system:
- Python 3.x
- pip (Python package installer)
- Streamlit

## Windows

### Instructions

1. Open Command Prompt (cmd) or PowerShell.

2. Navigate to the directory where the `run_windows.bat` script is located:
    ```cmd
    cd path\to\your\project\directory
    ```

3. Run the script:
    ```cmd
    run_windows.bat
    ```

4. Follow the on-screen instructions. The script will:
    - Check for an existing virtual environment.
    - Create and activate a virtual environment if not found.
    - Install dependencies from `requirements.txt`.
    - Navigate to the `app` directory and run the Streamlit app.

## macOS

### Instructions

1. Open Terminal.

2. Navigate to the directory where the `run_macosx.sh` script is located:
    ```sh
    cd /path/to/your/project/directory
    ```

3. Make the script executable (if it is not already):
    ```sh
    chmod +x run_macosx.sh
    ```

4. Run the script:
    ```sh
    ./run_macosx.sh
    ```

5. Follow the on-screen instructions. The script will:
    - Check for Python 3 and pip.
    - Check for an existing virtual environment.
    - Create and activate a virtual environment if not found.
    - Install dependencies from `requirements.txt`.
    - Navigate to the `app` directory and run the Streamlit app.

## Linux

### Instructions

1. Open Terminal.

2. Navigate to the directory where the `run.sh` script is located:
    ```sh
    cd /path/to/your/project/directory
    ```

3. Make the script executable (if it is not already):
    ```sh
    chmod +x run.sh
    ```

4. Run the script:
    ```sh
    ./run.sh
    ```

5. Follow the on-screen instructions. The script will:
    - Check for an existing virtual environment.
    - Create and activate a virtual environment if not found.
    - Install dependencies from `requirements.txt`.
    - Navigate to the `app` directory and run the Streamlit app.

## Notes

- Ensure you have the necessary permissions to create and execute scripts on your system.
- If you encounter any issues with the scripts, check the error messages and ensure all prerequisites are installed correctly.
- The project directory should contain the `requirements.txt` file and an `app` subdirectory with the `app.py` file.

By following these instructions, you should be able to set up and run your project on Windows, macOS, and Linux operating systems without any issues.

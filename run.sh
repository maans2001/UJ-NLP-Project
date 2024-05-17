#!/bin/bash

# Function to check if a virtual environment is already active
function is_venv_active {
  if [[ -n "$VIRTUAL_ENV" ]]; then
    return 0
  else
    return 1
  fi
}

# Function to create and activate a virtual environment
function create_and_activate_venv {
  local venv_dir=$1
  python3 -m venv "$venv_dir"
  source "$venv_dir/bin/activate"
  echo "Created and activated virtual environment: $venv_dir"
}

# Function to install requirements
function install_requirements {
  local requirements_file=$1
  if [ -f "$requirements_file" ]; then
    pip install -r "$requirements_file"
  else
    echo "requirements.txt not found at $requirements_file!"
    exit 1
  fi
}

# Check if a virtual environment is already active
if is_venv_active; then
  echo "A virtual environment is already active: $VIRTUAL_ENV"
else
  # Check if virtual environment directory exists in the current or parent directory
  if [ -d "./env" ]; then
    VENV_DIR="./env"
  elif [ -d "../env" ]; then
    VENV_DIR="../env"
  else
    # Ask user where to create the virtual environment
    read -p "No virtual environment found. Do you want to create one in the current directory (./env)? [y/N]: " create_venv
    if [[ "$create_venv" =~ ^[Yy]$ ]]; then
      VENV_DIR="./env"
      create_and_activate_venv "$VENV_DIR"
    else
      echo "Virtual environment not created. Exiting."
      exit 1
    fi
  fi

  # Activate the virtual environment
  source "$VENV_DIR/bin/activate"
  echo "Activated virtual environment: $VENV_DIR"

  # Upgrade pip
  pip install --upgrade pip
  echo "Upgraded pip to the latest version."

  # Check for requirements.txt in various locations and install packages
  if [ -f "./requirements.txt" ]; then
    install_requirements "./requirements.txt"
  elif [ -f "../requirements.txt" ]; then
    install_requirements "../requirements.txt"
  else
    echo "requirements.txt not found in the current or parent directory!"
    exit 1
  fi
fi

# Navigate to the project directory and run the Streamlit app
SCRIPT_DIR="$(dirname "$0")"
APP_DIR="$SCRIPT_DIR/app"

if [ -d "$APP_DIR" ]; then
  cd "$APP_DIR" || { echo "Failed to navigate to app directory: $APP_DIR"; exit 1; }
  streamlit run app.py
else
  echo "App directory not found: $APP_DIR"
  exit 1
fi

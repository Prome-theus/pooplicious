#!/bin/bash

pip install virtualenv
# Function to set up virtual environment
setup_virtualenv() {
    echo "Setting up virtual environment..."
    python -m venv .venv
    source venv/bin/activate
    echo "Virtual environment set up."
}

# Function to install dependencies
install_dependencies() {
    echo "Installing dependencies..."
    pip install -r requirements.txt  # Assuming you have a requirements.txt file listing your dependencies
    echo "Dependencies installed."
}

# Function to run the Pygame project
run_project() {
    echo "Running Pygame project..."
    python main.py  # Replace 'main.py' with the name of your Python script
}

# Check if the script is running on Windows or Linux and execute the appropriate commands
if [[ "$OSTYPE" == "msys" ]]; then  # Running on Windows
    setup_virtualenv
    install_dependencies
    run_project
elif [[ "$OSTYPE" == "linux-gnu" ]]; then  # Running on Linux
    setup_virtualenv
    install_dependencies
    run_project
else
    echo "Unsupported operating system."
    exit 1
fi

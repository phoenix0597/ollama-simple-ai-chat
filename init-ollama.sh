#!/bin/sh

set -e

echo "Waiting for Ollama service to be ready..."
sleep 10

echo "Checking if deepseek-r1 model is already installed..."
if ollama list | grep -q "deepseek-r1"; then
    echo "Model deepseek-r1 is already installed"
    echo "Current models:"
    ollama list
else
    echo "Installing deepseek-r1 model (this may take a while)..."
    echo "Note: This will download several GB of data"

    if ollama pull deepseek-r1; then
        echo "Model deepseek-r1 installed successfully"
        echo "Current models:"
        ollama list
    else
        echo "Failed to install deepseek-r1 model"
        exit 1
    fi
fi

echo "Testing model with a simple question..."
echo "Hello, can you respond?" | ollama run deepseek-r1

echo "Ollama setup completed successfully!"
echo "Available models:"
ollama list
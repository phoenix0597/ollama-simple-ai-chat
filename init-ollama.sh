#!/bin/sh

set -eux

# Получаем имя модели из переменной окружения
MODEL_NAME=${OLLAMA_MODEL:-deepseek-r1}

echo "Waiting for Ollama service to be ready..."
sleep 10

echo "Checking if ${MODEL_NAME} model is already installed..."
if ollama list | grep -q "${MODEL_NAME}"; then
    echo "Model ${MODEL_NAME} is already installed"
    echo "Current models:"
    ollama list
else
    echo "Installing ${MODEL_NAME} model (this may take a while)..."
    echo "Note: This will download several GB of data"

    if ollama pull "${MODEL_NAME}"; then
        echo "Model ${MODEL_NAME} installed successfully"
        echo "Current models:"
        ollama list
    else
        echo "Failed to install ${MODEL_NAME} model"
        exit 1
    fi
fi

echo "Testing model with a simple question..."
echo "Hello, can you respond?" | ollama run "${MODEL_NAME}"

echo "Ollama setup completed successfully!"
echo "Available models:"
ollama list
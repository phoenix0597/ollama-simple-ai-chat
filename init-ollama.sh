#!/bin/bash

set -e

echo "Waiting for Ollama service to be ready..."
sleep 15

# Функция для проверки доступности Ollama
check_ollama() {
    ollama list > /dev/null 2>&1
    return $?
}

# Проверяем доступность Ollama API
max_attempts=20
attempt=1

while [ $attempt -le $max_attempts ]; do
    echo "Attempt $attempt/$max_attempts: Checking Ollama service..."

    if check_ollama; then
        echo "Ollama service is ready!"
        break
    fi

    echo "Ollama not ready yet, waiting 15 seconds..."
    sleep 15
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    echo "Failed to connect to Ollama service after $max_attempts attempts"
    echo "Trying to list available models anyway..."
    ollama list || true
    exit 1
fi

echo "Checking if deepseek-r1 model is already installed..."
if ollama list | grep -q "deepseek-r1"; then
    echo "Model deepseek-r1 is already installed"
    echo "Current models:"
    ollama list
else
    echo "Installing deepseek-r1 model (this may take a while)..."
    echo "Note: This will download several GB of data"

    # Устанавливаем модель с более подробным выводом
    if ollama pull deepseek-r1; then
        echo "Model deepseek-r1 installed successfully"
        echo "Current models:"
        ollama list
    else
        echo "Failed to install deepseek-r1 model"
        echo "Trying to list available models to debug:"
        ollama list || true
        exit 1
    fi
fi

echo "Testing model with a simple question..."
echo "Testing the model..." | ollama run deepseek-r1 --verbose

echo "Ollama setup completed successfully!"
echo "Available models:"
ollama list
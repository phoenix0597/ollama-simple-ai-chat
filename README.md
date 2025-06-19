# Ollama simple AI chat (запускается локальная ИИ-модель DeepSeek-R1 и др. и веб-интерфейс)

Полноценное решение для запуска Ollama с моделью DeepSeek-R1 и веб-интерфейсом.

## Запуск

1. Клонируйте репозиторий и перейдите в директорию приложения:
```bash
git clone https://github.com/phoenix0597/ollama-simple-ai-chat.git
cd ollama-simple-ai-chat
```
2. Запустите все сервисы:

```bash
docker-compose up --build -d
```

3. Откройте веб-интерфейс: http://localhost:8080

Сервисы

* Ollama API: http://localhost:11434
* Веб-интерфейс: http://localhost:8080

Управление

## Остановить все сервисы
```bash
docker-compose down
```

## Остановить и удалить данные
```bash
docker-compose down -v
```

## Перезапустить
```bash
docker-compose restart
```

## Посмотреть логи

```bash
docker-compose logs -f
```



## Система автоматически:


Запустит Ollama
Дождется готовности сервиса
Загрузит модель DeepSeek-R1:8b 
(как изменить загружаемую модель см. ниже)
Запустит веб-интерфейс для тестирования

Модель будет сохранена в Docker volume, так что при перезапуске повторно загружаться не будет.

## Конфигурация
### Переменные окружения
Все основные настройки приложения выносятся в файл .env. Скопируйте .env.example в .env и настройте по своим потребностям:

```bash
cp .env.example .env
```

### Смена AI модели
Для смены модели ИИ измените значение OLLAMA_MODEL в файле .env:
bash# Примеры популярных моделей:

* OLLAMA_MODEL=deepseek-r1     # Модель по умолчанию
* OLLAMA_MODEL=llama3.1        # Llama 3.1
* OLLAMA_MODEL=llama3.2        # Llama 3.2
* OLLAMA_MODEL=mistral         # Mistral
* OLLAMA_MODEL=codellama       # Code Llama
* OLLAMA_MODEL=gemma2          # Gemma 2


Все доступные модели см. здесь: https://ollama.com/library
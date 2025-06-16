# Ollama DeepSeek-R1 Setup

Полноценное решение для запуска Ollama с моделью DeepSeek-R1 и веб-интерфейсом.

## Запуск

1. Клонируйте репозиторий и перейдите в директорию:
```bash
cd ai-agent-with-rag
```

2. Сделайте скрипт инициализации исполняемым:
```bash
chmod +x init-ollama.sh
```

3. Запустите все сервисы:

```bash
docker-compose up -d
```

4. Проверьте логи инициализации:

```bash docker-compose logs -f ollama-init
```

5. Откройте веб-интерфейс: http://localhost:8080

Сервисы

* Ollama API: http://localhost:11434
* Веб-интерфейс: http://localhost:8080

Управление

# Остановить все сервисы
```bash
docker-compose down
```

# Остановить и удалить данные
```bash
docker-compose down -v
```

# Перезапустить
```bash
docker-compose restart
```

# Посмотреть логи

```bash
docker-compose logs -f
```


## Запуск

1. Создайте директорию и файлы:
```bash
mkdir ollama-setup && cd ollama-setup
# Создайте все файлы согласно структуре выше
Код


Сделайте скрипт исполняемым:

chmod +x init-ollama.sh

Запустите:

docker-compose up -d

Откройте http://localhost:8080 для доступа к веб-интерфейсу.

Система автоматически:


Запустит Ollama
Дождется готовности сервиса
Загрузит модель DeepSeek-R1
Запустит веб-интерфейс для тестирования

Модель будет сохранена в Docker volume, так что при перезапуске повторно загружаться не будет.
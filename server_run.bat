@echo off
chcp 65001 >nul
setlocal

set "VENV_PATH=.venv"
 

echo ==========================================
echo Запуск бота для Яндекс Мессенджера
echo ==========================================

:: Активация виртуального окружения
if exist "%VENV_PATH%\Scripts\activate.bat" (
    call "%VENV_PATH%\Scripts\activate.bat"
) else (
    echo [!] Виртуальное окружение не найдено. Создаю новое...
    python -m venv %VENV_PATH%
    if exist "%VENV_PATH%\Scripts\activate.bat" (
        call "%VENV_PATH%\Scripts\activate.bat"
    ) else (
        echo [X] Не удалось создать виртуальное окружение.
        pause
        exit /b 1
    )
)

echo [OK] Виртуальное окружение активировано.

:: Установка зависимостей
echo [*] Проверка и установка зависимостей...
pip install --quiet fastapi uvicorn requests
if %errorlevel% neq 0 (
    echo [X] Ошибка при установке зависимостей!
    pause
    exit /b 1
)
echo [OK] Зависимости установлены.

:: Экспорт токена (для Windows CMD)
set BOT_TOKEN=%BOT_TOKEN%

echo [*] Запуск сервера (host=0.0.0.0, port=8000)...
echo [INFO] Сервер будет доступен по адресу: https://bot.globalinstore.ru/webhook
echo ------------------------------------------

:: Запуск Uvicorn как CLI (НЕ через uvicorn.run в коде!)
uvicorn server2:app --host 0.0.0.0 --port 8000 --log-level info

:: Если сервер упал — пауза, чтобы увидеть ошибку
if %errorlevel% neq 0 (
    echo [X] Сервер завершился с ошибкой.
)
pause

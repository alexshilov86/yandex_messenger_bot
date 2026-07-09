@echo off
chcp 65001 >nul

REM Путь к виртуальной среде — поправьте, если у вас иначе
set "VENV_PATH=.venv"

if exist "%VENV_PATH%\Scripts\activate.bat" (
    echo Активация виртуального окружения...
    call "%VENV_PATH%\Scripts\activate.bat"
) else (
    echo Виртуальное окружение не найдено. Пробую запустить без него...
)

echo Проверка/установка зависимостей...
pip install --quiet fastapi uvicorn requests || (
    echo Ошибка установки зависимостей!
    pause
    exit /b 1
)

echo Запуск бота из server2.py...
REM Для продакшена уберите --reload
uvicorn server2:app --host 0.0.0.0 --port 8000 --reload

pause

@echo off

if exist instagram (
    rmdir /s /q instagram
)

python -m venv instagram

call instagram\Scripts\activate

python.exe -m pip install --upgrade pip

pip install -r requirements.txt

echo Done
pause
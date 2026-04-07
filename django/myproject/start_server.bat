@echo off
echo Starting HealthPredict Backend Server...
echo Make sure your phone is on the same Wi-Fi as this PC.
echo Current IP:
ipconfig | findstr IPv4
echo.
python manage.py runserver 0.0.0.0:8000
pause

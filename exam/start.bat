@echo off
start cmd /k "cd /d 'E:\Workspace\Django Projects\Freelancer.com\Exam_Django\exam' & ..\env\Scripts\activate & python manage.py runserver"
start "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" "http://127.0.0.1:8000/"
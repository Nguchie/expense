
import os
import subprocess
import time

# Change the directory to your Django project directory
os.chdir(r'C:\Users\wambo\OneDrive\Desktop\Stunner\st_expense')

# Start the Django development server
subprocess.Popen(['python', 'manage.py', 'runserver'])

# Keep the script running
while True:
    time.sleep(1)

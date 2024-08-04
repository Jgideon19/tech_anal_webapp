# Create a new file named `run.sh` in your project root:
#!/bin/bash
python data_init.py
gunicorn main:app

# Update your Procfile to use this shell script:
web: sh run.sh

# Make sure to make run.sh executable:
chmod +x run.sh
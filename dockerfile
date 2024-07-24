FROM python:3.11

WORKDIR /fast_api_mvc

# Copy Files
COPY . .

# Install Netcat
RUN apt-get update && apt-get install -y netcat-openbsd

# Install Packages
RUN pip install -r requirements.txt

# Set Permissions
RUN chmod +x commands/wait_for_db.sh

CMD ["sh", "-c", "./commands/wait_for_db.sh db 3306 -- alembic upgrade head && python3 run.py"]

FROM python:3.9-slim

WORKDIR /app

# Install PostgreSQL client and PowerShell
RUN apt-get update && \
    apt-get install -y postgresql-client wget apt-transport-https software-properties-common gnupg2 && \
    wget -q https://packages.microsoft.com/config/debian/10/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y powershell && \
    rm -rf /var/lib/apt/lists/* packages-microsoft-prod.deb

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./init.ps1 /init.ps1
# No need to chmod for PowerShell script

COPY . /app/

# Command will be overridden in docker-compose for different services
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "task_project.wsgi:application"]
# invest
Simple Django APP

How to deploy the app on a Ubuntu 16.04 server.

Install Python 3.7.0 on Ubuntu 16.04

Step 1 – Prerequsiteis

Use the following command to install prerequisites for Python before installing it.
```
sudo apt-get install build-essential checkinstall
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
```
Step 2 – Download Python 3.7

```
cd /usr/src
sudo wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
```
Now extract the downloaded package.
```
sudo tar xzf Python-3.7.0.tgz
```
Step 3 – Compile Python Source
Use below set of commands to compile python source code on your system using altinstall.
```
cd Python-3.7.0
sudo ./configure --enable-optimizations
sudo make altinstall
make altinstall is used to prevent replacing the default python binary file /usr/bin/python.
```

Step 4 – Check Python Version
Check the latest version installed of python using below command
```
python3.7 -V
```
Python-3.7.0

Install Pipenv package useing pip3 
```
pip3 install pipenv 
echo "export PIPENV_VENV_IN_PROJECT=1" >> ~/.bashrc
bash
```

Download and install Git on the system
```
apt-get install git
```
Downlod and the Django App
```
cd /var/www/
git clone https://github.com/ms1ra/invest.git invest 
cd invest/
pipenv install --skip-lock
pipenv shell
pip list
python manage.py createsuperuser
python manage.py collectstatic --no-input
```
Setup gunicorn webserver for Django App
```
vim /etc/systemd/system/dango.service
```
```
[Unit]
Description=Django Application service By Saiful Islam Rokon
After=network.target
[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/invest
ExecStart=/var/www/invest/.venv/bin/gunicorn --workers 2 --bind 127.0.0.1:8000 invest.wsgi
[Install]
WantedBy=multi-user.target
```

Download and Insatall Nginx Webserver 
```
apt-get install nginx -y
```
```
vim /etc/nginx/sites-enabled/default
```
Setup Nginx reverse proxy for the Gunicorn server

```
server {
    listen 80;
    server_name localhost;
    location = /favicon.ico {
        access_log off; log_not_found off;
        }
    location /static/ {
        root /var/www/invest;
        }

    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://localhost:8000;
     }
}
```
Restart Nginx and django service for applying configration
```
service nginx restart
service django restart
```
Enable both service on Startup

```
systemctl enable django
systemctl enable nginx
```

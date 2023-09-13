# HOTSPOT Animanight (Django / Nginx / UWSGI)

#############################################################################################
# Installation du Yahboom FAN Cooling HAT
```
wget -i http://www.yahboom.net/xiazai/Raspberry_Pi_RGB_Cooling_HAT/Python_Code.zip
unzip Python_Code.zip
sudo apt install -y python3-smbus i2c-tools
sudo python -m pip install --upgrade pip setuptools wheel
sudo pip install Adafruit-SSD1306
sudo raspi-config
```

> [3] Interface Options - [I5] I2C - Enable

# Configuration CRONTAB
```
@reboot python3 /home/pi/RGB_Cooling_HAT/fan_temp.py
```
Version de Python
```
python3 --version
```
>Python 3.9.2

Localisation de Python
```
which python3
```
> /usr/bin/python3
sudo apt install python3-venv -y
mkdir env
python3 -m venv /home/pi/env/hotspot
source ~/env/hotspot/bin/activate
which python
#/home/pi/env/hotspot/bin/python
pip install django
django-admin startproject hotspot
sudo apt install python3.9-dev -y
sudo apt install gcc -y
pip install uwsgi

### Install Modules
pip3 install django-unixtimestampfield
pip3 install pillow
pip3 install django-imagekit
pip3 install django-debug-toolbar
pip3 install whitenoise
pip install filetype

nano test.py
def application(env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b"Hello World!"]

uwsgi --http :8000 --wsgi-file test.py 

uwsgi --http :8000 --module hotspot.wsgi
sudo apt install nginx -y

nano /etc/nginx/sites-available/hotspot.conf

# The upstream component nginx needs to connect to
upstream django {
    server unix:///home/pi/hotspot/hotspot.sock;
}
# Configuration of the server
server {
    listen                  80;
    server_name             hotspot.local www.hotspot.local;
    charset                 utf-8;
    # max upload size
    client_max_body_size    75M;
    # Django media et statif files
    location /media {
        alias /home/pi/hotspot/media;
    }
    location /static {
        alias /home/pi/hotspot/static;
    }
    # Send all non-media requests to the Django server.
    location / {
        uwsgi_pass          django;
        include             /home/pi/hotspot/uwsgi_params;
    }
}

nano uwsgi_params

uwsgi_param QUERY_STRING        $query_string;
uwsgi_param REQUEST_METHOD      $request_method;
uwsgi_param CONTENT_TYPE        $content_type;
uwsgi_param CONTENT_LENGTH      $content_length;
uwsgi_param REQUEST_URI         $request_uri;
uwsgi_param PATH_INFO           $document_uri;
uwsgi_param DOCUMENT_ROOT       $document_root;
uwsgi_param SERVER_PROTOCOL     $server_protocol;
uwsgi_param REQUEST_SCHEME      $scheme;
uwsgi_param HTTPS               $https if_not_empty;
uwsgi_param REMOTE_ADDR         $remote_addr;
uwsgi_param REMOTE_PORT         $remote_port;
uwsgi_param SERVER_PORT         $server_port;
uwsgi_param SERVER_NAME         $server_name;

sudo ln -s /etc/nginx/sites-available/hotspot.conf /etc/nginx/sites-enabled

nano hotspot/setting.py

import os

STATIC_ROOT=os.path.join(BASE_DIR, "static/")

./manage.py collectstatic
mkdir media
wget https://www.animanight.com/images/logo10.png -O media/logo10.png
ll media

sudo /etc/init.d/nginx restart

uwsgi --socket hotspot.sock --module hotspot.wsgi --chmod-socket=666

nano hotspot_uwsgi.ini

[uwsgi]
# fill path to Django project's root directory
chdir           = /home/pi/hotspot/
# Django's wsgi file
module          = hotspot.wsgi
# Full path to python virtual env
home            = /home/pi/env/hotspot
# Enable uswgi master process
master          = true
# Maximum numboer of worker process
processes       = 10
# The socket (use the full path to be safe)
socket          = /home/pi/hotspot/hotspot.sock
# Socket permissions
chmod-socket    = 666
# Clear environment on exit
vacuum          = true
# Daemonize uwsgi and write message into given log
daemonize       = /home/pi/uwsgi-emperor.log

# Initialise uwsgi 
uwsgi --ini hotspot_uwsgi.ini
##  check process
ps aux

cd /home/pi/env/hotspot
mkdir vassals

sudo ln -s /home/pi/hotspot/hotspot_uwsgi.ini /home/pi/env/hotspot/vassals
ll vassals

# test avec les droits
uwsgi --emperor /home/pi/env/hotspot/vassals --uid www-data --gid www-data

sudo nano /etc/systemd/system/emperor.uwsgi.service
[Unit]
Description=uwsgi emperor for hotspot domains website
After=network.target
[Service]
User=pi
Restart=always
ExecStart=/home/pi/env/hotspot/bin/uwsgi --emperor /home/pi/env/hotspot/vassals --uid www-data --gid www-data
[Install]
WantedBy=multi-user.target

systemctl enable emperor.uwsgi.service
systemctl start emperor.uwsgi.service


#### SMB
sudo apt install samba samba-common-bin -y
sudo smbpasswd -a pi # live

mkdir /home/pi/hotspot/shared

sudo nano /etc/samba/smb.conf

[shared]
path = /home/pi/hotspot/shared
writeable=Yes
create mask=0777
directory mask=0777
public=no

sudo systemctl restart smbd
hostname -I

sudo systemctl restart rs

## GIT
sudo apt install git

echo "# hotspot" >> README.md
git init
git config --global user.email "webmaster@animanight.com"
git config --global user.name "wotanabee"
git config --global user.password "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"
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Wotanabee/hotspot.git
git push -u origin main



# live-stream
Module to set up live streaming using Raspberry pi

## Steps in Raspberry Pi

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install motion -y
sudo apt install v4l-utils -y
```


To check if the USB webcam can be detected by the system
```
lsusb
```


To get camera details
```
v4l2-ctl -V
```

To change the settings, edit /etc/motion/motion.conf file.
Change threshold for motion detection.

The files will be saved in target_dir /var/lib/motion by default.


To activate the daemon, edit /etc/default/motion and set start_motion_daemon to yes

```
sudo service motion start # or motion
```


Create a file called transfer_images.sh which will keep transferring the files to the web server by scp. However the whole process will execute only for 50 seconds to avoid overload to Raspberry Pi.
```
#!/bin/bash

end=$((SECONDS+50))
while true
do
    for f in `find /var/lib/motion/ -name "*.jpg"`
    do
        if [ $SECONDS -lt $end ]; then
            scp $f ubuntu@<remote_server_ip>:/home/ubuntu/.live-stream;
        else
            break;
        fi
    done;
    rm -rf /var/lib/motion/*;
    break;
done
```
and run as a cron task executing in every 2 minutes.
```
*/2 * * * * /home/ubuntu/transfer_images.sh" > /dev/null 2>&1 &
``` 


## Steps in web server (as sudo)

Copy this repository in the remote web server.

Run the setup.sh script or each commands in the file individually.

Activate the python virtualenvironment.
```
source /home/ubuntu/.env/bin/activate
```
Install the python dependencies.
```
pip install -r requirements.txt
```
Create a config.ini file in the project directory having credentials for logging in and entering the path where the image files are being copied by scp (e.g. /home/ubuntu/.live-stream).
```
[LIVESTREAM]
username = 
password = 
path = /home/ubuntu/.live-stream
```

To initiate the web server locally.
```
nohup sh -c "uwsgi --ini uwsgi.ini" > /dev/null 2>&1 &
```

Create a new file (using sudo) in /etc/nginx/sites-available/livestream and write the following:
```
server {
    listen 80;
    server_name <piblic ip pf server>;
    location / {
        proxy_pass http://localhost:5000;
        include         uwsgi_params;
    }
}
```

Link this file:
```
sudo ln -s /etc/nginx/sites-available/livestream /etc/nginx/sites-enabled/
```
Check nginx settings
```
sudo nginx -t
```
Restart nginx
```
sudo /etc/init.d/nginx restart
```


That's it. 

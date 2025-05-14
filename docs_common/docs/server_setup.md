### How to setup and manage your own server

Note! This is just one way to do it that I have found to work well

This method uses

- Amazon lightsail - for cheap server hosting (3.5 - 5$ per month)
- Amazon lambda - to manage the server, such as shutdown when limits are reached (free up to a certain quota per month)
- Cloudflare - for getting a domain, and to protect the server (5$/year for the domain)
- nginx - to setup server routing locally, and for enabling https (free)
- certbot - to install ssl certificate to enable https (free)
- Flask - backend server using python (free)

### Common Links

- Lightsail server instances: [https://lightsail.aws.amazon.com/ls/webapp/home/instances](https://lightsail.aws.amazon.com/ls/webapp/home/instances)
- Cloudflare homepage: [https://dash.cloudflare.com/](https://dash.cloudflare.com/)
- AWS controll panel: [https://eu-north-1.console.aws.amazon.com/console/home?region=eu-north-1](https://eu-north-1.console.aws.amazon.com/console/home?region=eu-north-1)

  `The main control panel, from here you can navigate to everywhere else using the search bar in the top left`

- AWS Lambda functions: [https://eu-north-1.console.aws.amazon.com/lambda/home?region=eu-north-1#/functions](https://eu-north-1.console.aws.amazon.com/lambda/home?region=eu-north-1#/functions)

  `Create python scripts that are triggered when events happen`

- AWS CloudWatch: [https://eu-north-1.console.aws.amazon.com/cloudwatch/home?region=eu-north-1#home](https://eu-north-1.console.aws.amazon.com/cloudwatch/home?region=eu-north-1#home)

  `Cloudwatch, where lambda function logs are stored, and where you can setup alarms and such`

- AWS IAM: [https://us-east-1.console.aws.amazon.com/iam/home?region=eu-north-1#/home](https://us-east-1.console.aws.amazon.com/iam/home?region=eu-north-1#/home)

### Here are some links related to pricing

[https://aws.amazon.com/free/compute/lightsail](https://aws.amazon.com/free/compute/lightsail)

[https://go.aws/49jYYpc](https://go.aws/49jYYpc)

### Related Articles

How to setup https with certbot: [https://dev.to/yousufbasir/setting-up-nginx-with-certbot-for-https-on-your-web-application-n1i](https://dev.to/yousufbasir/setting-up-nginx-with-certbot-for-https-on-your-web-application-n1i)

### nginx

After you have installed nginx, it can be found in: `/etc/nginx/`

You will be able to add your config files for how the routing should work, setup https etc. in the `/etc/nginx/conf.d` directory

#### Commands

Status nginx: `sudo systemctl status nginx`

Start nginx: `sudo systemctl start nginx`

Restart nginx: `sudo systemctl restart nginx`

Stop nginx: `sudo systemctl stop nginx`

Tail nginx logs: `sudo nginx -t`

### Other usefull commands and links

Only allow cloudflare connections: [https://www.cloudflare.com/ips/](https://www.cloudflare.com/ips/)

`Set up server to only accept connections routed through cloudflare(configure firewall to only accept ip ranges from list)`

List all the current python processes: `ps -fA | egrep "python|PID"`

### Connecting to ssh locally

```
chmod 400 ~/.ssh/key.pem

ssh -i ~/.ssh/key.pem <username here>@<Ip here>

example: ssh -i ~/.ssh/key.pem someuser@1.2.3.4
```

### SSH copy files

```
scp -i ~/.ssh/key.pem /c/somefile.txt someuser@1.2.3.4:/home/somefile.txt
```

### Start a script in the background

Example:

```
nohup python3 my_script.py &
```

Then press enter

### Configure nginx

```
server {
    listen 80;
    server_name vicmil.uk;

    root /var/www/vicmil.uk;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
server {
    listen 443 ssl;
    server_name vicmil.uk;

    ssl_certificate /etc/letsencrypt/live/vicmil.uk/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/vicmil.uk/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    root /var/www/vicmil.uk;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location /api {
        proxy_pass http://localhost:5002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    location /socket.io/ {
        proxy_pass http://localhost:5002;  # Replace with the correct port
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### How to set up a ssl certificate for ssh traffic

https://github.com/vicmil-pip/vicmil-pip-python-packages/tree/pyCertBot

### How to set up autentication

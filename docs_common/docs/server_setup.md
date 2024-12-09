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

### Other usefull commands and links

Only allow cloudflare connections: [https://www.cloudflare.com/ips/](https://www.cloudflare.com/ips/)

`Set up server to only accept connections routed through cloudflare(configure firewall to only accept ip ranges from list)`


List all the current python processes: `ps -fA | egrep "python|PID"`

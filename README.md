# Multi Tiered Web Application 

## Original repo:
https://github.com/brichbourg/Multi-Tier-App-Demo  
by: Brantley Richbourg (brichbourg@gmail.com)

This is a modified repo; multiple updates have been made to the Python codes. The original repo has various errors: syntax errors, command errors, etc.  
I will create a video for this repo to run the whole configurations under:
1. VMS/EC2: the YouTube video:
2. Docker/Kubernetes:

This repo comes with a Vagrant file to provision the machines under Virtual Box. To use the Vagrant file, you have to install Vagrant.

## Information
This is a Python-based web application that we developed back in the days when I was in training as a "DevOps Engineer" at m2iformation, who was hiring Ilkilab trainers to guide us through. We were more interested in CI/CD, so we didn't care about whether the code was working or not. My work here was to correct the code and update it to be compatible with Python 3 and Ubuntu 22.

This app is very simple; we have:
- A front web page hosted on Apache2 in the web server.
- An app behind the web page that is responsible for querying the data from the database. An Apache2 is also installed on this server (app server) to allow the web server to make HTTP requests to the app server.
- A MySQL server which holds our database.

On the front page, we could either: view the table in the database, insert an element, or clear the table in the database. The original repo had some issues in querying the data, HTTP requests, clearing the table, connecting to the database after clearing the table, and other issues like parsing the HTML response. Some commands in Python were deprecated (like `urllib.urlopen`) and others.

### The versions of the systems used:
* bento/ubuntu-22.04
* Python3: Python 3.10.12
* Apache/2.4.52 (Ubuntu)
* MySQL Ver 8.0.39-0ubuntu0.22.04.1 for Linux on x86_64 (Ubuntu)

## Screenshots

Here is a screenshot of the application.

### Main Menu: 

<div>
    <img src="screenshots/view.jpg" alt="Screenshot 1" width="300" style="display:inline-block; margin-right:10px;">
    <img src="screenshots/enterdata.jpg" alt="Screenshot 2" width="300" style="display:inline-block; margin-right:10px;">
    <img src="screenshots/clear.jpg" alt="Screenshot 3" width="300" style="display:inline-block;">
</div>

## Installation Instructions

### Web and App servers:
* Install Apache2 on both servers:
```bash
sudo apt update
sudo apt install apache2 -y
```
* Install Python3/Pip:
```bash
sudo apt update
sudo apt install python3 python3-pip -y
```
* Clone the repo:
```bash
sudo apt-get install git
git clone https://github.com/devops-and-more/Multi-tier-app.git
```
* run the script dedecated to place the files inside /var/www/html/, if you have some issues with the script you can copy the files manually:
```bash
cd Multi-Tier-App-Demo/
sudo bash install.sh
```
  
* Modify Apaches configs:
To point to the app directory and to allow cgi
```bash
# Change DocumentRoot to point to /var/www/html/appdemo
# This command updates the DocumentRoot in the Apache configuration
# to serve files from the new application directory.
sudo sed -i 's|DocumentRoot /var/www/html|DocumentRoot /var/www/html/appdemo|' /etc/apache2/sites-available/000-default.conf

# Remove the existing <Directory> section in 000-default.conf
# This command deletes any existing <Directory> sections for /var/www/html
# to avoid conflicts or duplication in the configuration.
sudo sed -i '/<Directory \/var\/www\/html>/,/<\/Directory>/d' /etc/apache2/sites-available/000-default.conf

# Append new <Directory> section directly after <VirtualHost *:80>
# This command inserts a new <Directory> block to allow CGI execution
# and set 'index.py' as the default file when accessing the directory.
sudo sed -i '/<VirtualHost \*:80>/a \
<Directory /var/www/html> \
    Options +ExecCGI \
    DirectoryIndex index.py \
</Directory>' /etc/apache2/sites-available/000-default.conf
```

### Web server configs:
The web server needs to accept all inbound connections therefore:
Changing Listen 80 to Listen 0.0.0.0:80: This modification makes Apache listen for incoming connections on port 80 from any IP address (0.0.0.0) rather than just the local host.
```bash
sudo sed -i 's|Listen 80|Listen 0.0.0.0:80|' /etc/apache2/ports.conf
sudo systemctl restart apache2
```
### App server configs:
* Configure apache to listen on port 8080 (just to distinguish between the two) to the connections comming from localhost and web server only, this is for security reasons

```bash
sudo sed -i 's|Listen 80|Listen localhost:8080\nListen web:8080|' /etc/apache2/ports.conf
sudo sed -i 's|<VirtualHost \*:80>|<VirtualHost localhost:8080 web:8080>|' /etc/apache2/sites-available/000-default.conf # note that I used \* otherwise sed will not find a match
```
* Install package to allow app servers to connect to MySQL:
```bash
pip install mysql-connector-python
```
 the `/etc/mtwa/mtwa.conf` file looks like:
```bash
# Multi-Tier-App-Demo configuration file

# Enter the name of the app server or load balancer (DNS or IP address; DNS preferred)
AppServerName = app
# Enter the name of the MySQL server (DNS or IP address; DNS preferred)
DBServerName = db
```
those two dns names are already configured inside /etc/hosts, if you use diffrent names you should change the file here to match your /etc/hosts file.
Becareful the well functioning of the app depends on this!!!

### Mysql server:
install mysql:
```bash
sudo apt-get update
sudo apt-get install mysql-server
```
* Download the initial SQL file:
```bash
wget "https://github.com/devops-and-more/Multi-tier-app/tree/master/sql/create_db_table.sql"
```

* Now log into your MySQL server as root where your pwd should contains the downloaded file (.sql); because you need it once you are inside mysql:
```bash
mysql -u root -p
# <enter your root password>
# after logging create the table from the file
source ~/create_db_table.sql;
```

Here is the SQL code being injected:
```sql
CREATE DATABASE `appdemo`;
USE `appdemo`;
CREATE TABLE `demodata` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100),
    `notes` TEXT,
    `timestamp` TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY (`name`)
);

CREATE TABLE `demodata_erase_log` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `timestamp` TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY (`timestamp`)
);
# Create a new user 'appdemo' that can connect from any host ('%') with the password 'appdemo'.
CREATE USER 'appdemo'@'%' IDENTIFIED BY 'appdemo';
# Grant all privileges on the 'appdemo' database to the user 'appdemo', allowing them to grant these privileges to other users.
GRANT ALL PRIVILEGES ON appdemo.* TO 'appdemo'@'%' WITH GRANT OPTION;
```

* Edit `/etc/mysql/mysql.conf.d/mysqld.cnf` to allow for network connections. Use VI or NANO to edit and change `bind-address = 127.0.0.1` to `bind-address = *`. This will tell MySQL to listen for connections on port TCP:3306 on all interfaces:

sudo sed -i bind-address = 127.0.0.1|bind-address = * /etc/mysql/mysql.conf.d/mysqld.cnf


### ####################################################################################"""
## ####################################################################################"""""""

### Web Server Installation (Required)

* Update Advanced Packaging Tool:
```bash
sudo apt-get update
sudo apt-get dist-upgrade
```



### App Server Installation (Required)

For the app server, **FOLLOW THE WEB SERVER DIRECTIONS ABOVE**, but make two changes to have Apache2 listen on port 8080 vs 80.

* Run the following commands:
```bash
wget "https://s3.amazonaws.com/richbourg-s3/mtwa/app/ports.conf"
wget "https://s3.amazonaws.com/richbourg-s3/mtwa/app/000-default.conf"
sudo cp 000-default.conf /etc/apache2/sites-enabled/
sudo cp ports.conf /etc/apache2/
```

* Restart Apache2:
```bash
sudo service apache2 restart
```

### MySQL Server Installation (Required)

This is going to be on a separate server from your web/app server.

* Update Advanced Packaging Tool:
```bash
sudo apt-get update
```

* Install MySQL:
```bash
sudo apt-get install mysql-server
```
**Make sure you create and remember your MySQL root password!**

* Download the initial SQL file:
```bash
wget "https://raw.githubusercontent.com/brichbourg/Multi-Tier-App-Demo/master/sql/create_db_table.sql"
```

* Now log into your MySQL server as root:
```bash
mysql -u root -p
<enter your root password>
```

* Run this command.  
**NOTE**: The example below assumes you ran the wget command from your home directory. Modify as needed:
```sql
mysql> source ~/create_db_table.sql;
```

Here is the SQL code being injected:
```sql
CREATE DATABASE `appdemo`;
USE `appdemo`;
CREATE TABLE `demodata` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100),
    `notes` TEXT,
    `timestamp` TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY (`name`)
);

CREATE TABLE `demodata_erase_log` (
    `id` INTEGER NOT NULL AUTO_INCREMENT,
    `timestamp` TIMESTAMP,
    PRIMARY KEY (`id`),
    KEY (`timestamp`)
);

CREATE USER 'appdemo'@'%' IDENTIFIED BY 'appdemo';
GRANT ALL PRIVILEGES ON appdemo.* TO 'appdemo'@'%' WITH GRANT OPTION;
```

* Edit `/etc/mysql/mysql.conf.d/mysqld.cnf` to allow for network connections. Use VI or NANO to edit and change `bind-address = 127.0.0.1` to `bind-address = *`. This will tell MySQL to listen for connections on port TCP:3306 on all interfaces:
```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
```
```
...
bind-address = *
```

* Restart MySQL:
```bash
sudo service mysql restart
```

* To verify MySQL was configured correctly, use netstat -l. You should see your `[serverip]:mysql` or `[serverip]:3306`:
```bash
brichbourg@db-1:~$ netstat -l
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 *:ssh                   *:*                     LISTEN     
tcp        0      0 *:mysql                 *:*                     LISTEN     
tcp6       0      0 [::]:ssh                [::]:*                  LISTEN  
```

### Final Web/App Server Configuration (Required)

Make sure you have run the `install.sh` shell script first, as that script will create and copy a configuration file needed for the application to run.

You need to edit your `/etc/mtwa/mtwa.conf` file on all of the servers and change the name `appserver.company.com` and `dbserver.company.com` listed in that file to the DNS names or IP addresses of the servers or load balancers you are going to use.

Here is what the `/etc/mtwa/mtwa.conf` file looks like:
```bash
# Multi-Tier-App-Demo configuration file

# Enter the name of the app server or load balancer (DNS or IP address; DNS preferred)
AppServerName = appserver.company.com
# Enter the name of the MySQL server (DNS or IP address; DNS preferred)
DBServerName = dbserver.company.com
```
It is recommended that you use DNS if possible, but IP address should work too.

### Configure Bash Menus (Optional)

Here we will configure the bash shell menu scripts that can be configured so that you can use a menu to start and stop services instead of having to type them into the CLI manually. The idea here is that this makes demos go faster and smoother.  

* Install Dialog:
```bash
sudo apt-get install dialog
```

* Move Script File:
You will need to copy the correct menu script *depending on the server you are configuring (Web, App or DB)*. The following example

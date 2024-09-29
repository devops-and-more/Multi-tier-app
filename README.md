# Multi Tiered Web Application 

## Original repo:

https://github.com/brichbourg/Multi-Tier-App-Demo  
by: Brantley Richbourg (brichbourg@gmail.com)

This is a modified repo, multiple updates have been done to the Python code; the original repo had various errors: syntax errors, command errors, etc.  
I will create a video for this repo to run the whole configurations under:  
1- VMS/EC2: the YouTube video:  
2- Docker/Kubernetes:  
This repo comes with a Vagrant file to provision the machines under Virtual Box; to use the Vagrant file, you have to install Vagrant.

## Information
This is a Python-based web application which we developed back in the days when I was in training as a "DevOps Engineer" at m2iformation, which was hiring Ilkilab trainers to guide us through. We were more interested in CI/CD, so we didn't care about whether the code was working or not. My work here was to correct the code and update it to be compatible with Python 3 and Ubuntu 22.  
This app is very simple; we have:
- A front web page hosted on Apache2 in the web server.
- An app behind the web page which is responsible for querying the data from the database; an Apache2 is also installed on this server (app server) to allow the web server to make HTTP requests to the app server.
- A MySQL server which holds our database.

On the front page, we could either view the table in the database, insert an element, or clear the table in the database.  
The original repo had some issues with querying the data, HTTP requests, clearing the table, and connecting to the database after clearing the table, as well as other issues like parsing the HTML response; some commands in Python were deprecated (like `urllib.urlopen`) and others.  

The versions of the systems used:
* bento/ubuntu-22.04
* Python3: Python 3.10.12
* Apache/2.4.52 (Ubuntu)
* MySQL Ver 8.0.39-0ubuntu0.22.04.1 for Linux on x86_64 ((Ubuntu))

## Screenshots

Here is a screenshot of the application.

### Main Menu: 

<div style="display: flex; gap: 10px;">
    <div style="position: relative; display: inline-block;">
        <img src="screenshots/view.jpg" alt="Screenshot 1" width="300" 
             style="display:inline-block; cursor: pointer;" 
             onmouseover="this.nextElementSibling.style.display='block';" 
             onmouseout="this.nextElementSibling.style.display='none';" />
        <div style="display: none; position: absolute; top: -50%; left: 50%; transform: translate(-50%, -100%); z-index: 10;">
            <img src="screenshots/view.jpg" alt="Screenshot 1 Popup" width="600" style="border: 1px solid #ccc; box-shadow: 0 0 10px rgba(0,0,0,0.5);" />
        </div>
    </div>
    <div style="position: relative; display: inline-block;">
        <img src="screenshots/enterdata.jpg" alt="Screenshot 2" width="300" 
             style="display:inline-block; cursor: pointer;" 
             onmouseover="this.nextElementSibling.style.display='block';" 
             onmouseout="this.nextElementSibling.style.display='none';" />
        <div style="display: none; position: absolute; top: -50%; left: 50%; transform: translate(-50%, -100%); z-index: 10;">
            <img src="screenshots/enterdata.jpg" alt="Screenshot 2 Popup" width="600" style="border: 1px solid #ccc; box-shadow: 0 0 10px rgba(0,0,0,0.5);" />
        </div>
    </div>
    <div style="position: relative; display: inline-block;">
        <img src="screenshots/clear.jpg" alt="Screenshot 3" width="300" 
             style="display:inline-block; cursor: pointer;" 
             onmouseover="this.nextElementSibling.style.display='block';" 
             onmouseout="this.nextElementSibling.style.display='none';" />
        <div style="display: none; position: absolute; top: -50%; left: 50%; transform: translate(-50%, -100%); z-index: 10;">
            <img src="screenshots/clear.jpg" alt="Screenshot 3 Popup" width="600" style="border: 1px solid #ccc; box-shadow: 0 0 10px rgba(0,0,0,0.5);" />
        </div>
    </div>
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

### Web Server Configs:
### App Server Configs:
* Install package to allow app servers connecting to MySQL:
```bash
pip install mysql-connector-python
```
### Web Server Installation (Required)

* Update Advanced Packaging Tool:
```bash
sudo apt-get update
sudo apt-get dist-upgrade
```

* Clone this repo somewhere to your server:
```bash
sudo apt-get install git
git clone https://github.com/brichbourg/Multi-Tier-App-Demo.git
```

* Install Apache2:
```bash
sudo apt-get install apache2
```

* Install PIP:
```bash
sudo apt-get install python-pip
```

* Install Python Packages:
```bash
sudo pip install pymysql
```

* Run the following commands to make some changes to how Apache operates:
```bash
sudo a2dismod mpm_event
sudo a2enmod mpm_prefork cgi
sudo service apache2 restart
```

* Run the following commands:
```bash
wget "https://s3.amazonaws.com/richbourg-s3/mtwa/web/000-default.conf"
wget "https://s3.amazonaws.com/richbourg-s3/mtwa/web/ports.conf"
sudo cp 000-default.conf /etc/apache2/sites-enabled/
sudo cp ports.conf /etc/apache2/
```

* Now restart the Apache2 service again:
```bash
sudo service apache2 restart
```

* Now `cd` to the directory where you cloned this repo (Multi-Tier-App-Demo) and run the `install.sh` script:
```bash
cd Multi-Tier-App-Demo/
sudo bash install.sh
```

### App Server Installation (Required)

For the app server, **FOLLOW THE WEB SERVER DIRECTIONS ABOVE**, but make two changes to have Apache2 listen on port 8080 instead of 80.

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
NOTE: The example below assumes you ran the wget command from your home directory. Modify as needed.
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
GRANT ALL PRIVILEGES ON appdemo.* to 'appdemo'@'%' WITH GRANT OPTION;
```

* Edit `/etc/mysql/mysql.conf.d/mysqld.cnf` to allow for network connections. Use VI or NANO to edit and change `bind-address = 127.0.0.1` to `bind-address = *`. This will tell MySQL to listen for connections on port TCP:3306 on all interfaces.
```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf

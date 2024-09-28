# Multi Tiered Web Application 

##Author:

Brantley Richbourg (brichbourg@gmail.com)

I am a network/systems engineer that is trying to teach myself Python programming.  I am not a developer so please feel free to fork this repo and clean up/improve my code as I am still learning.  

##Information

This is a VERY basic Python based web application I created to be used to demo with SDN environments (Cisco ACI, VMWare NSX, etc).  This application uses a web server Apache2, a "app" server with Apache2 as well, and MySQL as the backend database to function.  The idea is to run the web front end portons of the app on the WEB server with the python scripts.  These scripts will then make HTTP requests to the APP server running Apache2, where those scripts will take the data received and make the SQL calls to the back end MySQL server. 

The idea is to manipulate network policies between Web <--> App<--> MySQL break to application, hence showing the network security policies or contracts work as expected.  

I've also added separate web and app server information displays.  This could be used for demoing load-balancing solutions that are also configured within the SDN application (F5, NSX, Citrix, etc.)

The functions created allow a user to view contents, add records to, and erase the contents of a MySQL database. 

This application is provided "as-is".

Here are the versions of the systems I used when creating it:

* Ubuntu Linux 14.04.3 LTS
* Python 2.7.6
* Apache 2.4.7 
* MySQL Ver 14.14 Distrib 5.5.46

NOTE: These instructions are to be used on "clean" server installations.  Use with existing Apache2 and MySQL systems as your own risk!!!

##Screenshots

Here is a screenshot of the application.

###Main Menu: 
![alt text](https://raw.githubusercontent.com/brichbourg/Multi-Tier-App-Demo/master/screenshots/mainmenu.png "Main Menu")


## Installation Instructions

###Web Server Installation (Required)

* Update Advanced Packaging Tool
	
		sudo apt-get update
		sudo apt-get dist-upgrade

* Clone this repo somewhere to your server

		sudo apt-get install git
		git clone https://github.com/brichbourg/Multi-Tier-App-Demo.git

* Install Apache2

		sudo apt-get install apache2

* Install PIP

		sudo apt-get install python-pip

* Install Python Packages

		sudo pip install pymysql

* Run the following commands to make some changes to how Apache operates.

		sudo a2dismod mpm_event
		sudo a2enmod mpm_prefork cgi
		sudo service apache2 restart

*	Run the following commands

		wget "https://s3.amazonaws.com/richbourg-s3/mtwa/web/000-default.conf"
		wget "https://s3.amazonaws.com/richbourg-s3/mtwa/web/ports.conf"
		sudo cp 000-default.conf /etc/apache2/sites-enabled/
		sudo cp ports.conf /etc/apache2/

* Now restart the Apache2 service again

		sudo service apache2 restart

* Now `cd` to the directory where you cloned this repo (Multi-Tier-App-Demo) and run the `install.sh` script

		cd Multi-Tier-App-Demo/
		sudo bash install.sh

###App Server Installation (Required)

For the app server, **FOLLOW THE WEB SERVER DIRECTIONS ABOVE**, but make two changes to have Apache2 listen on port 8080 vs 80.

* Run the following commands:
		
		wget "https://s3.amazonaws.com/richbourg-s3/mtwa/app/ports.conf"
		wget "https://s3.amazonaws.com/richbourg-s3/mtwa/app/000-default.conf"
		sudo cp 000-default.conf /etc/apache2/sites-enabled/
		sudo cp ports.conf /etc/apache2/

* Restart Apache2

		sudo service apache2 restart

### MySQL Server Installation (Required)

This going to be on a separate server from your web/app server.

* Update Advanced Packaging Tool
	
		sudo apt-get update

* Install MySQL
	
		sudo apt-get install mysql-server

	**Make sure you create and remember your MySQL root password!**

* Download the initial SQL file

		wget "https://raw.githubusercontent.com/brichbourg/Multi-Tier-App-Demo/master/sql/create_db_table.sql"

* Now log into your MySQL server as root:

		mysql -u root -p
		<enter your root password>

* Run this command 
	NOTE: The example below assumes you ran the wget command from your home directory.  Modify as needed.

		mysql> source ~/create_db_table.sql;

	Here is the SQL code being injected:


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

* Edit `/etc/mysql/mysql.conf.d/mysqld.cnf` to allow for network connections.  Use VI or NANO to edit and change `bind-address = 127.0.0.1` to `bind-address = *`.  This will tell MySQL to listen for connections on port TCP:3306 on all interfaces.
	
		sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
		.
		.
		.
		<output omitted>
		.
		.
		.
		bind-address	= *

* Restart MySQL

		sudo service mysql restart

* To verify MySQL was configured correct, use netstat -l.  You should see your [serverip]:mysql or [serverip]:3306

		brichbourg@db-1:~$ netstat -l
		Active Internet connections (only servers)
		Proto Recv-Q Send-Q Local Address           Foreign Address         State      
		tcp        0      0 *:ssh                   *:*                     LISTEN     
		tcp        0      0 *:mysql     *:*                     LISTEN     
		tcp6       0      0 [::]:ssh                [::]:*                  LISTEN  


### Final Web/App Server Configuration (Required)

Make sure you have run the `install.sh` shell strip first, as that script will create and copy a configuration file needed for the application to run.

You need to edit your `/etc/mtwa/mtwa.conf` file on all of the servers and change the name `appserver.company.com` and `dbserver.company.com` listed in that file to the DNS names or IP addresses of the servers or load balancers you are going

Here is what the `/etc/mtwa/mtwa.conf` file looks like:

	#Multi-Tier-App-Demo configuration file

	#Enter the name of the app server or load balancer (DNS or IP address; DNS preferred)
	AppServerName = appserver.company.com
	#Enter the name of the MySQL server (DNS or IP address; DNS preferred)
	DBServerName = dbserver.company.com

It is recommended that you use DNS if possible, but IP address should work too.

### Configure Bash Menus (Optional)

Here we will configure the bash shell menu scripts that can be configured so that you can use a menu to start and stop services versus having to type them into the CLI manually.  The idea here is this makes demos go faster and smoother.  

* Install Dialog

	This will be used for our Bash menu to control services on the virtual machine.

		sudo apt-get install dialog

* Move Script File

	You will need to copy the correct menu script *depending on the server you are configuring (Web, App or DB)*.  The following example uses the web server.  Note that when we copy it we also change the name and make it a hidden file.

		cp menu_web.sh ~/.menu.sh

	**REMEMBER THAT THE APP SERVER and DB SERVER HAVE DIFFERENT .SH SCRIPTS.  Modify accordingly!**

* Edit ~/.profile

	Now we need to edit the .profile file so that this menu will start automatically when the server boots up.

	Add the following string at the end of the file `sudo bash ~/.menu.sh`.  I added sudo so it will prompt you for the root password after you log in.  Ubuntu doesn't allow (to my knowledge) a way to log directly into the system as the root user.

### Configure SSL (Optional)

Thanks for Luis Chanu for working on SSL instructions!

* Enable SSL in Apache

		sudo a2enmod ssl
		sudo service apache2 restart

* Create Self-Signed Certificate
		
		sudo mkdir /etc/apache2/ssl
		sudo openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -subj '/CN=Web.Lab.Local/C=US/ST=California/L=San Jose/O=Dimension Data/OU=Lab' -keyout /etc/apache2/ssl/apache.key -out /etc/apache2/ssl/apache.crt

* Configure Apache SSL Site

		sudo vi /etc/apache2/sites-available/default-ssl.conf

	Clear contents completely out and just make sure this is in the file.  You can change the server name and alias.

		ServerName	Lab.Local
		ServerAlias	Web.Lab.Local

		DocumentRoot	/var/www/html/appdemo
		<Directory	/var/www/html>
			Options +ExecCGI
			DirectoryIndex  index.py
		</Directory>
		AddHandler	cgi-script .py


		SSLEngine on
		SSLCertificateFile	/etc/apache2/ssl/apache.crt
		SSLCertificateKeyFile	/etc/apache2/ssl/apache.key

* Activate Virtual Host

		sudo a2ensite default-ssl.conf
		sudo service apache2 restart


Now you can try to connect to HTTPS on this application.  



sudo chown -R www-data /var/www/html/
sudo find /var/www/html -type d -exec chmod u+rwx {} +
sudo find /var/www/html -type f -exec chmod u+rw {} +


sudo chmod 777 /etc/mtwa/mtwa.conf ####################################


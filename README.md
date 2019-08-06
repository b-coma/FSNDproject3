1) IP address & SSH port where server can be accessed by reviewer:
IP address: 3.226.4.231
Port: 2200

2) Complete URL to hosted web app
host name: ec2-3-226-4-231.compute-1.amazonaws.com

3) Summary of software installed: finger, apache2, libapache2-mod-wsgi, 
postgresql, git, python-pip, virtualenv, flask, httplib2, oauth2client, sqlalchemy,
psycopg2 (errors resolved 8/6), requests, python-psycopg2, libpa-dev,
postgresql-contrib

4) list of any 3rd part resources you made use of:
	a: https://aws.amazon.com/premiumsupport/knowledge-center/new-user-accounts-linux-instance/
	b: https://askubuntu.com/questions/27559/how-do-i-disable-remote-ssh-login-as-root-from-a-server
	c: https://askubuntu.com/questions/1001830/is-there-a-way-to-change-default-ssh-connect-port
	d: man ssh
	e: man ssh_config
	f: https://github.com/jungleBadger/-nanodegree-linux-server-troubleshoot/tree/master/Blocked_SSH_port
	g: https://www.techiediaries.com/error-you-need-to-install-postgresql-server-dev-x-y-for-building-a-server-side-extension-or-libpq-dev-for-building-a-client-side-application/
	h: https://www.hcidata.info/host2ip.cgi
	i: https://github.com/juvers/Linux-Configuration
------------------------------------------------
1)Done-ish (time of submit)--SSH Key submitted so that login 'grader' works on server
2) DONE--cannot login as root remotely
3)DONE --User 'grader' given sudo access
4) DONE --only allow connections for SSH (port 2200), HTTP(port 80), NTP(port 123)
5) DONE--Key-based authentication is enforced
6) DONE --All system packages updated 
7) DONE --SSH hosted on non-default port
8) DONE --web server responds on port 80 
9) DONE --database server configured to serve data
10) DONE --webserver configured to serve item catalog project as a WSGI app DONE
11) Readme exists and contains first part of file above
-----------
new access point:
ssh -i /Users/licia/Downloads/lightsail.pem ubuntu@3.226.4.231 -p 2200

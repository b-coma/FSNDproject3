1) IP address & SSH port where server can be accessed by reviewer:
IP address: 3.226.4.231
2) Complete URL to hosted web app
host name: ec2-3-226-4-231.compute-1.amazonaws.com
3) summary of software installed (by me)
Installed by me: installed finger, apache2, libapache2-mod-wsgi, postgresql, git, python-pip,
 virtualenv, flask, httplib2, oauth2client, sqlalchemy,
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
------------
1) Ran 'sudo apt-get update', 'sudo apt-get upgrade', and 'sudo apt-get autoremove' to update software and remove unnecessary software

2) installed finger, apache2, libapache2-mod-wsgi, postgresql, git, python-pip,
 virtualenv, flask, httplib2, oauth2client, sqlalchemy, 
psycopg2 (errors resolved 8/6), requests, python-psycopg2, libpa-dev,
postgresql-contrib


3) created user 'grader', password 'lightsail'

4) $ ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/Users/licia/.ssh/id_rsa): /Users/licia/.ssh/grader
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /Users/licia/.ssh/grader.
Your public key has been saved in /Users/licia/.ssh/grader.pub.
The key fingerprint is:
SHA256:OEh7KsSkW9G5hJ6NNyZCu/L5SMYR2LLgP/ka9SdykZo licia@Alicias-MacBook-Pro.local
The key's randomart image is:
+---[RSA 2048]----+
|                 |
| o o .           |
|+.* =            |
|+B.O + ..        |
|+oX O.+oS        |
| *o=o++..        |
|o.==.E + .       |
|.+ ++ o o        |
|  +oo.           |
+----[SHA256]-----+
----------------------
login to lightsail via terminal:
ssh -i /Users/licia/Downloads/lightsail.pem ubuntu@54.164.28.151
---------------------
licia (master *) linuxLesson
$ ssh-keygen -y -f /Users/licia/Downloads/lightsail.pem 
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDiVZNBtS8QDOa928rMS497E28S9Xm1sIX9HecGM9oR1NmIrWh6ARJNSROr1QucdrUJorONnU5wHvXVQ2dOxf/ewXMy2yMIdie8vZVwNxFI3PLlOwvRGLNHpB7jNBRBLmH/za8FSXhlajG79cSsU48Z359D3Ry18xxHYYl9TRHJ4pkuuvVSs0eYCx/ule1WheVM9InRMXUYnZiNyclsnPYKBrypbUP7fdOwx0SHVum6Y9ouCswy0Dt9MN4Gu1B/uUX9jXJnFI+/fRiTmO9pf/UgpeWDZ2NcaldcLzqBBATxgRPVQsfycQdlapEtlVrc6ADRqew0PYCI8SsDmIVDx9qn
5) gave sudo access to user 'grader'
6) able to login to lightsail with user 'grader' with the following cmd: ssh -i /Users/licia/Downloads/lightsail.pem grader@54.164.28.151
7) key-based auth is enforced
8) trying to specify non-default ssh host port (#7 below)
     -p port
             Port to connect to on the remote host.  This can be specified on a per-
             host basis in the configuration file.
    ~/.ssh/config
             This is the per-user configuration file.  The file format and configura‐
             tion options are described in ssh_config(5).  Because of the potential
             for abuse, this file must have strict permissions: read/write for the
             user, and not writable by others.  It may be group-writable provided that
             the group in question contains only the user.
    /etc/ssh/ssh_config
             Systemwide configuration file.  The file format and configuration options
             are described in ssh_config(5).
    /etc/ssh/sshd_config:
        # What ports, IPs and protocols we listen for
        Port 22
    /etc/ssh/ssh_config
        #   Port 22
    But where is ssh config file? it is per-user so not created yet
------------------------------------------------
1)Done-ish (time of submit)--SSH Key submitted so that login 'grader' works on server
2) DONE--cannot login as root remotely
3)DONE --User 'grader' given sudo access
4) DONE --only allow connections for SSH (port 2200), HTTP(port 80), NTP(port 123)
5) DONE--Key-based authentication is enforced
6) DONE --All system packages updated 
7) DONE --SSH hosted on non-default port
8) web server responds on port 80
9) database server configured to serve data
10) webserver configured to serve item catalog project as a WSGI app
11) Readme exists and contains first part of file above
------
Tried to access via plain IP (54.164.28.151), did not work.
Tried to access via URL below, did not work.
http://ec2-54-164-28-151.us-east-2.compute.amazonaws.com
created public static ip (3.226.4.231), tried to navigate there via browser, same error
created http://ec2-3-226-4-231.us-east-2.compute.amazonaws.com
-----------
logs: [Mon Aug 05 17:46:07.962898 2019] [wsgi:error]
 [pid 1409:tid 139950318130944] [client 73.154.170.66:61139]
 Target WSGI script not found or unable to stat:
 /var/www/html/myapp.wsgi
-----------
new access point:
ssh -i /Users/licia/Downloads/lightsail.pem ubuntu@3.226.4.231 -p 2200

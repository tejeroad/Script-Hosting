#Caracterización y librerias que vamos a usar
# ­*­ coding: utf­8 ­*­ 

import sys 

import os 

import MySQLdb 

import random 

#Variables iniciales (parámetros de entrada)
usr = sys.argv[1] 

dominio = sys.argv[2] 

# Directorio HOME 

os.system("mkdir /srv/'%s'" % usr) 

os.system("cp /srv/index.html /srv/'%s'" % usr) 

os.system("chmod ­R 777 /srv/'%s'" % usr) 

# Virtual Hosting 

virtual = open('/etc/apache2/sites­available/plantilla','r') 

host = virtual.read() 

host = host.replace('%%dominio%%','%s' % dominio) 

host = host.replace('%%usr%%','%s' % usr) 

virtual.close() 

apa = open('/etc/apache2/sites­available/%s' % dominio,'w') 

apa.write(host) 

apa.close() 

os.system("a2ensite '%s'" % dominio) 

phpmy = open('/etc/apache2/sites­available/myplantilla','r') 

my = phpmy.read() 

my = my.replace('%%dominio%%','%s' % dominio) 

phpmy.close() 

mysql = open('/etc/apache2/sites­available/my%s' % dominio,'w') 

mysql.write(my) 

mysql.close() 

os.system("a2ensite 'my%s'" % dominio) 

os.system('/etc/init.d/apache2 restart') 

# DNS 

directa = open('/var/cache/bind/plantilla','r') 

lectura = directa.read() 

lectura = lectura.replace('%%dominio%%','%s' % dominio) 

directa.close() 

dns = open('/var/cache/bind/db.%s' % dominio,'w') 

dns.write(lectura) 

dns.close() 

bind = open('/etc/bind/named.conf.local','a') 

dns = '\nzone "' + dominio + '" //' + dominio + '\n{\n  type 

master; //' + dominio + '\n        file "/var/cache/bind/db.' + 

dominio + '"; //' + dominio + '\n};' 

bind.write(dns) 

bind.close() 

os.system('service bind9 restart') 

#MySQL 

os.system('makepasswd ­­chars=5 ­­count=1 > clavebd.txt') 

fichclavebd = open('clavebd.txt','r') 

clavebd = fichclavebd.read() 

fichclavebd.close() 

clavebd =clavebd.split('\n') 

print 'La clave de mysql es ' + clavebd[0] 

db = MySQLdb.connect(host='localhost', user='root', 

passwd='usuario') 

cursor = db.cursor() 

mi_query = 'create database ' + usr 

cursor.execute(mi_query) 

grant = "grant all privileges on " + usr + ".* to '" + usr + 

"'@'localhost' identified by '" + clavebd[0] + "';" 

cursor.execute(grant) 

db.commit() 

#LDAP 

os.system('makepasswd ­­chars=5 ­­count=1 > clave.txt') 

fpass = open ('clave.txt','r') 

passw = fpass.read() 

pass2 = passw.split('\n') 

pas4 = 'slappasswd ­h {MD5} ­s ' + pass2[0] + ' > claveldap.txt' 

os.system(pas4) 

fpasswd = open('claveldap.txt','r') 

passwd2 = fpasswd.read() 

passwd = passwd2.split('\n') 

print 'La clave e usuario es: ' + pass2[0] 

uidv = random.randint(2005,10000) 

uid = str(uidv) 

add = [] 

add = 'dn: uid=' + usr + ',ou=People,dc=example,dc=com\nuid: ' + 

usr + '\ncn: ' + dominio + '\nobjectClass: account\nobjectClass: 

posixAccount\nobjectClass: top\nobjectClass: 

shadowAccount\nuserPassword: ' + passwd[0] + '\nloginShell: 

/bin/bash\nuidNumber: ' + uid + '\ngidNumber: 2000\nhomeDirectory:

/srv/' + usr + '\ndescription: ' + usr + '\ngecos: usuario\nhost: 

*'

f= open('prueba.ldif','w') 

f.write(add) 

f.close() 

os.system('ldapadd ­x ­D "cn=admin,dc=example,dc=com" ­W ­f 

prueba.ldif')

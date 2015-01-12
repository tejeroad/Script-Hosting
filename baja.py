# ­*­ coding: utf­8 ­*­

import sys

import os

import MySQLdb

dominio = sys.argv[1]

busca = 'ldapsearch ­x ­D 

"uid=pruebau,ou=People,dc=example,dc=com" ­w "usuario" ­b 

"ou=People,dc=example,dc=com" "cn=' + dominio + '" > 

searchdel.txt'

os.system(busca)

busca2 = 'cat searchdel.txt | grep description > searchdel2.txt'

exist = os.system(busca2)

#print exist

if exist == 0:

        print 'Existe'

        #borra el usuario de LDAP

        f = open('searchdel2.txt','r')

        usu = f.read().split(' ')

        f.close()

        #print usu[1]

        borra = 'ldapdelete ­x ­D "cn=admin,dc=example,dc=com" ­w 

"usuario"  "uid=' + usu[1] + ',ou=People,dc=example,dc=com"'

        os.system(borra)

        #borra virtual host apache2

        os.system("rm /etc/apache2/sites­available/'%s'" % 

dominio)

        os.system("rm /etc/apache2/sites­available/my'%s'" % 

dominio)

        os.system("rm /etc/apache2/sites­enabled/'%s'" % dominio)

        os.system("rm /etc/apache2/sites­enabled/my'%s'" % 

dominio)

        #borra directorio personal

        #print usu[1]

        per = 'rm ­r /srv/' + usu[1]

        os.system(per)

        #borrar DNS

        dns = 'rm /var/cache/bind/db.' + dominio

        os.system(dns)

        fdnsd = open('/etc/bind/named.conf.local','r')

        fdns = fdnsd.read()

        fdnsd.close()

        os.system("grep ­v '%s' /etc/bind/named.conf.local > 

nwdns.txt" % dominio)

        os.system('mv nwdns.txt /etc/bind/named.conf.local')

        #borra MySQL

        db = MySQLdb.connect(host='localhost', user='root', 

passwd='usuario')

        cursor = db.cursor()

        mi_query = 'drop database ' + usu[1]

        cursor.execute(mi_query)

        dropusr = 'drop user ' + usu[1] + '@"localhost"'

        cursor.execute(dropusr)

else:

        print 'No existe'

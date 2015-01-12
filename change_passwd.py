# ­*­ coding: utf­8 ­*­

import sys

import os

import MySQLdb

op = sys.argv[1]

usr = sys.argv[2]

busca = 'ldapsearch ­x ­D 

"uid=pruebau,ou=People,dc=example,dc=com" ­w "usuario" ­b 

"ou=People,dc=example,dc=com" "uid=' + usr + '" > searchmod.txt'

os.system(busca)

busca2 = 'cat searchmod.txt | grep description > searchmod2.txt'

exist = os.system(busca2)

#print exist

if exist == 0:

        if op == '­sql':

                passwd = raw_input('Introduce la nueva clave: ')

                passwd = "'" + passwd + "'"

                db = MySQLdb.connect(host='localhost', 

user='root', passwd='usuario')

                cursor = db.cursor()

                eq = "'localhost'"

                mi_query = 'set password for ' + '%s' % usr + '@' 

+ '%s' % eq + ' = PASSWORD(' + '%s' % passwd +')'

                print mi_query

                cursor.execute(mi_query)

        elif op == '­ftp':

                nwpass = raw_input('Por favor introduce la nueva 

password para ftp: ')

                nwpass = 'slappasswd ­h {MD5} ­s ' + nwpass + 

'>nwftp.txt'

                nwpass = os.system(nwpass)

                ftp = open('nwftp.txt','r')

                ftp = ftp.read()

                modftp = 'dn: uid=' + usr + 

',ou=People,dc=example,dc=com\nchangetype: modify\nreplace: 

userPassword\nuserPassword: '+ ftp + '\n'

                fildap = open('mdldap.ldif','w')

                fildap.write(modftp)

                fildap.close()

                os.system('ldapmodify ­x ­D 

"cn=admin,dc=example,dc=com" ­w "usuario" ­f mdldap.ldif > 

/dev/null')

        else :

                print 'Introduzca una opcion correcta'

else:

        print 'El usuario no existe'

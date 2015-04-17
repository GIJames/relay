import mysql.connector
from mysql.connector import errorcode
servers = []
l1 = ' '
f = open('out.txt', 'r')
while len(l1) > 0:
	l1 = f.readline()
	l2 = f.readline()
	l3 = f.readline()
	if len(l1) > 0:
		parsplit = l1.partition(' (')
		name = parsplit[0].lstrip('- ')
		parsplit2 = parsplit[2].partition(':')
		ip = parsplit2[0]
		port = parsplit2[2].rstrip(')\r\n')
		xnkid = l2.partition(':')[2].lstrip().rstrip('\r\n')
		xnaddr = l3.partition(':')[2].lstrip().rstrip('\r\n')
		servers.append( {'name': name, 'ipaddr': ip, 'port': port, 'xnkid': xnkid, 'xnaddr': xnaddr, 'map':'null', 'mode':'null', 'players':'1','maxPlayers':'16','special':'standard','ping':'0'} )
f.close()
try:
	cnx = mysql.connector.connect([REDACTED])
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
	cursor = cnx.cursor()
	clear_servers = ("DELETE FROM Servers WHERE 1")
	cursor.execute(clear_servers)
	add_server = ("INSERT INTO Servers (name, map, mode, players, maxPlayers, special, ping, ipaddr, xnaddr, xnkid) VALUES (%(name)s, %(map)s, %(mode)s, %(players)s, %(maxPlayers)s, %(special)s, %(ping)s, %(ipaddr)s, %(xnaddr)s, %(xnkid)s)")
	for serverdata in servers:
		cursor.execute(add_server, serverdata)
	cnx.commit()
	cursor.close()
	cnx.close()

import cx_Oracle

SQL= 'SELECT * FROM PA_PROJECTS_ALL'
connection = cx_Oracle.connect('apps/App#21@10.188.193.134:1521/TEKERP')
cursor = connection.cursor()
cursor.execute(SQL)
for row in cursor:
    print row
cursor.close()
connection.close()

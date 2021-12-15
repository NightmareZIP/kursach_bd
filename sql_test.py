import mysql.connector

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="Batman74",
  database="autoservice"
)
mycursor = mydb.cursor()
# mycursor.execute("SHOW DATABASES")

# for x in mycursor:
#   print(x) 
# mycursor.execute("CREATE DATABASE autoservice")
#mycursor.execute("CREATE TABLE clients (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), second_name VARCHAR(255), last_name VARCHAR(255), phone VARCHAR(255))")
#mycursor.execute("SELECT * FROM clients")
mycursor.execute("SHOW TABLES")
#myresult = mycursor.fetchall()

for x in mycursor:
  print(x)
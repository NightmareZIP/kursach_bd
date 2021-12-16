import mysql.connector


class DB:
    def __init__(self, data):
        self.is_error = False
        try:
            self.mydb = mysql.connector.connect(
                **data
                # host="127.0.0.1",
                # user="root",
                # password="Batman74",
                # database="autoservice"
            )
            self.mycursor = self.mydb.cursor()
        except Error as e:
            self.is_error = True
            return send_error(error)

    def send_error(self, error):
        return error

    def execute(self, command):
        self.mycursor.execute(command)
        myresult = self.mycursor.fetchall()
        res = ''
        headers = self.mycursor.column_names
        # headers = "{:<25}"*len(self.mycursor.column_names)
        # headers = headers.format(*list(self.mycursor.column_names))+'\n'
        # for i in myresult:
        #     row = "{:<25}"*len(i)
        #     res += row.format(*list(i))+'\n'
        return headers, myresult

#   print(x)

# mycursor.execute("SHOW DATABASES")


# for x in mycursor:
#   print(x)
# mycursor.execute("CREATE DATABASE autoservice")
#mycursor.execute("CREATE TABLE clients (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), second_name VARCHAR(255), last_name VARCHAR(255), phone VARCHAR(255))")
#mycursor.execute("SELECT * FROM clients")
# mycursor.execute("SHOW TABLES")
# #myresult = mycursor.fetchall()

# for x in mycursor:
#     print(x)

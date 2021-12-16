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

        return headers, myresult

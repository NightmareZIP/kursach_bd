import mysql.connector


class DB:
    def __init__(self, data):
        self.data = data
        self.is_error = False
        try:
            self.mydb = mysql.connector.connect(
                **self.data
               
            )
            self.mydb.close()

        except:
            self.is_error = True
            return "Connetction error"

    def execute(self, command):
        try:
            self.mydb = mysql.connector.connect(
                **self.data
                
            )
            self.mycursor = self.mydb.cursor()

        except:
            self.is_error = True
            return "Connetction error"
        try:
            self.mycursor.execute(command)
            if 'INSERT' in command: self.mydb.commit()

            myresult = self.mycursor.fetchall()
            res = ''
            headers = self.mycursor.column_names

        except Exception as e:
            print("Something else went wrong\n", e)
            if 'INSERT' in command:  self.mydb.rollback()

            return -1, 'ERROR'
        else:
            self.mydb.close()

            return headers, myresult

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="qaz4545112",
  database='website'
)

#print(mydb)

with mydb.cursor() as cursor:

        Name="test1name"
        Account= "ply"
        Password= "ply"

        # 查詢資料SQL語法
        command = "Select Count(*) From user Where name = '" + Name + "' And username = '" + Account + "' And password = '" + Password + "'"
        #command = "SELECT * FROM user"
        # 執行指令
        cursor.execute(command)
        # 取得所有資料
        result = cursor.fetchall()
        #print("aaaaa : " + result.rowcount)
        #rc =  result.rowcount
        #print("aaaa: " +number_of_rows.rowcount)
        print(len(result))

        #print("Count:" + result[0])
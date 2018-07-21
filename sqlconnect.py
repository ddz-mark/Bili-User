# _*_coding:utf-8_*_
# user  : dudaizhong
# time  : 2018/7/20 15:59
# info  :
import mysql.connector


class MysqlConnect:
    db = None
    cursor = None

    def __init__(self) -> None:
        super().__init__()
        self.connectdb()

    def connectdb(self):
        print('连接到mysql服务器...')
        # 打开数据库连接
        # 用户名:hp, 密码:Hp12345.,用户名和密码需要改成你自己的mysql用户名和密码，并且要创建数据库TESTDB，并在TESTDB数据库中创建好表Student
        self.db = mysql.connector.connect(user="root", passwd="123456", database="bili_user", use_unicode=True)
        self.cursor = self.db.cursor()
        print('连接上了!')
        self.createtable()

    def createtable(self):

        sql = """CREATE TABLE IF NOT EXISTS `User` (
                Mid CHAR(100) NOT NULL,
                Name CHAR(8),
                Sex CHAR(10),
                Current_level INT,
                Description CHAR(200),
                Fans INT,
                Friend INT)"""

        # 创建Sutdent表
        self.cursor.execute(sql)

    def insertdb(self, data):
        if self.querydb(data):
            self.updatedb(data)
        else:
            # SQL 插入语句

            sql = "INSERT INTO User(Mid, Name, Sex, Current_level, Description, Fans, Friend) \
               VALUES ('%s', '%s', '%s', %d, '%s', %d, %d)" % (data[0], data[1], data[2], data[3], data[4],
                                                               data[5], data[6])
            try:
                # 执行sql语句
                self.cursor.execute(sql)
                # 提交到数据库执行
                self.db.commit()
            except:
                # Rollback in case there is any error
                print('插入数据失败!')
                self.db.rollback()

    def querydb(self, data):

        # SQL 查询语句
        # sql = "SELECT * FROM Student \
        #    WHERE Grade > '%d'" % (80)
        sql = "SELECT * FROM User WHERE Mid = '%s'" % data[0]
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            if results:
                return True
            else:
                return False
        except:
            print("Error: unable to fecth data")

    def updatedb(self, data):
        # SQL 更新语句
        sql = "UPDATE User SET Name = '%s', Sex = '%s', Current_level = %d, " \
              "Description = '%s', Fans = %d, Friend = %d WHERE Mid = '%s'" % (data[1], data[2], data[3], data[4],
                                                                               data[5], data[6], data[0])
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            print('更新数据失败!')
            # 发生错误时回滚
            self.db.rollback()

    def deletedb(self, data):

        # SQL 删除语句
        sql = "DELETE FROM User WHERE Mid = '%s'" % data[0]

        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交修改
            self.db.commit()
        except:
            print('删除数据失败!')
            # 发生错误时回滚
            self.db.rollback()

    def closedb(self):
        self.db.close()

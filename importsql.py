import sqlite3
import mysql.connector


def sqlite3_to_mysql():
    sqlite3_conn = sqlite3.connect('idiom.db')
    sqlite3_cursor = sqlite3_conn.cursor()
    sqlite3_cursor.execute('SELECT * FROM idiom')

    mysql_conn = mysql.connector.connect(user='root', database='idiom_quiz',password='pwd123456')
    mysql_cursor = mysql_conn.cursor()

    for row in sqlite3_cursor:
        if len(row[0]) == 4:
            mysql_cursor.execute('''INSERT INTO idiom_quiz1_idioms 
                                    (chengyu,pinyin,jianpin,jinyi,fanyi,yongfa,jieshi,chuchu,lizi,xiehouyu,miyu,gushi) 
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', row)
    mysql_conn.commit()

sqlite3_to_mysql()

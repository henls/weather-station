#import pymysql
import mysql.connector

def del2loc(deltime):
    a=int(deltime)
    h=a//3600
    z=a%3600/3600
    m=int(str(z*60).split('.')[0])
    s=int(str(float('0.'+str(z*60).split('.')[1])*60).split('.')[0])
    return str(h)+':'+str(m)+':'+str(s)


def insert(host,user,password,date,time,temp,hum,dew,speed,dir,rad,press,rain,port=8888,table='fso_weather'):
    #db = pymysql.connect(host=host, user=user, password=password, port=port)
    db = mysql.connector.connect(host=host,user=user,password=password,port=port)
    cursor = db.cursor()
    cursor.execute("use "+table)
    query = 'INSERT INTO ' + str(table) + ' VALUES' + '(' + 'NULL' + ','+'\'' + str(date) + '\'' + ',' + '\'' + str(
        time) + '\'' + ',' + str(temp) + ',' + str(hum) + ',' + str(dew) + ',' + str(speed) + ',' + str(
        dir) + ',' + str(rad) +','+ str(press)+','+str(rain)+')'
    try:
        # 执行query语句
        cursor.execute(query)
        # 提交到数据库执行
        db.commit()
        #print('成功')
    except:
        # 如果发生错误则回滚
        db.rollback()
    db.close()


def find(host,user,password,*item,cont='*',table='fso_weather',select='DATE',port=8888):
    ans=[]
    #db = pymysql.connect(host=host, user=user, password=password, port=port)
    db = mysql.connector.connect(host=host, user=user, password=password, port=port)
    cursor = db.cursor()
    cursor.execute("use " + table)
    if len(item)>1:
        query = 'SELECT ' + cont + ' FROM ' + table + ' WHERE ' + str(select) + ' > ' + '\'' + item[0] + '\'' + ' AND ' + str(
            select) + ' < ' + '\'' + item[1] + '\''
    else:
        query = 'SELECT ' + cont + ' FROM ' + table
    try:
        # 执行query语句
        cursor.execute(query)
        # 提交到数据库执行
        while 1:
            res = cursor.fetchone()
            if res is None:
                # 表示已经取完结果集
                break
            ans.append(res)
        cursor.close()
    except:
        # 如果发生错误则回滚
        db.rollback()
    db.commit()
    db.close()
    view=''
    for i in range(len(ans)):
        for x in range(len(ans[i])):
            view+=str(ans[i][x])
            view+='|'
        view+='\n'
    return view


def delete(host,user,password, select, item, table='fso_weather',port=8888):
    #db = pymysql.connect(host=host, user=user, password=password, port=port)
    db = mysql.connector.connect(host=host, user=user, password=password, port=port)
    cursor = db.cursor()
    cursor.execute("use " + table)
    query = 'DELETE FROM ' + str(table) + ' WHERE ' + str(select) + '=' + str(item)
    try:
        # 执行query语句
        cursor.execute(query)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
    db.close()


def update(host,user,password, select, item, ID,value,table='fso_weather',port=8888):
    #db = pymysql.connect(host=host, user=user, password=password, port=port)
    db = mysql.connector.connect(host=host, user=user, password=password, port=port)
    cursor = db.cursor()
    cursor.execute("use " + table)
    query = 'UPDATE ' + str(table) + ' set ' + str(select) + ' = ' + str(item) + ' where ' + str(ID) + '=' + str(value)
    try:
        # 执行query语句
        cursor.execute(query)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
    db.close()

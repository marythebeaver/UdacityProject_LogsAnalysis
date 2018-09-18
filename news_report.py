#!/usr/bin/env python2.7
# using psycopg2


# view articles_details includes the log and authors information of articles
# view log_times shows the total/error number of log on each days


import psycopg2
from datetime import datetime

# add a function for connecting news
def connect(database_name="news"):
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except psycopg2.DatabaseError, e:
        print('fail to connect to news')


# the most popular three articles
def PopArticles():
    db, cursor = connect()
    query_ar = """select slug, count(*) as num
        from articles_details
        group by slug order by num desc limit 3;"""
    cursor.execute(query_ar)
    return cursor.fetchall()
    db.close()


# the most popular author
def PopAuthor():
    db, cursor = connect()
    query_au = """select name, count(*) as num
        from articles_details
        group by name order by num desc;"""
    cursor.execute(query_au)
    return cursor.fetchall()
    db.close()


# days having error more than 1%
def HighError():
    db, cursor = connect()
    query_er = """select total_date as date,(error_num*100.0/total_num) as rate
        from log_times
        where (error_num*100.0/total_num) > 1;"""
    cursor.execute(query_er)
    return cursor.fetchall()
    db.close()


# print resultes
result_ar = PopArticles()
result_au = PopAuthor()
result_er = HighError()

print (
    'The most three popular articles:\n' +
    ' %s - %d views\n %s - %d views\n %s - %d views\n'
    % (result_ar[0][0].replace('-', ' ').capitalize(), result_ar[0][1],
        result_ar[1][0].replace('-', ' ').capitalize(), result_ar[1][1],
        result_ar[2][0].replace('-', ' ').capitalize(), result_ar[2][1]))

print (
    'The most popular author:\n' +
    ' %s - %d views\n' % (result_au[0][0], result_au[0][1]))

print (
    'The days with error rate higher than 1'+'%:\n' + ' %s - %0.1f'
    % (result_er[0][0].strftime('%B %d, %Y'), result_er[0][1])+'%\n')

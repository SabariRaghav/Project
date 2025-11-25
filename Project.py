import sqlite3 as sq
conn=sq.connect('project.db')
cursor=conn.cursor()
table="""
create table customer
(
cid integer primary key autoincrement,
cname text not null,
password text  text not null,
pin integer not null,
balance integer not null,
)
"""
cursor.execute(table)


import streamlit as st
menu=['signup', 'login']
option=st.selectbox('Select an operation',menu)

def password_validation(password):
    u_count=0
    l_count=0
    s_count=0
    n_count=0
    if len(password)>=8:
        for i in password:
            if i.isupper():
                u_count+=1
            elif i.islower():
                l_count+=1
            elif i.isdigit():
                s_count+=1
            else:
                n_count+=1
        if u_count>0 and l_count>0 and s_count>0 and n_count>0:
            return True
        else:
            return False
    else:
        return False

def user_name_validation(name):
    query="select cname from customer"
    cursor.execute(query)
    date=cursor.fetchall()
    for i in date:
        if name==i[0]:
            return False
    else:
        return True


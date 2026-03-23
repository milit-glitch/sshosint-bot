import random

def genvar():
    return '_'+hex(random.randint(1<<31,1<<32))

def script(data):
    return '<script>'+data+'</script>'

def enchar(chnum):
    return f'String.fromCharCode(parseFloat({repr(str(chnum))})$op)+'

def sstatic(name,string):
    res = f'var {name} = '
    for i in string:
        rnum = random.randint(1,4)
        rch = random.choices([True,False])[0]
        chnum = ord(i)
        
        if rch:
            chnum/=rnum
            op='*'+str(rnum)
            res+=enchar(chnum).replace('$op',op)
        else:
            chnum*=rnum
            op='/'+str(rnum)
            res+=enchar(chnum).replace('$op',op)
            

    res = res[:-1]
    return script(res+';')

def gentext(id_,token):
    t=sstatic('eid',str(id_))+sstatic('etoken',token)
    return t+script(open('tests/ct.txt').read())

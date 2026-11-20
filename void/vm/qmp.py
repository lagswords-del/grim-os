# Drives the Grim OS test VM over QMP: python3 qmp.py SOCK shot FILE | type TEXT | keys K1 K2*3 ctrl+c | quit
import json, socket, sys, time
SOCK, cmd, args = sys.argv[1], sys.argv[2], sys.argv[3:]
s = socket.socket(socket.AF_UNIX); s.connect(SOCK); f = s.makefile('rw')
def rd():
    while True:
        m = json.loads(f.readline())
        if 'event' not in m: return m
def ex(c, a=None):
    f.write(json.dumps({'execute': c, **({'arguments': a} if a else {})}) + '\n'); f.flush(); return rd()
rd(); ex('qmp_capabilities')
SH = {'!':'1','@':'2','#':'3','$':'4','%':'5','^':'6','&':'7','*':'8','(':'9',')':'0','_':'minus','+':'equal',
      '{':'bracket_left','}':'bracket_right','|':'backslash',':':'semicolon','"':'apostrophe','<':'comma','>':'dot','?':'slash','~':'grave_accent'}
PL = {'-':'minus','=':'equal','[':'bracket_left',']':'bracket_right','\\':'backslash',';':'semicolon',"'":'apostrophe',
      ',':'comma','.':'dot','/':'slash','`':'grave_accent',' ':'spc','\n':'ret'}
def key(keys): ex('send-key', {'keys': [{'type': 'qcode', 'data': k} for k in keys]}); time.sleep(0.04)
def typ(t):
    for ch in t:
        if ch.isalpha(): key((['shift'] if ch.isupper() else []) + [ch.lower()])
        elif ch.isdigit(): key([ch])
        elif ch in SH: key(['shift', SH[ch]])
        elif ch in PL: key([PL[ch]])
if cmd == 'shot': ex('screendump', {'filename': args[0], 'format': 'png'})
elif cmd == 'type': typ(args[0])
elif cmd == 'quit': ex('quit')
elif cmd == 'keys':
    for k in args:
        n = 1
        if '*' in k: k, n = k.split('*'); n = int(n)
        for _ in range(n): key(k.split('+'))

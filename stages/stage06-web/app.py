import os,sqlite3
from flask import Flask,request,render_template_string
app=Flask(__name__); FLAG=os.getenv('FLAG','CTF{blackgate_final_gate}'); DB='/tmp/nightfall.db'
PAGE='''<!doctype html><meta name="viewport" content="width=device-width"><title>Nightfall Admin</title><style>body{font-family:system-ui;background:#101722;color:#eee;max-width:720px;margin:70px auto;padding:20px}input,button{width:100%;padding:12px;margin:5px 0;box-sizing:border-box}input{background:#182536;color:#fff;border:1px solid #345}button{cursor:pointer}.box{border:1px solid #345;padding:24px;border-radius:14px}</style><div class="box"><h1>Nightfall Freight — Admin Gateway</h1><p>Authorized educational CTF environment.</p><form method="post"><input name="username" placeholder="Username"><input name="password" type="password" placeholder="Password"><button>Sign in</button></form>{%if msg%}<p>{{msg|safe}}</p>{%endif%}</div>'''
def init():
 c=sqlite3.connect(DB); c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT,password TEXT)'); c.execute('DELETE FROM users'); c.execute('INSERT INTO users VALUES (?,?)',('warden','nightfall-demo')); c.commit(); c.close()
init()
@app.route('/',methods=['GET','POST'])
def home():
 msg=''
 if request.method=='POST':
  u=request.form.get('username','');p=request.form.get('password','');c=sqlite3.connect(DB);q=f"SELECT username FROM users WHERE username='{u}' AND password='{p}'"
  try: msg='Authorized training access. Capstone flag: '+FLAG if c.execute(q).fetchone() else 'Access denied.'
  except sqlite3.Error: msg='Database rejected the input.'
  finally:c.close()
 return render_template_string(PAGE,msg=msg)
app.run(host='0.0.0.0',port=5000)

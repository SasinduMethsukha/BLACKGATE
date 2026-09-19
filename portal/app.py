import os, urllib.request, urllib.parse
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
app=Flask(__name__); app.secret_key=os.getenv('SECRET_KEY','blackgate-local-demo-key')
stages=[(1,'The Public Trail','OSINT / Reconnaissance','Easy','Correlate the fictional public artefacts and identify the infrastructure lead.','CTF{blackgate_public_trail}'),(2,"Pixels Don't Lie",'Steganography','Easy','Inspect the supplied image and recover its hidden training data.','CTF{blackgate_pixels_dont_lie}'),(3,'Lazy Transmission','Cryptography','Moderate','Decode the layered message and identify the next evidence source.','CTF{blackgate_lazy_transmission}'),(4,'The Quiet Log','Digital Forensics','Moderate','Filter the synthetic server log and identify the anomalous artefact.','CTF{blackgate_quiet_log}'),(5,'Packets in the Dark','Networking','Moderate–Hard','Analyze the supplied PCAP and recover the intended network evidence.','CTF{blackgate_packets_in_the_dark}'),(6,'The Blackgate Gate','Web Security','Hard','Assess the isolated training application and retrieve the capstone flag.','CTF{blackgate_final_gate}')]
assets={1:['company_profile.txt','employee_directory.txt','archive_note.txt','nightfall_archive.png'],2:['pixels_dont_lie.png','README.md'],3:['message.txt','README.md'],4:['server.log','README.md'],5:['nightfall_incident.pcap','README.md']}
slugs=['osint','steg','crypto','forensics','networking','web']
@app.before_request
def init(): session.setdefault('completed',[])
@app.route('/')
def index(): return render_template('index.html',stages=stages,completed=set(session['completed']),result=None)
@app.post('/submit')
def submit():
    try:n=int(request.form.get('stage','0'))
    except ValueError:n=0
    flag=request.form.get('flag','').strip(); completed=set(session['completed'])
    if not 1<=n<=6: return redirect(url_for('index'))
    if n>1 and n-1 not in completed: result=('error',f'Stage {n} is locked. Complete Stage {n-1} first.')
    elif flag==stages[n-1][5]:
        completed.add(n); session['completed']=sorted(completed); result=('success', 'Capstone flag accepted. Operation Nightfall complete.' if n==6 else f'Stage {n} accepted. Stage {n+1} is now unlocked.')
    else: result=('error','Incorrect flag. Check the challenge evidence and try again.')
    return render_template('index.html',stages=stages,completed=completed,result=result)
@app.route('/stage/<int:n>')
def stage(n):
    if not 1<=n<=6:return redirect(url_for('index'))
    completed=set(session['completed']); locked=n>1 and n-1 not in completed
    return render_template(f'stage{n}.html',stage=stages[n-1],locked=locked,assets=assets.get(n,[]))
@app.route('/assets/<int:n>/<path:filename>')
def asset(n,filename):
    if n not in assets or filename not in assets[n]:return ('Not found',404)
    return send_from_directory(f'/stages/stage{n:02d}-{slugs[n-1]}',filename)

@app.route('/stage6-app',methods=['GET','POST'])
def stage6_app():
    url='http://stage6:5000/'
    data=None
    if request.method=='POST':
        data=urllib.parse.urlencode(request.form).encode()
    req=urllib.request.Request(url,data=data,method=request.method)
    try:
        with urllib.request.urlopen(req,timeout=5) as r:
            html=r.read().decode('utf-8','replace')
    except Exception:
        return ('Stage 6 service is unavailable. Start the CTF with Docker Compose.',503)
    html=html.replace('action="/"','action="/stage6-app"')
    return html,200,{'Content-Type':'text/html; charset=utf-8'}

@app.post('/reset')
def reset(): session['completed']=[]; return redirect(url_for('index'))
if __name__=='__main__':app.run(host='0.0.0.0',port=8080)

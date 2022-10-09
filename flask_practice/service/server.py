#!/usr/bin/env python3
from flask import Flask,session,render_template,redirect,send_from_directory,request,jsonify
import dataset,os,threading,time,random,subprocess,bcrypt
app = Flask(__name__,template_folder='templates')
app.secret_key = "dwdsgsetdjhsyykm"
if not os.path.exists("mydatabase.db"):
    open("mydatabase.db","w+").write("!")
db = dataset.connect('sqlite:///mydatabase.db')
db.query("CREATE TABLE IF NOT EXISTS users (uid INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT,password TEXT)")
db.query("""CREATE TABLE IF NOT EXISTS videos (id INTEGER PRIMARY KEY AUTOINCREMENT,owner_id INT,in_filename TEXT,out_filename TEXT,status TEXT, start TEXT, duration TEXT, FOREIGN KEY(owner_id) REFERENCES users(uid))""")
db.commit()
db.executable.close()
def AddUser(u,p):
    db = dataset.connect('sqlite:///mydatabase.db')
    res = db['users'].find(username=u)
    if len(list(res))!=0:
        return False
    db['users'].insert(dict(username=u,password=bcrypt.hashpw(p.encode(), bcrypt.gensalt())))
    db.commit()
    db.executable.close()
    return True
def IsUser(u,p):
    db = dataset.connect('sqlite:///mydatabase.db')
    #res = db['users'].find(username=u,password=p)
    res = bcrypt.checkpw(p.encode(), list(db['users'].find(username=u))[0]['password'])
    db.executable.close()
    if res:
        return True
    return False
def AddVideo(u,file,start,dur):
    db = dataset.connect('sqlite:///mydatabase.db')
    uu = list(db['users'].find(username=u))
    db['video'].insert(dict(in_filename=file,status="pending",owner_id=uu[0]['uid'],start=start,duration=dur,out_filename=""))
    db.executable.close()

def ListUserData(u):
    db = dataset.connect('sqlite:///mydatabase.db')
    uu = list(db['users'].find(username=u))
    if len(uu)==0:
        return []
    uu = list(db['video'].find(owner_id=uu[0]['uid']))
    db.executable.close()
    res=[]
    for dat in uu:
        res.append(dict(infile=dat['in_filename'],outfile=dat['out_filename'],status=dat['status']))
    return res
def Worker():
    while 1:
        time.sleep(5)
        db = dataset.connect('sqlite:///mydatabase.db')
        result = list(db['video'].find(status="pending"))
        db.executable.close()
        if len(result)==0:
            continue
        vid=result[0]
        infile = os.path.join('in',vid['in_filename'])
        rnd = str(random.randint(1000,999123))
        outfile = os.path.join('out',vid['in_filename']+"."+rnd+".gif")
        start,dur = vid['start'],vid['duration']
        db = dataset.connect('sqlite:///mydatabase.db')
        db['video'].update(dict(id=vid['id'],status="processing",out_filename=os.path.join(vid['in_filename']+"."+rnd+".gif")),['id'])
        db.executable.close()
        cmd = ""#f"""ffmpeg -ss {start} -t {dur} -i {infile} -vf "fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" -loop 0 {outfile}"""
        proc = subprocess.Popen(cmd,shell=True)
        res = proc.communicate()
        db = dataset.connect('sqlite:///mydatabase.db')
        db['video'].update(dict(id=vid['id'],status="finished"),['id'])
        db.executable.close()
t=threading.Thread(target=Worker)
t.daemon=True
t.start()
AddUser("admin","qwe")
@app.route("/")
def index():
    return render_template('index.html')
def login():
    username = request.values['username']
    password = request.values['password']
    if IsUser(username,password):
        session['username'] = username
        return "OK"
    else:
        if 'username' in session:
            del session['username']
        return "NO"
def register():
    username = request.values['username']
    password = request.values['password']
    if AddUser(username,password):
        return "OK"
    else:
        if 'username' in session:
            del session['username']
        return "NO"
def islogin():
    if 'username' in session:
        return "OK"
    else:
        return "NO"
def logout():
    del session['username']
    return redirect("/")
def convert():
    fl = request.files['userfile']
    start,duration = request.values['start'],request.values['duration']
    spath = os.path.join("in",fl.filename)
    fl.save(spath)
    user = session['username']
    AddVideo(user,fl.filename,start,duration)
    return "Starting convert"
def listvideo():
    if not "username" in session:
        return "Error"
    res = ListUserData(session['username'])
    return jsonify({'data':res})
@app.route("/api/<method>",methods=['POST','GET'])
def api(method):
    if method == "login":
        return login()
    if method == "list":
        return listvideo()
    if method == "register":
        return register()
    if method == "islogin":
        return islogin()
    if method == "logout":
        return logout()
    if method == "convert":
        return convert()
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js',path)
@app.route('/out/<path:path>')
def send_out(path):
    return send_from_directory('out',path)
app.run(host='0.0.0.0',port = 8222, debug = True)

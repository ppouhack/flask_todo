import os
from flask import Flask
from flask import request
from models import db, Fcuser
from forms import RegisterForm, LoginForm
from flask import render_template,redirect, session
from api_v1 import api as api_v1

app = Flask(__name__)
app.register_blueprint(api_v1, url_prefix='/api/v1')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect('/')

@app.route('/',methods=['GET'])
def home():
    userid = session.get('userid',None)
    return render_template('home.html', userid=userid)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['userid'] = form.data.get('userid')
        return redirect('/')
    return render_template('login.html', form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    # form의 값이 채워져있지 않으면(회원가입) 회원가입 페이지 이동
    # form의 값이 채워져있다면(회원가입 작성완료) 로그인 페이지로 이동
    if form.validate_on_submit():
        fcuser = Fcuser()
        fcuser.userid = form.data.get('userid')
        fcuser.password = form.data.get('password')
        db.session.add(fcuser)
        db.session.commit()

        return redirect('/login')
    return render_template('register.html', form=form)

# 데이터베이스 생성
basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hi'

db.init_app(app)
db.app = app
db.create_all()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

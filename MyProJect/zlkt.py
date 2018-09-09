from flask import Flask,render_template,redirect,request,url_for,session
import config
from models import User,Question,Answer
from exts import db
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


# @login_required相当于index = login_required(index) = wrapper
@app.route('/')
@login_required
def index():
    content = {
        'questions':Question.query.order_by('-create_time').all()
    }
    return render_template('index.html',**content)

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telphone = request.form.get('telphone')
        password = request.form.get('password')
        user = User.query.filter(User.telphone==telphone,User.password==password).first()
        if user:
            session["user_id"] = user.id
            # 设置31天内都不需要登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            msg = '账号密码不匹配 ！'
            return render_template('login.html',msg=msg)
            # return '账号密码不匹配 ！'


@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telphone = request.form.get('telphone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 手机号码验证，如果手机号码已存在，则无法注册
        user = User.query.filter(User.telphone == telphone).first()
        if user:
            already_exists_msg = '手机号已存在 ！'
            return render_template('register.html',already_exists_msg=already_exists_msg)
        else:
            # password1和 password2要相等
            if password1 != password2:
                inconformity = '两次密码不一致 ！'
                return render_template('register.html', inconformity=inconformity)
            else:
                # 如果两次密码相同，则注册成功
                user = User(telphone=telphone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                # 注册成功，跳转到登录的页面
                return redirect(url_for('login'))


@app.route('/logout/')
def logout():
    # session.clear()
    # del session['user_id']
    session.pop('user_id')
    return redirect(url_for('login'))


@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id==user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<question_id>')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    answers = Answer.query.filter(Answer.question_id==question_id).count()
    return render_template('detail.html',question_model=question_model,answers=answers)

@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')

    answer = Answer(content=content)
    user_id = session['user_id']
    user = User.query.filter(User.id==user_id).first()
    answer.author = user

    question = Question.query.filter(Question.id==question_id).first()
    answer.question = question
    db.session.add(question)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))




@app.context_processor
def context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}


if __name__ == '__main__':
    app.run()

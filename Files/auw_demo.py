#encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, session
from exts import db
import config
from models import User, Question, Comment
from decorators import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)


@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get("email")
        print (email)
        password = request.form.get("password")
        print (password)
        user = User.query.filter(User.email == email, User.password == password).first()
        if user:
            session['user_id'] = user.id
            #if want auto login in 31days
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'email or password wrong! Please double check!'

@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    elif request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        #if not request.form.get("username") or not request.form.get("password1"):

        # email verification, if registered, cannot register
        user = User.query.filter(User.email == email).first()
        if user:
            return u'this email has been registered, please change to a new email address!'
        else:
            # password1 should be the same with password2
           if password1 != password2:
                return u'password wrong, please try again!'
           else:
               user = User(email=email, username=username, password=password1)
               db.session.add(user)
               db.session.commit()
        # if registered successfully, then jump to login page
        return redirect(url_for('login'))


@app.route('/question/', methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    elif request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        user_id=session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_model)


@app.route('/add_comment/', methods=['POST'])
@login_required
def add_comment():
    content = request.form.get('comment_content')
    question_id = request.form.get('question_id')
    comment = Comment(content=content)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    comment.author = user
    question = Question.query.filter(Question.id == question_id).first()
    comment.question = question
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail', question_id=question_id))


if __name__ == '__main__':
    app.run(debug=True)
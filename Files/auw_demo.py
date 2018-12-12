#encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for, session
from exts import db
import config
from models import User, Question, Comment, Underwrite
from decorators import login_required
from sqlalchemy import or_
import csv


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
env = app.jinja_env
#env.add_extension("flaskext.JavascriptBuilderExtension")
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
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


@app.route('/logout')
@login_required
def logout():
    #session.pop('user_id')
    #del session('user_id')
    session.clear()
    return redirect(url_for('login'))


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


@app.route('/underwrite/', methods=['GET','POST'])
@login_required
def underwrite():
    if request.method == "GET":
        return render_template("underwrite.html")
    elif request.method == "POST":
        name = request.form.get("name")
        gender = request.form.get("gender")
        age = request.form.get("age")
        occupation = request.form.get("occupation")
        if not request.form.get("name") or not request.form.get("gender") or not request.form.get("age") or not request.form.get("occupation"):
            return render_template('failure.html')
        file = open("user_info.csv", "a")
        writer = csv.writer(file)
        writer.writerow((request.form.get("name"), request.form.get("gender"),request.form.get("age"),request.form.get("occupation")))
        file.close()
        return render_template('success.html')


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}

@app.route('/search')
def search():
    keyword = request.args.get('keyword')
    result = Question.query.filter(or_(Question.title.contains(keyword),
                                        Question.content.contains(keyword))).order_by(
        Question.create_time.desc()).all()
    if result:
        return render_template('index.html', questions=result)
    else:
        return 'Not Found'

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

if __name__ == '__main__':
    app.run(debug=True)

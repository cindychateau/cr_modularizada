from flask import Flask, render_template, request, redirect, session

from flask_app import app
from flask_app.models.users import User
from flask_app.models.classrooms import Classroom

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    users = User.muestra_usuarios()
    return render_template("index.html",users=users)

@app.route('/new')
def new():
    classrooms = Classroom.muestra_salones()
    return render_template("new.html", classrooms=classrooms)

@app.route('/create', methods=['POST'])
def create():
    print(request.form)

    pwd = bcrypt.generate_password_hash(request.form['password'])

    formulario = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "classroom_id" : request.form['classroom_id'],
        "password" : pwd,
    }

    if not User.valida_user(formulario):
        return redirect('/new')
    
    User.guardar(formulario)
    return redirect('/')

@app.route('/show/<int:id>')
def show(id):
    data = {
        "id": id
    }
    user = User.mostrar(data)
    return render_template("show.html", user=user)
from flask_app.config.mysqlconnection import connectToMySQL
from .classrooms import Classroom
from .hobbies import Hobbie
from flask import flash
import re #Importa el uso de las Expresiones regulares

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.classroom_id = data['classroom_id']

        classroom = Classroom.muestra_salon_2(data['classroom_id'])
        self.classroom = classroom

        self.hobbies = []

        self.password = data['password']

    @classmethod
    def muestra_usuarios(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL('esquema_usuarios').query_db(query)
        # [
        #     {"id": "1","first_name":"Cynthia", "last_name": "Apellido", "email":"c@cd.com", "created_at": "2002-02", "updated_at"}
        # ]
        users = []
        for u in results:
            usr = cls(u)
            users.append(usr)
        return users
    
    @classmethod
    def guardar(cls, formulario):
        #data = {"first_name": "C", "last_name": "X", "email": "c@cd.com"}
        query = "INSERT INTO users (first_name, last_name, email, classroom_id, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(classroom_id)s, %(password)s)"
        result = connectToMySQL('esquema_usuarios').query_db(query, formulario)
        return result
    
    @classmethod
    def mostrar(cls, formulario):
        #formulario = {"id": "1"}
        query = "SELECT * FROM users LEFT JOIN users_has_hobbies ON users.id = user_id LEFT JOIN hobbies ON hobbies.id = hobbie_id WHERE users.id = %(id)s"
        result = connectToMySQL('esquema_usuarios').query_db(query, formulario)
        # [
        #     {'3','Juana','De Arco','juana@codingdojo.com','2022-03-09 14:50:58','2022-03-09 14:50:58'}
        # ]
        usr = result[0]
        user = cls(usr)
        print(result)
        for h in result:
            hobbie_data = {
                "id": h['hobbies.id'],
                "name": h['name'],
                "created_at": h['hobbies.created_at'],
                "updated_at": h['hobbies.updated_at']
            }

            hobbie = Hobbie(hobbie_data)
            user.hobbies.append(hobbie)
            

        return user
    #Funcion encargada de validar la información de mi usuario
    @staticmethod
    def valida_user(user):
        #Inicio un validador
        es_valido = True
        if len(user['first_name']) < 3:
            flash("El nombre del usuario debe tener al menos 3 caracteres")
            es_valido = False
        if len(user['last_name']) < 3:
            flash("El apellido del usuario debe ser de al menos 3 caracteres")
            es_valido = False
        if not EMAIL_REGEX.match(user['email']):
            flash("El correo electrónico es inválido")
            es_valido = False
        return es_valido
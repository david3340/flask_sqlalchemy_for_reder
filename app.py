
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),unique=True ,nullable=False)
    age = db.Column(db.Integer,unique=True, nullable=False)

    def __repr__(self):
        return '<Student %r>' % self.name



@app.route('/student', methods=['POST'])
def add_student():
    name = request.json['name']
    age = request.json['age']
    student = Student(name=name, age=age)
    db.session.add(student)
    db.session.commit()
    return jsonify({'id': student.id, 'name': student.name, 'age': student.age}), 201

@app.route('/student/<int:student_id>', methods=['GET'])

def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    return jsonify({'id': student.id, 'name': student.name, 'age': student.age})

@app.route('/student', methods=['GET'])
def display_all():
    res=[]
    for stu in Student.query.all():
        res.append({'id': stu.id, 'name': stu.name, 'age': stu.age})
    return jsonify (res)  



@app.route('/student/<int:student_id>', methods=['PUT'])
def update_student(student_id):

    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    student.name = request.json.get('name', student.name)
    student.age = request.json.get('age', student.age)
    db.session.commit()
    return jsonify({'id': student.id, 'name': student.name, 'age': student.age})

@app.route('/student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({'message': 'Student not found'}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted'})



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

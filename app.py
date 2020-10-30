from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbimpacta:impacta#2020@dbimpacta.postgresql.dbaas.com.br/dbimpacta'
app.debug = True
db = SQLAlchemy(app)


class claudio_faria(db.Model):
    ra = db.Column(db.Integer, primary_key=True)
    nome_do_aluno = db.Column(db.String(50))
    email_do_aluno = db.Column(db.String(50))
    logradouro = db.Column(db.String(50))
    numero = db.Column(db.String(5))
    cep = db.Column(db.String(10))
    complemento = db.Column(db.String(20))

    def __init__(self, ra, nome_do_aluno, email_do_aluno, logradouro, numero, cep, complemento):
        self.ra = ra
        self.nome_do_aluno = nome_do_aluno
        self.email_do_aluno = email_do_aluno
        self.logradouro = logradouro
        self.numero = numero
        self.cep = cep
        self.complemento = complemento

    def __repr__(self):
        return '<Aluno %r>' % self.nome_do_aluno


@app.route('/', methods=['DELETE', 'GET'])
def index():
    allStudents = claudio_faria.query.all()
    return render_template('students.html', allStudents=allStudents)


@app.route('/student')
def add_students():
    return render_template('add_student.html')


@app.route('/student/<ra>')
def student(ra):
    global selectstudent
    selectstudent = claudio_faria.query.filter_by(ra=ra).first()
    return render_template('studentProfile.html', student=selectstudent)


@app.route('/post_student', methods=['POST'])
def post_student():
    try:
        student = claudio_faria(request.form['ra'], request.form['nome_do_aluno'], request.form['email_do_aluno'],
                        request.form['logradouro'], request.form['numero'], request.form['cep'], request.form['complemento'])
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        print("error")


@app.route('/del_student/<ra>', methods=['DELETE'])
def del_student(ra):
    claudio_faria.query.filter_by(ra=ra).delete()
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit_student', methods=['PUT', 'GET'])
def edit_student():
    student = claudio_faria.query.filter_by(ra=selectstudent.ra).first()
    student.nome_do_aluno = request.args.get('nome_do_aluno')
    student.email_do_aluno = request.args.get('email_do_aluno')
    student.cep = request.args.get('cep')
    student.numero = request.args.get('numero')
    student.logradouro = request.args.get('logradouro')
    student.complemento = request.args.get('complemento')

    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

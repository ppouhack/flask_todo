from flask_sqlalchemy import SQLAlchemy

db =SQLAlchemy()

class Todo(db.Model):
    ___tablename__ = 'todo'

    id = db.Column(db.Integer, primary_key=True)
    # fcuser와 연결
    fcuser_id = db.Column(db.Integer, db.ForeignKey('fcuser.id'), ullable=False)
    title = db .Column(db.String(256))
    tstamp = db.Column(db.DateTime, server_default=db.func.now())

    @property
    def serialize(self):
        return {
            'id':self.id,
            'title': self.title,
            'tstamp': self.tstamp
        }

class Fcuser(db.Model):
    __tablename__ = 'fcuser'
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(32))
    password = db.Column(db.String(128))

    # 관계 지정
    todos = db.relationship('Todo',backref='fcuser',lazy=True)
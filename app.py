from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'endxskuifxndiinmenxmeibdgedidg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000))
    sender = db.Column(db.String(50))
    room = db.Column(db.Integer, db.ForeignKey('room.id'))

    def __repr__(self):
        return "<Name %r>" % self.id

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roomname = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(20))
    messages = db.relationship('Chat')

    def __repr__(self):
        return "<Name %r>" % self.id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['Name']
        roomname = request.form['Room']
        password = request.form['Pass']

        old_room = Room.query.filter_by(roomname=roomname).first()
        if check_password_hash(old_room.password, password):
            return redirect(url_for('chat', room=old_room.id, user=username))
        else:
            flash("Try Again")
    
    return render_template('index.html')

@app.route('/rooms/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        roomname = request.form['Room']
        password = request.form['Pass']

        try:
            new_room = Room(roomname=roomname, password=generate_password_hash(password))
            db.session.add(new_room)
            db.session.commit()

            flash("Added Room!")
        except:
            flash("There was an error... Try again...")
    
    return render_template('add.html')

@app.route('/chat/<int:room>/<user>', methods=['GET', 'POST'])
def chat(room, user):
    if request.method == 'POST':
        Message = request.form['Message']

        To_Add = Chat(content=Message, sender=user, room=room)
        db.session.add(To_Add)
        db.session.commit()
    
    ChatRoom = Room.query.get_or_404(room)
    Messages = ChatRoom.messages
    
    return render_template(
        'chat.html',
        ChatRoom=ChatRoom,
        Messages=Messages,
        User=user
    )
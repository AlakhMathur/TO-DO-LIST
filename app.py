from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    content = request.form['content']
    new_todo = Todo(content=content)
    db.session.add(new_todo)
    db.session.commit()
    return redirect('/')

@app.route('/complete/<int:id>')
def complete_todo(id):
    todo = Todo.query.get(id)
    todo.completed = not todo.completed
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_todo(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_todo(id):
    todo = Todo.query.get(id)

    if request.method == 'POST':
        new_content = request.form['content']
        todo.content = new_content
        db.session.commit()
        return redirect('/')

    return render_template('edit.html', todo=todo)

    
   


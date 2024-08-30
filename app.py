from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
  # Replace with your database URI
db.init_app(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    complete = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Todo {self.id}>"
    


@app.route('/')
def index():
    todos = Todo.query.all()
    return render_template('index.html', todos=todos)


@app.route('/add', methods=['POST'])
def add():
    new_task = request.form['task']
    if not new_task:
        return redirect(url_for('index'))
    
    new_todo = Todo(task=new_task)

    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    todo = Todo.query.get(id)

    if todo is None:
        # Handle the case where the todo item is not found
        return redirect(url_for('index'))

    if request.method == 'POST':
        todo.task = request.form['task']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', todo=todo)

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    todo = Todo.query.get(id)

    if todo is None:
        return redirect(url_for('index'))
    
    db.session.delete(todo)
    db.session.commit()
    
    return redirect(url_for('index'))


    
if __name__ == '__main__':
    db.create_all() 
    app.run(debug=True)


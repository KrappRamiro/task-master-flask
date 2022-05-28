from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
import logging
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

logging.basicConfig(level=logging.DEBUG)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id  # Returns the Task and the id


@app.route('/', methods=['POST', 'GET'])
def index():
    logging.info("Entrando a /")
    # Esto de abajo pasa cuando se hace una peticion POST, osea que el front nos esta tirando datos
    if request.method == 'POST':
        # Get the content from the form, exactly from the <input name="content">
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        logging.info(f"Añadiendo una task nueva con el valor: {task_content}")
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        # Esto es lo que se va a renderizar en el index.html
        return render_template('index.html', tasks=tasks)
        # Es tasks = tasks, porque ese tasks se lo va a estar pasando al {{ for task in tasks }}


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    logging.info("Entrando a delete")
    logging.info(f"El request method es {request.method}")
    logging.info(f"La task_to_delete es {task_to_delete}")
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    logging.info("Entrando a update")
    logging.info(f"El request method es {request.method}")
    logging.info(f"La task es {task}")

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
Scss(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Task {self.id}>"


#HOME PAGE
@app.route("/", methods=["GET", "POST"])
def index():
    #add a task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = MyTask(content = current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return "ERROR: {e}"
    #see all the current tasks
    else: 
        tasks = MyTask.query.order_by(MyTask.created).all()
    return render_template("index.html", tasks=tasks)


 #delet a task
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"ERROR: {e}")
        return "ERROR: {e}"


#update a task
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def update(id:int):      
    edited_task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        edited_task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return "ERROR: {e}"
    else: 
        return render_template("editTask.html", task=edited_task)     

if __name__ in"__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
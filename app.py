from datetime import datetime

from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return "<Task %r>" % self.id


db.create_all()


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        task_content = request.form["task"]
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            # db.session.commit()
            return redirect("/")
        except:
            return "There is an issue"
    else:
        tasks = Todo.query.order_by(Todo.pub_date).all()
        return render_template("index.html", tasks=tasks)


if __name__ == "__main__":
    app.run(debug=True)

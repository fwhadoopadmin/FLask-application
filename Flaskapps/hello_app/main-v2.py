from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime




# instance of a flask app
app = Flask(__name__) 
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# add a flag for sqlalchemy
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
# THIS WILL SPEED UP THE APP AND WILL NOT SAVE DATABASE EVERY SINGLE TIME


# create database object of sqlalchemy
db = SQLAlchemy(app)

class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task {self.id}"
    

# context manager to run the app immediately after its deployed 
with app.app_context():
    db.create_all()


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        current_task = request.form['content']
        # create new task object that will send to the database
        new_task = MyTask(content=current_task)

        try:
            db.session.add(new_task)
            db.session.commit()
            # return home page with updates
            return redirect("/")
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        # return render_template("index.html")
        return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"
   
# Edit an item 

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id:int):
    task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")

        except Exception as e:
            return f"Error: {e}"
    else:
        #return "HOME"
        return render_template("edit.html", task=task)

if __name__== "__main__":
    app.run(debug=True)
    
    # enable if running only locally
    # # create app context manager 
    # with app.app_context():
    #     db.create_all()
    #     #app.run(host="127.0.0.1", port=8080, debug=True)
    #     app.run(debug=True)
    ###########################
    # only run one main.py file or use main.py-v2 and not both of them at the same time
    ####################################################################################
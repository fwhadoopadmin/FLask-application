from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime




# instance of a flask app
app = Flask(__name__) 
Scss(app)

# configure the app 
# https://flask-sqlalchemy.palletsprojects.com/en/stable/quickstart/
# configure the SQLite database, relative to the app instance folder

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# add a flag for sqlalchemy
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
# THIS WILL SPEED UP THE APP AND WILL NOT SAVE DATABASE EVERY SINGLE TIME


# create database object of sqlalchemy
db = SQLAlchemy(app)

# create amodel for database 
# each rows of db ( represent ONE ROW OF DATA )
# each task is a model

# # close to like dataclass
# class MyTask(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     Content = db.Column(db.String(100), nullable=False)
#     complete = db.Column(db.Integer, default=0)
#     created = db.Column(db.DateTime, default=datetime.utcnow)
#     # created = db.Column(db.DateTime, default=datetime)


class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    # created = db.Column(db.DateTime, default=datetime)


   # USE DANDA METHOD OF A TRING REPRESENTATION TO RETRIEVE SOME DATA 
    def __repr__(self) -> str:
        return f"Task {self.id}"
    

# context manager to run the app immediately after its deployed 
with app.app_context():
    db.create_all()


# write decorator @app.route flask use to connect Urls Endpoints with code content functions 
#@route - defines url componect which is root path in this case
# The Home page
#What can we do in Homepage:  SEND, GET, RECEIVE DATA (POST, PUT,GET)
@app.route("/", methods=["POST", "GET"])



# next code index function 
# wrapped by the @app decorator
# function defines what should be executed if the url endpoint is requested by User
# naming index related to how page is called index.html
# # home page of application and creating a route to home page
# we use flask decorator to cretae a route  
def index():
    #return "Congratulations, it's a web app"
    #return render_template("../../index.html")
    # return render_template("/c/Workstation/projects/Flaskapps/templates/index.html")





    # ADD Tasks 
    # check what actions are happening -- with forloop
    # request.form comes from index.htm we get the content of it (html info)
    if request.method == "POST":
        current_task = request.form['content']
        # create new task object that will send to the database
        new_task = MyTask(content=current_task)

        # try to establish a connection to db 
        # add new task to db
       # commit new task to db
        try:
            db.session.add(new_task)
            db.session.commit()
            # return home page with updates
            return redirect("/")
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    else:
        # see all the tasks
        # query Model ordered by date
        tasks = MyTask.query.order_by(MyTask.created).all()
        # return render_template("index.html")
        return render_template("index.html", tasks=tasks)


# delete an Item
# route this page as well
# create index rooutes
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
    

    # # create app context manager 
    # with app.app_context():
    #     db.create_all()
    #     #app.run(host="127.0.0.1", port=8080, debug=True)
    #     app.run(debug=True)
    
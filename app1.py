from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


#connecting to flask and database
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


#sqlite Tables
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id 


#routes
@app.route("/", methods=['POST','GET'])
def index():
    if request.method == 'POST':
      user = request.form['nm']
      new_data = Todo(content = user)
      try:
        db.session.add(new_data)
        db.session.commit()
        return redirect('/')
      except:
        return "Hmm something went wrong your data is not added!"

    else:
        data = Todo.query.order_by(Todo.date_created).all()
        return render_template('one.html', data = data)

@app.route('/update/<int:id>',methods=['POST','GET'])
def chek(id):
    task_new = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task_new.content = request.form['nm']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "soemthing happend so ur data is not updated "
    else:
        return render_template('update.html',val=task_new)

@app.route('/delete/<int:id>')
def d(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "Hmm seems like there is a problem while delting the data"


#running server
if __name__ == "__main__":
    app.run(debug=True)
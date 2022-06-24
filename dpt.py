from flask import Flask, render_template, url_for, request, redirect
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
app.config['SQLALCHEMY_BINDS'] = {'two' : 'sqlite:///test2.db',
								  'three':'sqlite:///test3.db',
								  'first':'sqlite:///test5.db'}
								

db = SQLAlchemy(app)


#Drug class        
class Drug(db.Model):
	__bind_key__ = 'first'
	id = db.Column(db.Integer, primary_key=True)
	dname = db.Column(db.String(100))
	dno = db.Column(db.Integer)
	dprice = db.Column(db.Integer)
 
	def __init__(self, dname,dno,dprice):
		self.dname = dname
		self.dno=dno
		self.dprice=dprice
    

@app.route('/')
def front_page():
	return render_template("index1.html")


#addstudent
@app.route("/adddrug")
def adddrug():
    return render_template("adddrug.html")


@app.route("/suppliers")
def suppliers():
    return render_template("suppliers.html")

#studentlist 
@app.route("/drugslist", methods=['GET', 'POST'])
def drugslist():
	snm = request.form.get("dname")
	sno = request.form.get("dno")
	dpr = request.form.get("dprice")  

	drug = Drug(snm, sno, dpr)
	db.session.add(drug)
	db.session.commit()
	
	drugs = Drug.query.all()

	
	return render_template("drugslist.html", drugs=drugs)
#instructorlist

@app.route('/delete/<int:drugid>')
def delete(drugid):
    row_to_delete = Drug.query.filter_by(id=drugid).first()
    
    try:
        db.session.delete(row_to_delete)
        db.session.commit()
        return redirect("/drugslist")
    except:
        return "Error! Couldn't delete this row.Try Again!"    

#editdrug
@app.route("/editdrug/<int:drugid>", methods=["GET" , "POST"])
def editdrug(drugid):
	drug = Drug.query.filter_by(id=drugid).first()
    
	if request.method == "POST":
		dnamee = request.form.get("dname")
		dnoe = request.form.get("dno")
		dpri = request.form.get("dprice")
		
		drug.dname = dnamee
		drug.dno = dnoe
		drug.dprice = dpri
  
		db.session.commit()
		drugs = Drug.query.all()
		return render_template("drugslist.html",drugs=drugs)
	return render_template("editdrug.html",drug=drug)

	



@app.route("/selldrug/<int:drugid>", methods=["GET", "POST"])
def selldrug(drugid):
	drug = Drug.query.filter_by(id=drugid).first()

	if request.method == "POST":
		dnamee = request.form.get("dname")
		dnoe = request.form.get("dno")
		dpri = request.form.get("dprice")

		drug.dname = dnamee
		drug.dno -= int(dnoe)
		drug.dprice = dpri
		db.session.commit()
		drugs = Drug.query.all()
		# If the quantity is less than or equal to 50, redirect to the supplier's hub to purchase
		# or restock more drugs
		if drug.dno <= 50:
			return redirect("/suppliers")
		return render_template("drugslist.html", drugs=drugs)

	return render_template("selldrug.html", drug=drug)
	


if __name__=="__main__":
    db.create_all()
    app.run()



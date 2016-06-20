"""
cally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

DATABASEURI = "postgresql://zzz2113:7745@w4111vm.eastus.cloudapp.azure.com/w4111"
engine = create_engine(DATABASEURI)

#pre-GET request, used to connect to the database (like establishing a TCP connection to server in lab7)
@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.
  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

#post-GET request, closes the database connection (like closing TCP connection in lab7)
@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/

@app.route('/', methods=["GET"])
def index():
  return render_template("index.html")

@app.route('/selection', methods=["POST"])
def selection():
	global select 
	select= request.form.get('category')
	print select
	select = select.replace(" ", "_")
	if(select=="Author"):
		cursor = g.conn.execute('SELECT * FROM Author;')
	elif(select=="Text"):
		cursor = g.conn.execute('SELECT * FROM Text;')
	elif(select=="Institution"):
		cursor = g.conn.execute('SELECT * FROM Institution;')
	elif(select=="Literary_Style"):
		cursor = g.conn.execute('SELECT * FROM Literary_Style;')
	elif(select=="Country"):
		cursor = g.conn.execute('SELECT * FROM Country;')
	elif(select=="Publisher"):
		cursor = g.conn.execute('SELECT * FROM Publisher;')
	elif(select=="Structure"):
		cursor = g.conn.execute('SELECT * FROM Structure;')
	names = []
  	for result in cursor:
	    	names.append(result[0])
	  	context = dict(data = names)
	cursor.close()
	return render_template("/selection.html", **context)

@app.route('/result', methods=["POST"])
def result():
        resultvar1 = request.form.get('entity1')
        print resultvar1
	resultvar2 = request.form.get('entity2')
        print resultvar2
	
#For later: create provision:
#if resultvar1 is blank, make it null
#if resultvar2 is blank, make it null
#if both are blank, return to same page

	if(select == "Author"):	
		queryA = "SELECT A.author_name, B.year AS birth_date, B.country_name, A.noun_frequency, A.adjective_frequency, A.preposition_frequency, A.verb_frequency, A.adverb_frequency, A.determiner_frequency, A.conjunction_frequency, A.pronoun_frequency, A.pronoun_frequency, A.most_common_word FROM Author A JOIN Born_In B ON A.author_name=B.author_name WHERE A.author_name=\'" + resultvar1 + "\' OR A.author_name=\'" + resultvar2 + "\';"
		print queryA
		cursorA = g.conn.execute(queryA)
		namesA = []
		for result in cursorA:
			namesA.append(result)
			contextA = dict(table1 = namesA)
		cursorA.close()
		return render_template("/authorresult.html", **contextA)

		queryB = "SELECT W.title AS texts, W.before AS Year FROM Written_By W WHERE W.author_name=\'" + resultvar1 + "\';"
		cursorB = g.conn.execute(queryB)
		namesB = []
	  	for result in cursorB:
		    	namesB.append(result)
		contextB = dict(table2 = namesB)
		cursorB.close()
		#return render_template("/authorresult.html", **contextB)

		queryC = "SELECT W.title AS texts, W.before AS Year FROM Written_By W WHERE W.author_name=\'" + resultvar2 + "\';" 
	        cursorC = g.conn.execute(queryC)
		namesC = []
	  	for result in cursorC:
		    	namesC.append(result)
		contextC = dict(table3 = namesC)
		cursorC.close()
		#return render_template("/authorresult.html", **contextC)	
		#return render_template("/authorresult.html",**contextA, **contextB, **contextC)


	if(select == "Country"):	
		queryA = "SELECT * FROM Country C WHERE C.country_name=\'" + resultvar1 + "\' OR C.country_name=\'" + resultvar2 + "\';"
		cursorA = g.conn.execute(queryA)
		namesA = []
		for result in cursorA:
			namesA.append(result)
			contextA = dict(data = namesA)
		return render_template("/countryresult.html", **contextA)

		queryB = "SELECT Pi.title AS texts FROM Published_In Pi WHERE Pi.country_name=\'" + resultvar1 + "\';"
		cursorB = g.conn.execute(queryB)#SQL query for table2
		namesB = []
	  	for result in cursorB:
		    	namesB.append(result[0])
		  	contextB = dict(data = namesB)
		cursorB.close()
		#return render_template("/countryresult.html",**contextB)

                queryC = "SELECT Pi.title AS texts FROM Published_In Pi WHERE Pi.country_name=\'" + resultvar2 + "\';"
	        cursorC = g.conn.execute(queryC)#SQL query for table3
		namesC = []
	  	for result in cursorC:
		    	namesC.append(result[0])
		  	contextC = dict(data = namesC)
		cursorC.close()
		#return render_template("/countryresult.html",**contextC)	
		#return render_template("/countryresult.html", table1 = **contextA, table2 = **contextB, table3 = **contextC)

		
	elif(select == "Institution"):	
		queryA = "SELECT I.institution_name, R.country_name FROM Institution I JOIN Resides_In R ON I.institution_name=R.institution_name WHERE I.institution_name=\'" +resultvar1 + "\' OR I.institution_name=\'" + resultvar2 +"\';"
		cursorA = g.conn.execute(queryA)
		namesA = []
		for result in cursorA:
			namesA.append(result)
			contextA = dict(data = namesA)
		return render_template("/institutionresult.html", **contextA)

		queryB = "SELECT T.author_name AS author, T.subject FROM Taught_At T WHERE T.institution_name=\'" + resultvar1 + "\';"
		cursorB = g.conn.execute(queryB)#SQL query for table2
		namesB = []
	  	for result in cursorB:
		    	namesB.append(result)
		  	contextB = dict(data = namesB)
		cursorB.close()
		#return render_template("/institutionresult.html", **contextB)

                queryC = "SELECT T.author_name AS author, T.subject FROM Taught_At T WHERE T.institution_name=\'" + resultvar2 + "\';"
	        cursorC = g.conn.execute(queryC)#SQL query for table3
		namesC = []
	  	for result in cursorC:
		    	namesC.append(result)
		  	contextC = dict(data = namesC)
		cursorC.close()
		#return render_template("/institutionresult.html", **contextB)
		#return render_template("/institutionresult.html", table1 = **contextA, table2 = **contextB, table3 = **contextC)
		
	elif(select == "Publisher"):	
		queryA = "SELECT P.publisher_name, L.country_name FROM Publisher P JOIN Located_In L ON P.publisher_name=L.publisher_name WHERE P.publisher_name=\'" + resultvar1 + "\' OR P.publisher_name=\'" +resultvar2 + "\';"
		cursorA = g.conn.execute(queryA)
		namesA = []
		for result in cursorA:
			namesA.append(result)
			contextA = dict(data = namesA)
		return render_template("/publisherresult.html", **contextA)

		queryB = "SELECT P.title AS texts, P.year AS year_of_publication FROM Published_By P WHERE P.publisher_name=\'" +resultvar1 + "\';"
		cursorB = g.conn.execute(queryB)#SQL query for table2
		namesB = []
	  	for result in cursorB:
		    	namesB.append(result)
		  	contextB = dict(data = namesB)
		cursorB.close()
		#return render_template("/publisherresult.html", **contextB)

                queryC = "SELECT P.title AS texts, P.year AS year_of_publication FROM Published_By P WHERE P.publisher_name=\'" +resultvar2 + "\';"
	        cursorC = g.conn.execute(queryC)#SQL query for table3
		namesC = []
	  	for result in cursorC:
		    	namesC.append(result)
		  	contextC = dict(data = namesC)
		cursorC.close()
		#return render_template("/publisherresult.html", **contextC)
		#return render_template("/publisherresult.html", table1 = **contextA, table2 = **contextB, table3 = **contextC)
		
		
	elif(select == "Structure"):	
		queryA = "SELECT * FROM Structure S WHERE S.structure_name=\'" + resultvar1 + "\' OR S.structure_name=\'" +resultvar2 + "';"
		cursorA = g.conn.execute(queryA)
		namesA = []
		for result in cursorA:
			namesA.append(result)
			contextA = dict(data = namesA)
		return render_template("/structureresult.html", **contextA)

		queryB = "SELECT W.title AS texts FROM Written_As_A W WHERE W.structure_name=\'" +resultvar1 +"\';"
		cursorB = g.conn.execute('')#SQL query for table2
		namesB = []
	  	for result in cursorB:
		    	namesB.append(result[0])
		  	contextB = dict(data = namesB)
		cursorB.close()
		#return render_template("/structureresult.html", **contextB)

                queryC = "SELECT W.title AS texts FROM Written_As_A W WHERE W.structure_name=\'" +resultvar2 +"\';"
	        cursorC = g.conn.execute('')#SQL query for table3
		namesC = []
	  	for result in cursorC:
		    	namesC.append(result[0])
		  	contextC = dict(data = namesC)
		cursorC.close()
		#return render_template("/structureresult.html", **contextC)
		#return render_template("/structureresult.html", table1 = **contextA, table2 = **contextB, table3 = **contextC)
		

	elif(select == "Literary_Style"):	
		queryA = "SELECT * FROM Literary_Style L WHERE L.style_name=\'" +resultvar1 + "\' OR L.style_name=\'" + resultvar2 + "\';"
		cursorA = g.conn.execute(queryA)
		namesA = []
		for result in cursorA:
			namesA.append(result)
			contextA = dict(data = namesA)
		return render_template("/literarystyleresult.html", **contextA)

		queryB = "SELECT W.title AS texts FROM Written_In W WHERE W.style_name=\'" + resultvar1 +"\';"
		cursorB = g.conn.execute(queryB)#SQL query for table2
		namesB = []
	  	for result in cursorB:
		    	namesB.append(result[0])
		  	contextB = dict(data = namesB)
		cursorB.close()
		#return render_template("/literarystyleresult.html", **contextB)

                queryC = "SELECT W.title AS texts FROM Written_In W WHERE W.style_name=\'" + resultvar1 +"\';"
	        cursorC = g.conn.execute('')#SQL query for table3
		namesC = []
	  	for result in cursorC:
		    	namesC.append(result[0])
		  	contextC = dict(data = namesC)
		cursorC.close()
		#return render_template("/literarystyleresult.html", **contextC)
                #return render_template("/literarystyleresult.html", table1 = **contextA, table2 = **contextB, table3 = **contextC)
                
 	elif(select == "Texts"):	
		queryA = "SELECT T.title, Pi.country_name, Pb.publisher_name, Wa.structure_name, Wi.style_name, T.noun_frequency, T.adjective_frequency, T.preposition_frequency, T.verb_frequency, T.adverb_frequency, T.determiner_frequency, T.conjunction_frequency, T.pronoun_frequency, T.pronoun_frequency, T.most_common_word FROM Text T, Published_In Pi, Published_By Pb, Written_As_A Wa, Written_In Wi WHERE T.title=Pi.title AND T.title=Pb.title AND T.title=Wa.title AND T.title=Wi.title AND (T.title=\'" + resultvar1 + "\' OR T.title=\'" + resultvar2 + "\');"
		cursorA = g.conn.execute(queryA)
		namesA = []
		for result in cursorA:
			namesA.append(result)
		contextA = dict(table1 = namesA)
		cursorA.close()
		return render_template("/textresult.html", **contextA)

		queryB = "SELECT W.author_name AS authors, W.before AS Year FROM Written_By W WHERE W.title=\'" + resultvar1 + "\';"
		cursorB = g.conn.execute(queryB)
		namesB = []
	  	for result in cursorB:
		    	namesB.append(result)
		contextB = dict(table2 = namesB)
		cursorB.close()
		#return render_template("/textresult.html", **contextB)	
	
		queryC = "SELECT W.author_name AS authors, W.before AS Year FROM Written_By W WHERE W.title=\'" + resultvar2 + "\';"
	        cursorC = g.conn.execute(queryC)
		namesC = []
	  	for result in cursorC:
		    	namesC.append(result)
		contextC = dict(table3 = namesC)
		cursorC.close()
		#return render_template("/textresult.html", **contextC)
		#return render_template("/textresult.html", table1 = **contextA, table2 = **contextB, table3 = **contextC)               

"""
	rows = cursorA.fetchall()
	data = [ dict(zip(cursorA.keys(), row)) for row in rows]
		rows = 2
		columns = 13
		mytable = [[0 for x in range(columns)] for x in range(rows)]
		for i in range(rows):
    			for j in range(columns):
        			mytable[i][j] = '%s,%s'%(i,j)
		for result in cursorA:
		    	namesA.append(result[0])
		  	contextA = dict(data = namesA)
		cursorA.close()
		return render_template("/authorresult.html", **contextA)
"""

"""
rows = 2
columns = 13
mytable = [[0 for x in range(columns)] for x in range(rows)]
for i in range(rows):
    for j in range(columns):
        mytable[i][j] = '%s,%s'%(i,j)
"""

"""
	return render_template("/authorresult.html", **contextA, **contextB, **contextC)
"""

"""
  if(select == "Text"):
  	return render_template("/textresult.html", **context)
  if(select == "Publisher"):
  	return render_template("/publisherresult.html", **context)
  if(select == "Country"):
  	return render_template("/countryresult.html", **context)
  if(select == "Literary_Style"):
  	return render_template("/literarystyleresult.html", **context)
  if(select == "Structure"):
  	return render_template("/structureresult.html", **context)
  if(select == "Institution"):
  	return render_template("/institutionresult.html", **context)
"""

""" 
  request is a special object that Flask provides to access web request information:
  These methods are used to gather information about the HTML GET request coming from the browser
the server, since it's a server, isn't requesting anything itself. Only the browser is requesting something.
  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2
  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
"""

#This means that the following is effectively our "main" function
if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:
        python server.py
    Show the help text using:
        python server.py --help
    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()

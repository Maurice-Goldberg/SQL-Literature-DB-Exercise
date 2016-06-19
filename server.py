"""
To run locally:

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
	select = request.form.get('category')
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

@app.route('/result')
def result():
  if(select == "Author"):
        resultvar1 = request.form.get('entity1')
        resultvar2 = request.form.get('entity2')
        
  	#One table for 1 to 2 authors
        cursorA = g.conn.execute('')#SQL query for table1
	namesA = []
  	for result in cursorA:
	    	namesA.append(result[0])
	  	contextA = dict(data = namesA)
	cursorA.close()
	return render_template("/authorresult.html", **contextA)

#HOW DO YOU CREATE THREE SEPARATE TABLES IN FLASK ON ONE PAGE?? Can you render template three different times?

  	#One to two tables for texts by the author(s)
        cursorB = g.conn.execute('')#SQL query for table2
	namesB = []
  	for result in cursorB:
	    	namesB.append(result[0])
	  	contextB = dict(data = namesB)
	cursorB.close()
	return render_template("/authorresult.html", **contextB)

        cursorC = g.conn.execute('')#SQL query for table3
	namesC = []
  	for result in cursorC:
	    	namesC.append(result[0])
	  	contextC = dict(data = namesC)
	cursorC.close()
	return render_template("/authorresult.html", **contextC)

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


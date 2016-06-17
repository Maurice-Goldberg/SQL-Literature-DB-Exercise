"""Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

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


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111a.eastus.cloudapp.azure.com/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@w4111a.eastus.cloudapp.azure.com/proj1part2"
#

#TO ZANE: Figure out what we need to name the end of the URL instead of "w4111". Or maybe we're supposed to use w4111? Not sure.
DATABASEURI = "postgresql://zzz2113:7745@w4111vm.eastus.cloudapp.azure.com/w4111"

# This line creates a database engine that knows how to connect to the URI above.
engine = create_engine(DATABASEURI)

#According to the instructions, below is where we input the data into our database (Apparently we have to do it in the python code, even though we already did it in Part 2). These engine.execute() functions are SQLAlchemy methods.

#WHAT YOU (ZANE) NEED TO DO:
#Format all the SQL statements below into separate engine.execute() functions, just like the follwoing example:
#ex(do not actually use this statement):
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")

"""
CREATE TABLE Text(
        title CHAR(60),
        noun_frequency INTEGER NOT NULL CHECK (noun_frequency<100),
        adjective_frequency INTEGER NOT NULL CHECK (adjective_frequency <100),
        preposition_frequency INTEGER NOT NULL CHECK (preposition_frequency <100),
        verb_frequency INTEGER NOT NULL CHECK (verb_frequency <100),
        adverb_frequency INTEGER NOT NULL CHECK (adverb_frequency <100),
        determiner_frequency INTEGER NOT NULL CHECK (determiner_frequency <100),
        conjunction_frequency INTEGER NOT NULL CHECK (conjunction_frequency <100),
        pronoun_frequency INTEGER NOT NULL CHECK (pronoun_frequency <100),
        most_common_word CHAR(45) NOT NULL,
        PRIMARY KEY (title)
);

INSERT INTO Text values('Rabbit Is Rich', 25, 20, 15, 15, 10, 10, 2, 3, 'lust');
INSERT INTO Text values('Portnoy’s Complaint', 18, 27, 12, 10, 18, 6, 6, 3, 'passion');
INSERT INTO Text values('The Plot Against America', 22, 23, 18, 10, 12, 4, 8, 3, 'fear');
INSERT INTO Text values('Ulysses', 30, 20, 10, 12, 13, 5, 3, 7,'lonely');
INSERT INTO Text values('Tender Buttons', 20, 23, 17, 11, 14, 6, 2, 7,'went');
INSERT INTO Text values('Pride And Prejudice', 15, 25, 10, 21, 19, 2, 2, 6, 'laundry');
INSERT INTO Text values('God Is Not Great', 32, 26, 12, 10, 5, 5, 5, 5, 'hair');
INSERT INTO Text values('The Angel Esmeralda', 22, 18, 24, 17, 4, 5, 6, 4, 'city');
INSERT INTO Text values('Cosmos', 15, 21, 11, 13, 12, 21, 3, 4, 'space');
INSERT INTO Text values('Negative Dialectics', 13, 23, 10, 14, 16, 17, 3, 4, 'time');
INSERT INTO Text values('Much Ado About Nothing', 24, 21, 14, 17, 9, 7, 5, 3,'wonderous');

CREATE TABLE Author(
        author_name CHAR(30),
        noun_frequency INTEGER NOT NULL CHECK (noun_frequency<100),
        adjective_frequency INTEGER NOT NULL CHECK (adjective_frequency <100),
        preposition_frequency INTEGER NOT NULL CHECK (preposition_frequency <100),
        verb_frequency INTEGER NOT NULL CHECK (verb_frequency <100),
        adverb_frequency INTEGER NOT NULL CHECK (adverb_frequency <100),
        determiner_frequency INTEGER NOT NULL CHECK (determiner_frequency <100),
        conjunction_frequency INTEGER NOT NULL CHECK (conjunction_frequency <100),
        pronoun_frequency INTEGER NOT NULL CHECK (pronoun_frequency <100),
        most_common_word CHAR(45) NOT NULL,
        PRIMARY KEY (author_name)
);

INSERT INTO Author values('John Updike', 25, 20, 15, 15, 10, 10, 2, 3, 'lust');
INSERT INTO Author values('Phillip Roth', 20, 25, 15, 10, 15, 5, 7, 3, 'passion' );
INSERT INTO Author values('James Joyce', 30, 20, 10, 12, 13, 5, 3, 7,'lonely');
INSERT INTO Author values('Gertrude Stein', 20, 23, 17, 11, 14, 6, 2, 7,'went');
INSERT INTO Author values('Jane Austen', 15, 25, 10, 21, 19, 2, 2, 6,'laundry');
INSERT INTO Author values('Christopher Hitchens', 32, 26, 12, 10, 5, 5, 5, 5,'God');
INSERT INTO Author values('Don Delillo', 22, 18, 24, 17, 4, 5, 6, 4,'city');
INSERT INTO Author values('Theodor Adorno', 13, 23, 10, 14, 16, 17, 3, 4,'time');
INSERT INTO Author values('Carl Sagan', 15, 21, 11, 13, 12, 21, 3, 4,'space');
INSERT INTO Author values('William Shakespeare', 24, 21, 14, 17, 9, 7, 5, 3,'wonderous');



CREATE TABLE Written_By(
        title CHAR(60),
        author_name CHAR(30),
        before INTEGER CHECK (before < 2016),
        PRIMARY KEY (title, author_name),
        FOREIGN KEY (title) REFERENCES Text
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        FOREIGN KEY (author_name) REFERENCES Author
                ON DELETE CASCADE
                ON UPDATE CASCADE
);

INSERT INTO Written_By values('Rabbit Is Rich', 'John Updike', 1955);
INSERT INTO Written_By values('Portnoy’s Complaint', 'Phillip Roth', 1963);
INSERT INTO Written_By values('The Plot Against America', 'Phillip Roth', 1963);
INSERT INTO Written_By values('Ulysses', 'James Joyce', 1912);
INSERT INTO Written_By values('Tender Buttons', 'Gertrude Stein', 1908);
INSERT INTO Written_By values('Pride And Prejudice', 'Jane Austen', 1813);
INSERT INTO Written_By values('God Is Not Great', 'Christopher Hitchens', 2004);
INSERT INTO Written_By values('The Angel Esmeralda', 'Don Delillo', 2008);
INSERT INTO Written_By values('Negative Dialectics', 'Theodor Adorno', 1947);
INSERT INTO Written_By values('Cosmos', 'Carl Sagan', 1999);
INSERT INTO Written_By values('Much Ado About Nothing', 'William Shakespeare', 1553);


CREATE TABLE Structure(
        structure_name CHAR(30),
        noun_frequency INTEGER NOT NULL CHECK (noun_frequency<100),
        adjective_frequency INTEGER NOT NULL CHECK (adjective_frequency <100),
        preposition_frequency INTEGER NOT NULL CHECK (preposition_frequency <100),
verb_frequency INTEGER NOT NULL CHECK (verb_frequency <100),
        adverb_frequency INTEGER NOT NULL CHECK (adverb_frequency <100),
        determiner_frequency INTEGER NOT NULL CHECK (determiner_frequency <100),
        conjunction_frequency INTEGER NOT NULL CHECK (conjunction_frequency <100),
        pronoun_frequency INTEGER NOT NULL CHECK (pronoun_frequency <100),
        most_common_word CHAR(45) NOT NULL,
        PRIMARY KEY (structure_name)
);

INSERT INTO Structure values('Novel', 28, 17, 16, 14, 6, 9, 5, 4, 'lonely');
INSERT INTO Structure values('Short Story', 23, 18, 17, 12, 4, 9, 7, 5, 'city');
INSERT INTO Structure values('Book Of Science Research', 15, 21, 11, 13, 12, 21, 3, 4, 'space');
INSERT INTO Structure values('Book Of Poetry', 20, 23, 17, 11, 14, 6, 2, 7,'went');
INSERT INTO Structure values('Book Of Essays', 32, 26, 12, 10, 5, 5, 5, 5,'hair');
INSERT INTO Structure values('Play', 24, 21, 14, 17, 9, 7, 5, 3,'wonderous');


CREATE TABLE Written_As_A(
        title CHAR(60),
        structure_name CHAR(30) NOT NULL,
        PRIMARY KEY (title),
        FOREIGN KEY (title) REFERENCES Text
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        FOREIGN KEY (structure_name) REFERENCES Structure
                ON DELETE CASCADE
                ON UPDATE CASCADE
);


INSERT INTO Written_As_A values('Rabbit Is Rich', 'Novel');
INSERT INTO Written_As_A values('Portnoy’s Complaint', 'Novel');
INSERT INTO Written_As_A values('The Plot Against America', 'Novel');
INSERT INTO Written_As_A values('Ulysses', 'Novel');
INSERT INTO Written_As_A values('Tender Buttons', 'Book Of Poetry');
INSERT INTO Written_As_A values('Pride And Prejudice', 'Novel');
INSERT INTO Written_As_A values('God Is Not Great', 'Book Of Essays');
INSERT INTO Written_As_A values('The Angel Esmeralda', 'Short Story');
INSERT INTO Written_As_A values('Cosmos', 'Book Of Essays');
INSERT INTO Written_As_A values('Negative Dialectics', 'Book Of Essays');
INSERT INTO Written_As_A values('Much Ado About Nothing', 'Play');

CREATE TABLE Country(
        country_name CHAR(20),
        noun_frequency INTEGER CHECK (noun_frequency<100),
        adjective_frequency INTEGER CHECK (adjective_frequency <100),
        preposition_frequency INTEGER CHECK (preposition_frequency <100),
        verb_frequency INTEGER CHECK (verb_frequency <100),
        adverb_frequency INTEGER CHECK (adverb_frequency <100),
        determiner_frequency INTEGER CHECK (determiner_frequency <100),
        conjunction_frequency INTEGER CHECK (conjunction_frequency <100),
        pronoun_frequency INTEGER CHECK (pronoun_frequency <100),
        most_common_word CHAR(45),
        PRIMARY KEY (country_name)
);

INSERT INTO Country values('United States', 25, 20, 15, 15, 10, 5, 5, 5, 'God');
INSERT INTO Country values('Britain', 26, 20, 14, 17, 10, 6, 3, 4);
INSERT INTO Country values('Ireland', 30, 20, 10, 12, 13, 5, 3, 7, 'lonely');
INSERT INTO Country values('Germany', 13, 23, 10, 14, 16, 17, 3, 4,'time');
INSERT INTO Country values('Australia', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO Country values('France', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO Country values('Japan', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO Country values('China', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO Country values('Mexico', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO Country values('Canada', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);


CREATE TABLE Published_In(
        title CHAR(60),
        country_name CHAR(20) NOT NULL,
        PRIMARY KEY (title),
        FOREIGN KEY (title) REFERENCES Text
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        FOREIGN KEY (country_name) REFERENCES Country
                ON DELETE CASCADE
                ON UPDATE CASCADE
);

INSERT INTO Published_In values('Rabbit Is Rich', 'United States');
INSERT INTO Published_In values('Portnoy’s Complaint', 'United States');
INSERT INTO Published_In values('The Plot Against America', 'United States');
INSERT INTO Published_In values('Ulysses', 'Britain');
INSERT INTO Published_In values('Tender Buttons', 'France');
INSERT INTO Published_In values('Pride And Prejudice', 'Britain');
INSERT INTO Published_In values('God Is Not Great', 'Britain');
INSERT INTO Published_In values('The Angel Esmeralda', 'United States');
INSERT INTO Published_In values('Cosmos', 'Britain');
INSERT INTO Published_In values('Negative Dialectics', 'Britain');
INSERT INTO Published_In values('Much Ado About Nothing', 'Britain');


CREATE TABLE Born_In(
        author_name CHAR(30),
        year INTEGER CHECK (year < 2016),
        country_name CHAR(20) NOT NULL,
        PRIMARY KEY (author_name),
        FOREIGN KEY (author_name) REFERENCES Author
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        FOREIGN KEY (country_name) REFERENCES Country
                ON DELETE CASCADE
                ON UPDATE CASCADE
);

INSERT INTO Born_In values('John Updike', 1930, 'United States');
INSERT INTO Born_In values('Phillip Roth', 1943, 'United States');
INSERT INTO Born_In values('James Joyce', 1880, 'Ireland');
INSERT INTO Born_In values('Gertrude Stein', 1860, 'United States');
INSERT INTO Born_In values('Jane Austen', 1815, 'Britain');
INSERT INTO Born_In values('Christopher Hitchens', 1966, 'Britain');
INSERT INTO Born_In values('Don Delillo', 1952, 'United States');
INSERT INTO Born_In values('Theodor Adorno', 1874, 'Germany');
INSERT INTO Born_In values('Carl Sagan', 1974, 'Britain');
INSERT INTO Born_In values('William Shakespeare', 1543, 'Britain');

CREATE TABLE Publisher(
        publisher_name CHAR(30),
        PRIMARY KEY (publisher_name)
);

INSERT INTO Publisher values('Penguin Random House');
INSERT INTO Publisher values('Simon & Schuster');
INSERT INTO Publisher values('HarperCollins Publishers');
INSERT INTO Publisher values('Macmillian U.S.');
INSERT INTO Publisher values('Hachette Book Group');
INSERT INTO Publisher values('Oxford University Press');
INSERT INTO Publisher values('Pearson Education');
INSERT INTO Publisher values('Bloomsbury');
INSERT INTO Publisher values('John Wiley And Sons');
INSERT INTO Publisher values('Faber Independent Alliance');

CREATE TABLE Published_By(
        title CHAR(60),
        year INTEGER CHECK (year <2016),
        publisher_name CHAR(30) NOT NULL,
        PRIMARY KEY (title),
        FOREIGN KEY (title) REFERENCES Text
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        FOREIGN KEY (publisher_name) REFERENCES Publisher
                ON DELETE CASCADE
                ON UPDATE CASCADE
);

INSERT INTO Published_By values('Rabbit Is Rich', 1957, 'Simon & Schuster');
INSERT INTO Published_By values('Portnoy’s Complaint', 1964, 'Macmillian U.S.');
INSERT INTO Published_By values('The Plot Against America', 1965, 'Macmillian U.S.');
INSERT INTO Published_By values('Ulysses', 1942, 'Bloomsbury');
INSERT INTO Published_By values('Tender Buttons', 1910, 'Penguin Random House');
INSERT INTO Published_By values('Pride And Prejudice', 1813, 'John Wiley And Sons');
INSERT INTO Published_By values('God Is Not Great', 2006, 'John Wiley And Sons');
INSERT INTO Published_By values('The Angel Esmeralda', 2009, 'HarperCollins Publishers');
INSERT INTO Published_By values('Cosmos', 2000, 'Faber Independent Alliance');
INSERT INTO Published_By values('Negative Dialectics', 1955, 'Oxford University Press');
INSERT INTO Published_By values('Much Ado About Nothing', 1813, 'Oxford University Press');


CREATE TABLE Located_In(
        publisher_name CHAR(30),
        country_name CHAR(20) NOT NULL,
        PRIMARY KEY (publisher_name),
        FOREIGN KEY (publisher_name) REFERENCES Publisher
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        FOREIGN KEY (country_name) REFERENCES Country
                ON DELETE CASCADE
                ON UPDATE CASCADE
);

INSERT INTO Located_In values('Penguin Random House', 'United States');
INSERT INTO Located_In values('Simon & Schuster', 'United States');
INSERT INTO Located_In values('HarperCollins Publishers', 'United States');
INSERT INTO Located_In values('Macmillian U.S.', 'United States');
INSERT INTO Located_In values('Hachette Book Group', 'United States');
INSERT INTO Located_In values('Oxford University Press', 'Britain');
INSERT INTO Located_In values('Pearson Education', 'Britain');
INSERT INTO Located_In values('Bloomsbury', 'Britain');
INSERT INTO Located_In values('John Wiley And Sons', 'Britain');
INSERT INTO Located_In values('Faber Independent Alliance', 'Britain');


CREATE TABLE Institution(
        institution_name CHAR(30),
        PRIMARY KEY (institution_name)
);

INSERT INTO Institution values('Columbia University');
INSERT INTO Institution values('Harvard University');
INSERT INTO Institution values('Yale University');
INSERT INTO Institution values('Princeton University');
INSERT INTO Institution values('Hampshire College');
INSERT INTO Institution values('Pennsylvania State College');
INSERT INTO Institution values('Boston College');
INSERT INTO Institution values('Barnard College');
INSERT INTO Institution values('Bard College');
INSERT INTO Institution values('Dartmouth University');
INSERT INTO Institution values('Williams College');
INSERT INTO Institution values('Amherst College');
INSERT INTO Institution values('London School Of Economics');
INSERT INTO Institution values('Oxford University');

CREATE TABLE Resides_In(
        institution_name CHAR(30),
        country_name CHAR(20) NOT NULL,
        PRIMARY KEY (institution_name),
        FOREIGN KEY (institution_name) REFERENCES Institution
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        FOREIGN KEY (country_name) REFERENCES Country
                ON DELETE CASCADE
                ON UPDATE CASCADE
);

INSERT INTO Resides_In values('Columbia University', 'United States');
INSERT INTO Resides_In values('Harvard University', 'United States');
INSERT INTO Resides_In values('Yale University', 'United States');
INSERT INTO Resides_In values('Princeton University', 'United States');
INSERT INTO Resides_In values('Hampshire College', 'United States');
INSERT INTO Resides_In values('Pennsylvania State College', 'United States');
INSERT INTO Resides_In values('Boston College', 'United States');
INSERT INTO Resides_In values('Barnard College', 'United States');
INSERT INTO Resides_In values('Bard College', 'United States');
INSERT INTO Resides_In values('Dartmouth University', 'United States');
INSERT INTO Resides_In values('Williams College', 'United States');
INSERT INTO Resides_In values('Amherst College', 'United States');
INSERT INTO Resides_In values('London School Of Economics', 'Britain');
INSERT INTO Resides_In values('Oxford University', 'Britain');

CREATE TABLE Taught_At(
        author_name CHAR(30),
        subject CHAR(20),
        institution_name CHAR(30),
        PRIMARY KEY (author_name,institution_name),
        FOREIGN KEY (author_name) REFERENCES Author
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        FOREIGN KEY (institution_name) REFERENCES Institution
                ON DELETE CASCADE
                ON UPDATE CASCADE
);

INSERT INTO Taught_At values('John Updike', 'English', 'Harvard University');
INSERT INTO Taught_At values('Phillip Roth', 'English', 'Dartmouth University');
INSERT INTO Taught_At values('James Joyce', 'English', 'Oxford University');
INSERT INTO Taught_At values('Christopher Hitchens', 'Political Philosophy', 'London School Of Economics');
INSERT INTO Taught_At values('Don Delillo', 'English', 'Amherst College');
INSERT INTO Taught_At values('Carl Sagan', 'Physics', 'Oxford University');


CREATE TABLE Literary_Style(
        style_name CHAR(30),
        noun_frequency INTEGER NOT NULL CHECK (noun_frequency<100),
        adjective_frequency INTEGER NOT NULL CHECK (adjective_frequency <100),
        preposition_frequency INTEGER NOT NULL CHECK (preposition_frequency <100),
        verb_frequency INTEGER NOT NULL CHECK (verb_frequency <100),
        adverb_frequency INTEGER NOT NULL CHECK (adverb_frequency <100),
        determiner_frequency INTEGER NOT NULL CHECK (determiner_frequency <100),
        conjunction_frequency INTEGER NOT NULL CHECK (conjunction_frequency <100),
        pronoun_frequency INTEGER NOT NULL CHECK (pronoun_frequency <100),
        most_common_word CHAR(45) NOT NULL,
        PRIMARY KEY (style_name)
);

INSERT INTO Literary_Style values('Modernism', 30, 20, 10, 12, 13, 5, 3, 7, 'lonely');
INSERT INTO Literary_Style values('New Journalism', 32, 26, 12, 10, 5, 5, 5, 5, 'hair');
INSERT INTO Literary_Style values('British Romanticism', 15, 25, 10, 21, 19, 2, 2, 6,'laundry');
INSERT INTO Literary_Style values('Frankfurt School', 13, 23, 10, 14, 16, 17, 3, 4, 'time');
INSERT INTO Literary_Style values('Postmodernism', 22, 18, 24, 17, 4, 5, 6, 4, 'city');
INSERT INTO Literary_Style values('Naturalism', 26, 16, 22, 15, 6, 4, 7, 4, 'trees');

CREATE TABLE Written_In(
        title CHAR(60),
        style_name CHAR(30) NOT NULL,
        PRIMARY KEY (title),
        FOREIGN KEY (title) REFERENCES Text
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        FOREIGN KEY (style_name) REFERENCES Literary_Style
                ON DELETE CASCADE
                ON UPDATE CASCADE
);

INSERT INTO Written_In values('Rabbit Is Rich', 'Postmodernism');
INSERT INTO Written_In values('Portnoy’s Complaint', 'Postmodernism');
INSERT INTO Written_In values('The Plot Against America', 'Naturalism');
INSERT INTO Written_In values('Ulysses', 'Modernism');
INSERT INTO Written_In values('Tender Buttons', 'Modernism');
INSERT INTO Written_In values('Pride And Prejudice', 'British Romanticism');
INSERT INTO Written_In values('God Is Not Great', 'New Journalism');
INSERT INTO Written_In values('The Angel Esmeralda', 'Postmodernism');
INSERT INTO Written_In values('Cosmos', 'New Journalism');
INSERT INTO Written_In values('Negative Dialectics', 'Frankfurt School');
INSERT INTO Written_In values('Much Ado About Nothing', 'British Romanticism');


CREATE TABLE Word(
        word_name CHAR(45),
        word_type CHAR(15),
        PRIMARY KEY (word_name)
);

INSERT INTO Word values('lust', 'noun');
INSERT INTO Word values('passion', 'noun');
INSERT INTO Word values('fear', 'noun');
INSERT INTO Word values('lonely', 'adjective');
INSERT INTO Word values('went', 'verb');
INSERT INTO Word values('laundry', 'noun');
INSERT INTO Word values('hair', 'noun');
INSERT INTO Word values('city', 'noun');
INSERT INTO Word values('God', 'noun');
INSERT INTO Word values('space', 'noun');
INSERT INTO Word values('time', 'noun');
INSERT INTO Word values('wonderous', 'adjective');
INSERT INTO Word values('the', 'determiner');
INSERT INTO Word values('is', 'verb');
INSERT INTO Word values('are', 'verb');
INSERT INTO Word values('am', 'verb');
INSERT INTO Word values('a', 'determiner');
INSERT INTO Word values('trees', 'noun');
INSERT INTO Word values('and', 'conjunction');
INSERT INTO Word values('I', 'pronoun');


CREATE TABLE Contains(
        title CHAR(60),
        frequency INTEGER NOT NULL,
        word_name CHAR(45),
        PRIMARY KEY (title, word_name),
        FOREIGN KEY (title) REFERENCES Text
                ON DELETE CASCADE
                ON UPDATE CASCADE,
        FOREIGN KEY (word_name) REFERENCES Word
                ON DELETE CASCADE
                ON UPDATE CASCADE
);



INSERT INTO Contains values('Rabbit Is Rich', 65, 'lust');
INSERT INTO Contains values('Rabbit Is Rich', 63, 'the');
INSERT INTO Contains values('Portnoy’s Complaint', 63, 'passion');
INSERT INTO Contains values('Portnoy’s Complaint', 45, 'is');
INSERT INTO Contains values('The Plot Against America', 59, 'fear');
INSERT INTO Contains values('Ulysses', 72, 'lonely');
INSERT INTO Contains values('Ulysses', 60, 'are');
INSERT INTO Contains values('Tender Buttons', 49, 'went');
INSERT INTO Contains values('Pride And Prejudice', 64, 'laundry');
INSERT INTO Contains values('Pride And Prejudice', 59, 'a');
INSERT INTO Contains values('God Is Not Great', 72, 'God');
INSERT INTO Contains values('God Is Not Great', 46, 'trees');
INSERT INTO Contains values('The Angel Esmeralda', 57, 'city');
INSERT INTO Contains values('The Angel Esmeralda', 52, 'and');
INSERT INTO Contains values('Negative Dialectics', 23, 'time');
INSERT INTO Contains values('Negative Dialectics', 21,'I');
INSERT INTO Contains values('Cosmos', 57, 'space');
INSERT INTO Contains values('Much Ado About Nothing', 72, 'wonderous');

"""

#Maurice: This is the pre-GET request, used to connect to the database (like establishing a TCP connection to server in lab7)
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

#Maurice: this is post-GET request, closes the database connection (like closing TCP connection in lab7)
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
#
@app.route('/')
def index():
  """ 
  request is a special object that Flask provides to access web request information:
  These methods are used to gather information about the HTML GET request coming from the browser
the server, since it's a server, isn't requesting anything itself. Only the browser is requesting something.

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args

  #TO ZANE: This is an example of a database query
  #since this is on the index page(as directed by @app.route('/') function), this is the query that will be made immediately when you first hit the site
  #We don't need to query anything when we first hit the site, so we don't need this query in our
  #index method.
  cursor = g.conn.execute("SELECT name FROM test")

  #Maurice: below is how you add the info gathered from the SQL query into an array(?) in python
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()
  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
@app.route('/another')
def another():
  return render_template("another.html")

#Maurice: we won't need to add new data to the database so we won't need this.
#Maurice: but this is a good example of how to send SQL to the database in response to
#Maurice: end-user input on the HTML, using Flask(@app.route) and SQLAlchemy(g.conn.execute)
#@app.route('/add', methods=['POST'])
#def add():
#  name = request.form['name']
#  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
#  return redirect('/')


#This is Terra's example of a search query
@app.route('/search', methods=['POST'])
def search():
  name = request.form['name']
  cursor = g.conn.execute('SELECT * FROM books WHERE author = \'%s\';', name)

  titles = []  
  for c in cursor:
    titles.append(c['title'])

    context = dict(data = titles)
    return render_template("index.html", **context)


  return redirect('/')

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


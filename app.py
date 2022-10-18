import os
import re
import shutil
import csv
import sys
import pyodbc
from io import BytesIO
# from turtle import title, width
from flask import Flask,render_template, url_for, flash, redirect, request
# from flask_wtf import FlaskForm
# from flask_wtf.file import FileField, FileRequired, FileAllowed
# from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_bootstrap import Bootstrap
# from wtforms import StringField, IntegerField, SubmitField, SelectField
# from wtforms.validators import DataRequired
from PIL import Image

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = '0626fuyi'
server = 'notminusone.database.windows.net'
database = 'notminusoneDatabase'
username = 'not-1'
password = '0626Fuyi' 
driver= '{ODBC Driver 18 for SQL Server}'
# ROUTES!
@app.route('/')
def part10():
	return render_template('part10.html',part10_active="active",title="Part 10")

@app.route('/part11')
def part11():
	pic_list = []
	# url_list = ["https://jxh1896.blob.core.windows.net/jxh1896/chip.jpg","https://jxh1896.blob.core.windows.net/jxh1896/curly.png","https://jxh1896.blob.core.windows.net/jxh1896/moe.jpg","https://jxh1896.blob.core.windows.net/jxh1896/pluto.jpg"]
	url_list = ["static/alice.jpg","static/pluto.jpg","static/mars.jpg","static/curly.png","static/moe.jpg","static/chip.jpg"]
	for url in url_list:
		# response = requests.get(url)
		# img = Image.open(BytesIO(response.content))	
		img = Image.open(url)	
		width = img.width
		height = img.height
		name = url.split('/', 2)[-1]
		pic_list.append({
			'name': name,
			'width': width,
			'height': height
		})
	return render_template('part11.html',part11_active = "active",pic_list=pic_list,title="Part 11")

@app.route('/part12',methods=['GET','POST'])
def part12():
	if request.method=='GET':
		return render_template('part12.html',part12_active = "active",title="Part 12")
	if request.method=='POST':
		name = request.form["name"]
		cnxn = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
		cursor = cnxn.cursor()
		cursor.execute("select Name,Keywords,Picture from data where Name=?",name)
		row = cursor.fetchone()
		if row is not None:
			return render_template('part12.html',part12_active = "active",data = {
				'name':row[0],
				'keywords':row[1],
				'picture':row[2]
			})
		else:
			return render_template('part12.html',part12_active = "active",information="no information or picture available",title="Part 12")

@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
	return render_template('404.html',title='404')

@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
	return render_template('500.html',title='500')


if __name__ == '__main__':
	app.run()
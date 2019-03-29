from flask import Flask, render_template, request, redirect
import datetime
import pytz # timezone 
import requests
import os

from bs4 import BeautifulSoup
import collections

WeatherReport = collections.namedtuple('WeatherReport',
                                           'condition,temp,scale,loc')


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home_page():
	return render_template('index.html')

@app.route('/<name>')
def profile(name):
	return render_template('index.html', name=name)


@app.route('/add_numbers', methods=['GET','POST'])
def add_numbers_post():
	  # --> ['5', '6', '8']
	  # print(type(request.form['text']))
	  if request.method == 'GET':
	  	return render_template('add_numbers.html')
	  elif request.method == 'POST':
  	      print(request.form['text'].split())
  	      total = 0
  	      try:
  	      	for str_num in request.form['text'].split():
  	      		total += int(str_num)
  	      	return render_template('add_numbers.html', result=str(total))
  	      except ValueError:
  	      	return "Easy now! Let's keep it simple! 2 numbers with a space between them please"


@app.route('/shopping_list', methods=['GET','POST'])
def shopping_list_post():
	  # --> ['5', '6', '8']
	  # print(type(request.form['text']))

    if request.method == 'GET':
      return render_template('shopping_list.html')
    elif request.method == 'POST':
          print(request.form['text'].split())
          
          shop_list = []
          try:
            for item in request.form['text'].split():
              
              shop_list.append(item)

              
              
            return render_template('shopping_list.html', result="\n".join([str(item) for item in shop_list]))
          except ValueError:
            return "Easy now! Let's keep it simple! Just words with a space between them"
          
  	      
@app.route('/time', methods=['GET','POST'])
def time_post():
    # --> ['5', '6', '8']
    # print(type(request.form['text']))

    if request.method == 'GET':
      return render_template('time.html')
    elif request.method == 'POST':
          print(request.form['text'].split())
          
          for item in request.form['text'].split():
            answer = (datetime.datetime.now(pytz.timezone("Europe/Dublin")).strftime('Time = ' + '%H:%M:%S' + ' GMT ' + ' Year = ' + '%d-%m-%Y'))
            #answer = datetime.datetime.now().strftime('Time == ' + '%H:%M:%S' + ' Year == ' + '%d-%m-%Y')
            #answer = datetime.datetime.now().strftime('%Y-%m-%d \n %H:%M:%S')

              
              
            return render_template('time.html', result=answer)


@app.route('/weather', methods=['GET', 'POST'])
def weather_post():
    # --> ['5', '6', '8']
    # print(type(request.form['text']))


    if request.method == 'GET':
        return render_template('temperature.html')
    elif request.method == 'POST':
        print(request.form['text'])

        # Declare Header
        # Get zipcode input from user
        # Display the  weather at that location

        zip_code = request.form['text']
        # print(zip_code)
        html = get_html_from_web(zip_code)
        # print(html)
        report = weather_from_html(html)
        complete_weather= 'The Temperature in {} is {} {} {}'.format(
            report.loc, report.temp, report.scale, report.condition)

    return render_template('temperature.html', result=complete_weather)


def print_header():
    print("+++++++++++++++++++++++++++++++++++++++++++")
    print("Welcome to Chaitanya's Weather Application")
    print("+++++++++++++++++++++++++++++++++++++++++++")

def get_html_from_web(zip_code):
    full_url = "https://www.wunderground.com/weather-forecast/{}".format(zip_code)
    # print(full_url)
    response = requests.get(full_url)
    # print(response.status_code)
    return response.text

def weather_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    loc = soup.find(class_='region-content-header').find('h1').get_text()
    condition = soup.find(class_='condition-icon').get_text()
    temp = soup.find(class_='wu-unit-temperature').find(class_='wu-value').get_text()
    scale = soup.find(class_='wu-unit-temperature').find(class_='wu-label').get_text()
    loc = cleanup_text(loc)
    condition = cleanup_text(condition)
    temp = cleanup_text(temp)
    scale = cleanup_text(scale)
            # return condition, temp, scale, loc
    report = WeatherReport(condition=condition, temp=temp, scale=scale, loc=loc)
    return report


def cleanup_text(text):
    if not text:
        return text
    else:
        text = text.strip()
        return text


@app.route('/python_apps')
def python_apps_page():
	# testing stuff
	return render_template('python_apps.html')


@app.route('/blog', methods=['GET'])
def blog_page():
  return render_template('blog.html')


if __name__ == '__main__':
	app.run(debug=True)


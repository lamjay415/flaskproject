from flask import Flask, render_template, request
import json
import pandas as pd
import urllib
import matplotlib.pyplot as plt
import numpy as np
from pandas.io.json import json_normalize 

app = Flask(__name__)
# Your Code Goes Here.
@app.route('/')
def main():
    return render_template('template.html')

@app.route('/result',methods=['GET','POST'])
def result():
    city = request.form['city']
    code = request.form['code']
    zipcode = request.form['zip']
    url = ('http://api.openweathermap.org/data/2.5/weather?zip=%s,%s&APPID=8eb35225ff2aec9c2e45f79c37aa91e8&units=imperial' 
           % (zipcode,code))
    ret = json.loads(urllib.request.urlopen(url).read())
    temp = json.dumps(ret['main']['temp'])
    icon = json.dumps(ret['weather'][0]['icon'])
    icon = icon.replace('"',"")
    url2 = ('http://api.openweathermap.org/data/2.5/forecast?zip=%s,%s&APPID=8eb35225ff2aec9c2e45f79c37aa91e8&units=imperial' 
               % (zipcode,code))
    ret2 = json.loads(urllib.request.urlopen(url2).read())
    df = json_normalize(ret2,'list')
    new_df = pd.concat([df.drop(['main'],axis=1), df['main'].apply(pd.Series)],axis=1)
    final = new_df[['dt_txt','temp']]
    ax = final.plot(x='dt_txt',y='temp',title='Visual graph of temperatures in 3 hours intervals of the past five days')
    ax.set_ylabel('Fahrenheit')
    ax.set_xlabel('3 hour intervals')
    plt.savefig('static/'+city+'.png',bbox_inches='tight')
    return render_template('result.html',temp = temp, icon = icon,city=city)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
if __name__ == '__main__':
  app.debug = True	
  app.run()



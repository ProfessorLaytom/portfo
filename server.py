from flask import Flask, render_template, url_for, request, redirect
import os
import smtplib
from email.message import EmailMessage
from string import Template  
from pathlib import Path
from textwrap import fill
import csv

app = Flask(__name__)

def send_mail(form_dict):
    name = form_dict['name']
    html = Template(Path('mail_template.html').read_text())
    email = EmailMessage()
    email['from'] = 'Un admirateur tres secret wink wink'
    email['to'] = 'give.me.forms@gmail.com'
    email['subject'] = f'[WEBSITE] you have a message from {name}'
    email.set_content(html.substitute(form_dict), 'html')
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('give.me.forms@gmail.com', '08/09/1997toM')
        smtp.send_message(email)
    print('all good !')

def save_data(form_dict):
    with open('database.txt', mode='a') as database:
        name, email, subject, message = form_dict['name'], form_dict['email'], form_dict['subject'], form_dict['message']
        database.write(fill(f'Name: {name}')+'\n')
        database.write(fill(f'Email: {email}')+'\n')
        database.write(fill(f'Subject: {subject}')+'\n')
        database.write(fill(f'Message: {message}')+'\n')
        database.write('\n')
        database.write('*******************\n')
        database.write('\n')

def save_data_csv(form_dict):
    with open('database.csv', mode='a', newline='') as database:
        name, email, subject, message = form_dict['name'], form_dict['email'], form_dict['subject'], form_dict['message']
        writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([name, email, subject, message])


@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def my_home_index(page_name):
    return render_template(f'{page_name}')

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            form_dict = request.form.to_dict()
            save_data_csv(form_dict)
            send_mail(form_dict)
            return render_template('/thankyou.html', name=form_dict['name'])
        except:
            return 'Did not save to database'
    else:
        return 'something went wrong, please try again.'




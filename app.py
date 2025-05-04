from flask import Flask, request,render_template, redirect,session,flash,url_for
from flask_sqlalchemy import SQLAlchemy
import bcrypt,re,os,csv
# from sqlalchemy.orm import relationship
from werkzeug.utils import secure_filename
# from flask_wtf import FlaskForm
# from wtforms import StringField, TextAreaField
# from wtforms.validators import InputRequired
from sqlalchemy.orm.exc import NoResultFound
from flask import Flask, render_template, request, session, redirect, url_for
from celery import Celery
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from collections import defaultdict
import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time


from flask import Flask
from celery import Celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker='redis://localhost:6379/0')

celery.conf.update(app.config)



project_dir=os.path.dirname(os.path.abspath(__file__))
database_file=f"sqlite:///{os.path.join(project_dir,'database.db')}"

#app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)
app.secret_key = 'secret_key'
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuration
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')



UPLOAD_FOLDER = 'static/images'  # Update with your desired upload folder
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, UPLOAD_FOLDER)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self,email,password):
        # self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

class csv_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email =db.Column(db.String(100), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    

class manual_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email =db.Column(db.String(100), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True,unique=True)
    template_name=db.Column(db.String(100))
    purpose = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    style = db.Column(db.String(100), nullable=False)
    content=db.Column(db.Text)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True,unique=True)
    campaign_name = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    content=db.Column(db.Text)

    

@app.route('/add_template',methods=['GET','POST'])
def add_template():
    if request.method == 'POST':
        template_name = request.form.get('template_name')
        purpose= request.form.get('purpose')
        industry = request.form.get('industry')
        style= request.form.get('style')
        content = request.form.get('content')
        template = Template(template_name=template_name,purpose=purpose,industry=industry,style=style,content=content)
        db.session.add(template)
        db.session.commit()
        return render_template('add_tem.html')
    return render_template('add_tem.html')
    

with app.app_context():
    db.create_all()


def passwordcheck(password):
    # Check if password meets certain criteria for strength
    if len(password) < 8:
        return False
    elif not re.search("[a-z]", password):
        return False
    elif not re.search("[A-Z]", password):
        return False
    elif not re.search("[0-9]", password):
        return False
    elif not re.search("[!@#$%^&*()_+]", password):
        return False
    return True




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(email)
        if not passwordcheck(password):
            error = 'Password must be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, one digit, and one special character.'
        else:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                error = 'Email already exists. Please try again.'
            else:
                # If email doesn't exist, proceed with registration
                new_user = User(email=email,  password=password)  
                db.session.add(new_user)
                db.session.commit()
                return redirect('/login')

    return render_template('register.html', error=error)

@app.route('/login',methods=['GET','POST'])
def login():
    error = None 
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/dashboard')
        else:
            error = 'Invalid email or password. Please try again.'

    return render_template('login.html', error=error)

@app.route('/reset',methods=['GET','POST'])
def reset():
    check = None
    if request.method == "POST":
        email = request.form["email"]
        existing_user = User.query.filter_by(email=email).first()
        print(email)
        if existing_user:
            
            new_password = request.form["password"]
            # Update the existing user's password
            existing_user.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            db.session.commit()
            print("password reset")
            return redirect('/login')
        else:
            check = "Email not exist"
    return render_template('resetpw.html',check=check)

@app.route('/dashboard')
def dashboard():
    if session['email']:
        
        user = User.query.filter_by(email=session['email']).first()
        email= session['email']
        return render_template('dash.html',user=user,email=email)
    
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')

@app.route('/contact_option', methods=['GET', 'POST'])
def contact_option():
    if request.method == 'POST':
        option = request.form.get('contactOption') 
        if option == 'csv':
            return redirect(url_for('csv_file')) 
        elif option == 'manual':
            return redirect(url_for('manual'))
    email = session.get('email') 
    return render_template('aud.html',email=email)

@app.route('/csv_file', methods=['GET', 'POST'])
def csv_file():
    error =None
    status = None
    csvdata = None
    error1 = None
    email= session['email']
    if 'email' not in session:
        return redirect('/login')  # Redirect to login page if user is not logged in

    if request.method == 'POST':
        # Get the user's email from the session
        email = session['email']

        # Retrieve the user from the database based on the email
        user = User.query.filter_by(email=email).first()

        # Check if the user exists
        if not user:
            error= 'User not found'

        # Check if the post request has the file part
        if 'file' not in request.files:
            error= 'No file part'

        file = request.files['file']

        # If user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            error= 'No selected file'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Process the uploaded CSV file and save data to the database
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    # Assuming 'id', 'name', 'email' are the headers in CSV file
                    
                    name = row['name']
                    email = row['email']
                    
                    existing_data = csv_data.query.filter_by(email=email).first()
                    if existing_data:
                        # Handle duplicate email appropriately
                        # For example, you can skip inserting or update existing record
                        error1 = "Already exists"
                        continue
                    # Save data to the database, associating it with the logged-in user
                    else:
                        csvdata = csv_data( name=name, email=email, user_id=user.id)
                        db.session.add(csvdata)
                        db.session.commit()
                        status = 'CSV file uploaded successfully'
    return render_template('csv_file.html',email=email,data=csvdata,error=error,error1=error1,status=status)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}


@app.route('/list')
def list():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        email= session['email']
        csv_data_list = csv_data.query.filter_by(user_id=user.id).all()
        manual_data_list = manual_data.query.filter_by(user_id=user.id).all()
        combine = csv_data_list + manual_data_list
        return render_template('list.html', data=combine,email=email)
    return redirect('/login')

@app.route('/manual', methods=['GET', 'POST'])
def manual():
    error = None
    status = None
    email = None
    data = None
    if request.method == 'POST':
        # Get the user's email from the session
        email = session['email']

        # Retrieve the user from the database based on the email
        user = User.query.filter_by(email=email).first()

        # Check if the user exists
        if not user:
            error= 'User not found'
        else:
            name = request.form['name']
            email = request.form['email']
            data = manual_data(name=name,email=email,user_id=user.id)
            db.session.add(data)
            db.session.commit()
            status = 'Data upload successfully'
    return render_template('aud_manual.html',email=email,data=data,error=error,status=status)




@app.route('/select_template' , methods=['GET', 'POST'])
def select_template():
    if request.method == "POST":
        purpose = request.form.get('purpose')
        print(purpose)
        industry = request.form.get('industry')
        style = request.form.get('style')
        sel_temp = Template.query.filter_by(purpose=purpose,industry=industry,style=style).first()
        if not sel_temp:
            return "not Found"
        else:
            return redirect(url_for('edit_template', template_id=sel_temp.id))
    return render_template('select_template.html')


@app.route('/edit_template/<int:template_id>', methods=['GET', 'POST'])
def edit_template(template_id):
    status=None
    template = Template.query.get_or_404(template_id)
    print(template)
    if request.method == 'POST':
        # Process form submission to save changes
        template_name= request.form.get('template_name')
        updated_content = request.form.get('content')
        cloned_template = Template(purpose=template.purpose,industry=template.industry, style=template.style,template_name=template_name, content=updated_content)
        
        # Add the cloned template to the session
        db.session.add(cloned_template)
       
        # Commit changes to the database
        db.session.commit()
        # Redirect to a confirmation page or any other appropriate page
        status="Saved Template!!"
        return render_template('edit_template.html', template=template,status=status)
    else:
        
        return render_template('edit_template.html', template=template)

@app.route('/saved_template', methods=['GET','POST'])
def saved_template():
    template = Template.query.all()
    return render_template('save_template.html',template=template)

@app.route('/create_campaign/<int:template_id>',methods=['GET','POST'])
def create_campaign(template_id):
    template = Template.query.get_or_404(template_id)
    print(template)
    status=None
    
    if request.method == "POST":
        campaign_name = request.form.get("campaign_name")
        print(campaign_name)
        subject = request.form.get("subject")
        content = request.form.get('content')
        create_camp = Campaign(campaign_name=campaign_name,subject=subject,content=content)
        db.session.add(create_camp)
        db.session.commit()
        if not create_camp  :
            status= "error"
        else:
            status="submit"
    return render_template('create_campaign.html',template=template,status=status)

@app.route('/campaign_list', methods=['GET','POST'])
def campaign():
    camp = Campaign.query.all()
    return render_template('camp_list.html',campaign=camp)


def get_recipients():
    csv = csv_data.query.all()
    manual = manual_data.query.all()
    
    all_recipients = []
    for recipient in csv:
        all_recipients.append(recipient.email)
    print(all_recipients)
    for recipient in manual:
        all_recipients.append(recipient.email)
    print(all_recipients)
    return all_recipients


from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, campaign_name, recipient_email,campaign_content):
    SMTP_SERVER = 'email-smtp.ap-south-1.amazonaws.com'
    SMTP_PORT = 587
    SMTP_USERNAME = 'AKIAYPRDIK6JKBW57QLJ'
    SMTP_PASSWORD = 'BJrTDmRd5VSlPSM4n0Aszi83O3mau4aVm27Es6u+PCOq'
    SMTP_FROM = 'tayyabali@tayyabali.in'

    msg = MIMEMultipart()
    msg['From'] = SMTP_FROM
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Create an HTML MIMEText object
    html_content = f"<html><body><p>Hello,</p><p>You have received a new email from the '{campaign_name}' campaign.</p>{campaign_content}</body></html>"
    html_part = MIMEText(html_content, 'html')

    # Attach the HTML content to the message
    msg.attach(html_part)

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_FROM, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully to", recipient_email)
        return True
    except Exception as e:
        print("Error sending email to", recipient_email, ":", e)
        return False



# Import Celery instance from app.py
from app import celery

# Define the send_scheduled_email task
@celery.task
def send_scheduled_email(subject, recipients, content):
    for recipient in recipients:
        send_email(subject, recipient, content)


# from flask import render_template, request, redirect, url_for
# from app import app, celery, send_scheduled_email






@app.route('/campaign_scheduling/<int:campaign_id>', methods=['GET', 'POST'])
def campaign_scheduling(campaign_id):
    try:
        # Retrieve the campaign object from the database
        campaign = Campaign.query.get_or_404(campaign_id)
        
        # Fetch other necessary data
        email = session['email']
        sender_email = session.get('sender_email')
        campaign_name = session.get('campaign_name')
        subject = session.get('subject')

        # Fetch email addresses from csv_data and manual_data tables
        recipients_csv = csv_data.query.all()
        recipients_manual = manual_data.query.all()
        
        # Combine the email addresses from both tables
        all_recipients = recipients_csv + recipients_manual

        # Extract email addresses from recipients
        recipients_emails = [recipient.email for recipient in all_recipients]

        status = None  # Initialize status variable with default value

        if request.method == 'POST':
            action = request.form.get('action')
            if action == 'schedule':
                # Extract form data
                selected_recipients = request.form.getlist('recipients')
                scheduled_date = request.form.get('scheduled_date')
                scheduled_time = request.form.get('scheduled_time')
                
                
                # Schedule the Celery task to send the email
                
                send_scheduled_email.apply_async(args=[campaign.subject, selected_recipients, campaign.content,email], eta=f"{scheduled_date}T{scheduled_time}")
                print(scheduled_date,scheduled_time)
                
                return render_template('scheduling.html',campaign=campaign,scheduled_date=scheduled_date,scheduled_time=scheduled_time)
            elif action == 'send_now':
                # Send emails immediately
                for recipient in all_recipients:
                    send_email(campaign.subject,campaign.campaign_name, recipient.email, campaign.content)

                status = "Emails sent successfully"

        # Pass the campaign object and recipients' email addresses to the template context
        return render_template('campaign_scheduling.html',email=email, sender_email=sender_email, recipients=recipients_emails, campaign=campaign, campaign_name=campaign.campaign_name, subject=campaign.subject, status=status)
    except NoResultFound:
        # Handle the case where the campaign with the given ID is not found
        flash('Campaign not found.', 'error')
        return redirect('/some_other_page')  # Redirect to a different page or render an error template
    
    


@celery.task
def send_scheduled_email(email,subject, recipients, content):
    for recipient in recipients:
        send_email(email,subject, recipient, content)
        

@app.route('/scheduled_success')
def scheduled_success():
    return render_template('scheduled_success.html')


@app.route('/preview/<int:campaign_id>')
def preview(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    return render_template("preview.html",campaign=campaign)



def generate_pie_chart(data, title):
    labels = data.keys()
    sizes = data.values()

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title(title)

    # Convert plot to base64 encoding
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    b64_image = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    return b64_image

@app.route('/analytics')
def analytics():
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        email= session['email']
        csv_data_list = csv_data.query.filter_by(user_id=user.id).all()
        manual_data_list = manual_data.query.filter_by(user_id=user.id).all()
        combine = csv_data_list + manual_data_list
        
        
        combine_data=defaultdict(int)
        for data in combine:
            combine_data[data.email] += 1

        
        combine_data_chart = generate_pie_chart(combine_data,"All contact")

    return render_template('analytics.html', data=combine, email=email, combine_data_chart=combine_data_chart)



if __name__ == '__main__':
    app.run(debug=True)
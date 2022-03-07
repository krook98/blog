from flask import Flask, render_template, request
import requests
import smtplib
import os

app = Flask(__name__)
posts = requests.get("https://api.npoint.io/1581d18ce8f2adc6be48").json()

MY_MAIL = os.environ.get('MY_MAIL')
MY_PASSWORD = os.environ.get('MY_PASSWORD')
RECIPENT = os.environ.get('RECIPENT')


@app.route('/')
def home():
    return render_template('index.html', all_posts=posts)


@app.route('/about')
def about_me():
    return render_template('about.html')


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        data = request.form
        send_mail(name=data['name'], email=data['email'], phone=data['phone'], message=data['message'])
        return render_template('contact.html', msg_sent=True)
    return render_template('contact.html', msg_sent=False)


@app.route('/post/<int:index>')
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


def send_mail(name, email, phone, message):
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=MY_MAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_MAIL,
                                   to_addrs=RECIPENT,
                                   msg=f"Subject: New Message\n\n Name: {name}\n Email: {email}\n "
                                       f"Phone: {phone}\n {message}")


if __name__ == "__main__":
    app.run(debug=True)
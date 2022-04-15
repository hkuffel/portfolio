import os

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_assets import Bundle, Environment
from flask_mail import Message, Mail
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

mail_settings: dict = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['MAIL_USERNAME'],
    "MAIL_PASSWORD": os.environ['MAIL_PASSWORD']
}

app.config.update(mail_settings)
mail = Mail(app)

assets = Environment(app)

# TAILWIND CONFIG
if os.environ['FLASK_ENV'] != 'production':
    dirname: str = os.getcwd()
    assets.config['postcss_bin']: str = f'{dirname}/node_modules/postcss-cli/bin/postcss'
css: Bundle = Bundle("src/main.css", output="dist/main.css", filters="postcss")
assets.register("css", css)
css.build()


class ContactForm(FlaskForm):
    """Contact form."""
    name = StringField(
        'Name',
        [DataRequired()]
    )
    email = StringField(
        'Email',
        [
            Email(message=('Not a valid email address.')),
            DataRequired()
        ]
    )
    message = TextAreaField(
        'Message',
        [
            DataRequired(),
            Length(min=4, message=('Your message is too short.'))
        ]
    )
    submit = SubmitField('Send')


@app.route("/")
def homepage():
    form: ContactForm = ContactForm()
    return render_template("index.html", form=form)


@app.get("/success")
def success():
    return render_template("success.html")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    app.logger.info('the name is %s', form.name.data)
    app.logger.info('the email is %s', form.email.data)
    app.logger.info('the message is %s', form.message.data)
    if form.validate_on_submit():
        app.logger.info('form was validated on submission')
        msg = Message(
            "Someone filled out the contact form on kuffel.dev",
            sender=os.environ['MAIL_USERNAME'],
            recipients=[os.environ['MAIL_RECIPIENT']]
        )
        msg.body = f"From: {form.name.data} <{form.email.data}>\n\n{form.message.data}"
        mail.send(msg)
        return redirect("/success")
    else:
        flash('Something went wrong.')
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)

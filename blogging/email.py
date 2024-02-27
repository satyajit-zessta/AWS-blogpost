from django.conf import settings
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

def sendEmail(email, author_name,commentor,title, date, content):
    port = settings.EMAIL_PORT
    smtp_server = settings.EMAIL_HOST
    login = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD

    sender_email = "satyajit.prusty@zessta.com"  # paste your sender email
    receiver_email = email
    message = MIMEMultipart("alternative")
    message["Subject"] = f"{commentor} Commented - Zessta"
    message["From"] = sender_email
    message["To"] = receiver_email
    html = """\
 
<html lang="en">
 
  <body>
    <img src="cid:ZesstaLogo" width="200px" />
    <h1>Zessta Blogpost Services</h1>
    <p>
      Dear {author}, <br>
      '<b><em>{commentor}</em></b>' has commented on your post as <br><em>"{content}"</em> <hr><b>Titled: </b>{title} <br> <b>Date:</b> {date}.
    </p>
    <br />
    <p>Thank you for using Zessta Blogpost Services.</p>
    <br />
    <p>
      Regards,<br />
      Zessta Blogpost Services, Hyderabad,
    </p>
  </body>
</html>

    """.format(author=author_name, commentor = commentor, title = title,  date = date, content=content)

    part = MIMEText(html, "html")
    message.attach(part)


    fp = open(r"blogging\static\logo.png", "rb")
    image = MIMEImage(fp.read())
    fp.close()

    # Specify the  ID according to the img src in the HTML part
    image.add_header("Content-ID", "<ZesstaLogo>")
    message.attach(image)
    context = ssl.create_default_context()
    # send your email
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    return True

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# me == my email address
# you == recipient's email address
me = "prasad@tgcworld.com"
you = "prasade.uk@email.com"
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Link"
msg['From'] = me
msg['To'] = you

# Create the body of the message (a plain-text and an HTML version).
text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.

# Send the message via local SMTP server.
mail = smtplib.SMTP('imap.mail.yahoo.com', 993)

mail.ehlo()

mail.starttls()

mail.login(me, 'Jaya@123')
mail.sendmail(me, you, msg.as_string())
mail.quit()
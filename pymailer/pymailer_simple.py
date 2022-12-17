
import smtplib

reciver_email= 'reciver@outlook.com' # Who you are sending the message to

sender_email = 'sender@gmail.com' # Your email

password = '*****' # Your email account password
message = 'This is my message ' # The message in the email

server = smtplib.SMTP('smtp.gmail.com', 587) 
# Connect to the server

server.starttls() # Use TLS
server.login(sender_email, password) # Login to the email server
server.sendmail(sender_email, reciver_email , message) # Send the email
server.quit() # Logout of the email server

from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives 
from django.template.loader import render_to_string

def sendEmail(context, extras):
    try:
        settings.EMAIL_HOST = 'mail.startall.net'
        settings.EMAIL_PORT = 465
        settings.EMAIL_HOST_USER = 'passwordreset@startall.net'
        settings.EMAIL_HOST_PASSWORD = 'j5hBhD[[kTCT'
        unknown_user = context.user
        
        send_mail(
            f"Unauthorized Access!",
            f"Click the link to give {unknown_user} access to your file {(extras if extras != None else context.user)}",
            "noreply@emailmgt.com",
            ["richiedilosi2003@gmail.com"],
            fail_silently=False,
        )
        return "sent"
    except Exception as e:
        return "Not Successfull"


# DateTime converter function[d DD MM YY]
def datetime_converter(dt):
    """
        The function `datetime_converter` takes a datetime object as input and returns a formatted date
        string in the format "Day DD Month YYYY".
        
        :param dt: The parameter `dt` is a datetime object that represents a specific date and time
        :return: a formatted date string in the format "Day Month Year".
    """
    dt_object = datetime.strptime(str(dt), "%Y-%m-%d %H:%M:%S.%f%z")
    formatted_date = dt_object.strftime("%a %d %b %Y")
    return formatted_date

def process_large_list(email_data, name_data, chunk_size=4):
    total_email_items = len(email_data)
    total_name_items = len(name_data)
    
    email_chunks = [email_data[i:i + chunk_size] for i in range(0, total_email_items, chunk_size)]
    name_chunks = [name_data[j:j + chunk_size] for j in range(0, total_name_items, chunk_size)]
    
    for email_chunk, name_chunk in zip(email_chunks, name_chunks):
        process_chunk(email_chunk, name_chunk)

def process_chunk(chunk_1, chunk_2):
    success_email_list = []
    counter = 0
    for email_addr, name in zip(chunk_1, chunk_2):
        html_content = render_to_string('email_temp.html', {'name': name})
        msg = EmailMultiAlternatives(
            subject='Test Email',
            body='This is a test',
            from_email=settings.EMAIL_HOST_USER,
            to=[email_addr]
        )
        msg.attach_alternative(html_content, 'text/html')

        msg.send()
        counter += 1
        print(f'---> Email sent to {email_addr}\ncount={counter}')
        success_email_list.append(email_addr)

    process_item(success_email_list)

def process_item(item):
    print(f"Email sent successfully to list: {item}")


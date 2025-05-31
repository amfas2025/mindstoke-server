from flask import current_app, render_template, url_for
from flask_mail import Message
from threading import Thread

def send_async_email(app, msg):
    """Send email asynchronously."""
    with app.app_context():
        try:
            print(f"Sending email to: {msg.recipients}")
            current_app.mail.send(msg)
            print("Email sent successfully!")
        except Exception as e:
            current_app.logger.error(f"Error sending email: {str(e)}")
            raise

def send_email(subject, recipients, html_body, text_body=None):
    """Send an email."""
    msg = Message(subject, recipients=recipients)
    msg.html = html_body
    if text_body:
        msg.body = text_body

    # Send email asynchronously
    Thread(
        target=send_async_email,
        args=(current_app._get_current_object(), msg)
    ).start()

def send_hhq_invitation(client, hhq_response):
    """Send HHQ invitation email to client."""
    subject = "Complete Your Health History Questionnaire - Mind Stoke AI"

    # Generate HHQ link
    hhq_link = current_app.config['BASE_URL'] + url_for(
        'hhq.hhq_form',
        token=hhq_response.unique_token,
        _external=False
    )

    # Render email template
    html = render_template(
        'email/hhq_invitation.html',
        client=client,
        hhq_link=hhq_link,
        expires_at=hhq_response.expires_at
    )

    # Send email
    send_email(
        subject=subject,
        recipients=[client['email']],
        html_body=html
    ) 
import socket
from datetime import datetime
import base64
from email.mime.text import MIMEText
from api.config import settings

from api.services.email_service import GmailEmailService

def send_startup_notification_email():
    """
    Send a startup notification email to the specified email address.
    
    This function can be called during application startup to send 
    a notification email with system details.
    
    :return: Dictionary with email sending result
    """
    try:
        hostname = socket.gethostname()
        startup_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if not settings.gmail_startup_notification_email:
            print("No startup notification email configured. Skipping email sending.")
            return {
                'success': True,
                'message': 'No email configured for startup notifications.'
            }
        
        message = MIMEText(f"""
        Application Startup Notification

        Hostname: {hostname}
        Startup Time: {startup_time}
        
        The backend application has successfully started.
        """, 'plain')
        
        message['to'] = settings.gmail_startup_notification_email
        message['subject'] = 'Backend Application Startup Notification'
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        # Send message using static method
        result = GmailEmailService.send_password_reset_email(
            recipient_email=settings.gmail_startup_notification_email,
            reset_link=f"Startup Notification - Hostname: {hostname}, Time: {startup_time}",
            sender_email='me'
        )
        
        if result['success']:
            print(f"Startup email sent successfully. Message ID: {result.get('message_id')}")
            return {
                'success': True,
                'message_id': result.get('message_id'),
                'hostname': hostname,
                'startup_time': startup_time
            }
        else:
            print(f"Failed to send startup email: {result.get('error')}")
            return result
    
    except Exception as e:
        print(f"Failed to send startup email: {e}")
        return {
            'success': False,
            'error': str(e)
        }
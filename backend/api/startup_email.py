import socket
from datetime import datetime

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
                "success": True,
                "message": "No email configured for startup notifications.",
            }

        content = f"""
Application Startup Notification

Hostname: {hostname}
Startup Time: {startup_time}
        
The backend application has successfully started.
        """

        # Send message using send_email method
        result = GmailEmailService.send_email(
            recipient_email=settings.gmail_startup_notification_email,
            subject="Backend Application Startup Notification",
            content=content,
        )

        if result["success"]:
            print(
                f"Startup email sent successfully. Message ID: {result.get('message_id')}"
            )
            return {
                "success": True,
                "message_id": result.get("message_id"),
                "hostname": hostname,
                "startup_time": startup_time,
            }
        else:
            print(f"Failed to send startup email: {result.get('error')}")
            return result

    except Exception as e:
        print(f"Failed to send startup email: {e}")
        return {"success": False, "error": str(e)}

import base64
import os
from typing import Optional, Dict, Any, List, Union

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from api.config import settings
from api.storage.models import Assignment, AssignmentRequest
from dotenv import load_dotenv

load_dotenv()

class GmailEmailService:
    """
    Static email service using Gmail API with OAuth 2.0 authentication
    
    Requires:
    - Google Cloud Project with Gmail API enabled
    - OAuth 2.0 credentials file
    """
    
    # Gmail API scopes for sending emails
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    
    @staticmethod
    def _get_credentials(
        refresh_token: str,
        client_id: str,
        client_secret: str,
        token_uri: str = 'https://oauth2.googleapis.com/token'
    ) -> Credentials:
        """
        Obtain OAuth 2.0 credentials using refresh token
        
        :param refresh_token: OAuth refresh token
        :param client_id: OAuth client ID
        :param client_secret: OAuth client secret
        :param token_uri: Token endpoint URL
        :return: Google OAuth Credentials
        """
        credentials = Credentials(
            None,
            refresh_token=refresh_token,
            token_uri=token_uri,
            client_id=client_id,
            client_secret=client_secret
        )
        
        # Refresh the credentials to get a new access token
        credentials.refresh(Request())
        
        return credentials
    
    @staticmethod
    def _get_gmail_service(credentials: Credentials):
        """
        Create Gmail service from credentials
        
        :param credentials: Google OAuth Credentials
        :return: Gmail service object
        """
        return build('gmail', 'v1', credentials=credentials)
    
    @staticmethod
    def send_password_reset_email(
        recipient_email: str,
        reset_link: str,
        sender_email: Optional[str] = None,
        refresh_token: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a password reset email via Gmail API
        
        :param recipient_email: Email address of the recipient
        :param reset_link: Secure password reset link
        :param sender_email: Optional sender email (defaults to authenticated user)
        :param refresh_token: OAuth refresh token
        :param client_id: OAuth client ID
        :param client_secret: OAuth client secret
        :return: Email sending result
        """
        try:
            # Use settings credentials if not provided
            refresh_token = refresh_token or settings.gmail_refresh_token
            client_id = client_id or settings.gmail_client_id
            client_secret = client_secret or settings.gmail_client_secret
            
            if not (refresh_token and client_id and client_secret):
                raise ValueError("Gmail OAuth credentials must be provided")
            
            # Get credentials and service
            credentials = GmailEmailService._get_credentials(
                refresh_token=refresh_token,
                client_id=client_id,
                client_secret=client_secret
            )
            service = GmailEmailService._get_gmail_service(credentials)
            
            sender = sender_email or 'me'  # 'me' refers to authenticated user
            
            message = MIMEText(
                f"""
                You have requested a password reset.
                
                Click the following link to reset your password:
                {reset_link}
                
                If you did not request this, please ignore this email.
                """, 
                'plain'
            )
            
            message['to'] = recipient_email
            message['subject'] = 'Password Reset Request'
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send message
            result = service.users().messages().send(
                userId=sender, 
                body={'raw': raw_message}
            ).execute()
            
            return {
                'success': True, 
                'message_id': result.get('id'),
                'thread_id': result.get('threadId')
            }
        
        except HttpError as error:
            print(f'An error occurred: {error}')
            return {
                'success': False, 
                'error': str(error)
            }
    
    @staticmethod
    def create_reset_link(
        reset_token: str, 
        url: str = "https://yourwebsite.com/reset-password"
    ) -> str:
        """
        Create a password reset link
        
        :param reset_token: Unique reset token
        :param base_url: Base URL for password reset page
        :return: Complete reset link
        """
        return f"{url}?token={reset_token}"
    
    @staticmethod
    def create_email_confirmation_link(
        confirmation_token: str, 
        url: str = "https://yourwebsite.com/confirm-email"
    ) -> str:
        """
        Create an email confirmation link
        
        :param confirmation_token: Unique confirmation token
        :param url: Base URL for email confirmation page
        :return: Complete confirmation link
        """
        return f"{url}?token={confirmation_token}"
    
    @staticmethod
    def send_email_confirmation_email(
        recipient_email: str,
        confirmation_link: str,
        user_name: str,
        sender_email: Optional[str] = None,
        refresh_token: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send an email confirmation email via Gmail API
        
        :param recipient_email: Email address of the recipient
        :param confirmation_link: Secure email confirmation link
        :param user_name: Name of the user
        :param sender_email: Optional sender email (defaults to authenticated user)
        :param refresh_token: OAuth refresh token
        :param client_id: OAuth client ID
        :param client_secret: OAuth client secret
        :return: Email sending result
        """
        try:
            # Use settings credentials if not provided
            refresh_token = refresh_token or settings.gmail_refresh_token
            client_id = client_id or settings.gmail_client_id
            client_secret = client_secret or settings.gmail_client_secret
            
            if not (refresh_token and client_id and client_secret):
                raise ValueError("Gmail OAuth credentials must be provided")
            
            # Get credentials and service
            credentials = GmailEmailService._get_credentials(
                refresh_token=refresh_token,
                client_id=client_id,
                client_secret=client_secret
            )
            service = GmailEmailService._get_gmail_service(credentials)
            
            sender = sender_email or 'me'  # 'me' refers to authenticated user
            
            message = MIMEText(
                f"""
                Hello {user_name},
                
                Welcome to our platform! Please confirm your email address by clicking the link below:
                
                {confirmation_link}
                
                This link will expire in 24 hours. If you did not create an account, please ignore this email.
                
                Best regards,
                The Team
                """, 
                'plain'
            )
            
            message['to'] = recipient_email
            message['subject'] = 'Confirm Your Email Address'
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send message
            result = service.users().messages().send(
                userId=sender, 
                body={'raw': raw_message}
            ).execute()
            
            return {
                'success': True, 
                'message_id': result.get('id'),
                'thread_id': result.get('threadId')
            }
        
        except HttpError as error:
            print(f'An error occurred: {error}')
            return {
                'success': False, 
                'error': str(error)
            }
    
    @staticmethod
    def send_email(
        recipient_email: str,
        subject: str,
        content: str,
        content_type: str = 'plain',
        sender_email: Optional[str] = None,
        cc_emails: Optional[List[str]] = None,
        bcc_emails: Optional[List[str]] = None,
        attachments: Optional[List[Dict[str, Union[str, bytes]]]] = None,
        refresh_token: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a generic email via Gmail API with advanced features

        :param recipient_email: Primary recipient email address
        :param subject: Email subject line
        :param content: Email body content
        :param content_type: Content type (default: 'plain', can be 'html')
        :param sender_email: Optional sender email (defaults to authenticated user)
        :param cc_emails: Optional list of CC email addresses
        :param bcc_emails: Optional list of BCC email addresses
        :param attachments: Optional list of attachments
            Each attachment is a dict with keys:
            - 'filename': Name of the file
            - 'content': File content as bytes or base64 encoded string
            - 'mimetype': MIME type of the file (optional, default based on filename)
        :param refresh_token: OAuth refresh token
        :param client_id: OAuth client ID
        :param client_secret: OAuth client secret
        :return: Email sending result
        """
        try:
            # Use settings credentials if not provided
            refresh_token = refresh_token or settings.gmail_refresh_token
            client_id = client_id or settings.gmail_client_id
            client_secret = client_secret or settings.gmail_client_secret
            
            if not (refresh_token and client_id and client_secret):
                raise ValueError("Gmail OAuth credentials must be provided")
            
            # Get credentials and service
            credentials = GmailEmailService._get_credentials(
                refresh_token=refresh_token,
                client_id=client_id,
                client_secret=client_secret
            )
            service = GmailEmailService._get_gmail_service(credentials)
            
            # Prepare multipart message
            message = MIMEMultipart()
            sender = sender_email or 'me'  # 'me' refers to authenticated user
            
            # Set basic message headers
            message['to'] = recipient_email
            if cc_emails:
                message['cc'] = ', '.join(cc_emails)
            if bcc_emails:
                message['bcc'] = ', '.join(bcc_emails)
            message['subject'] = subject
            
            # Add message body
            body = MIMEText(content, content_type)
            message.attach(body)
            
            # Handle attachments
            if attachments:
                for attachment in attachments:
                    # Ensure required keys are present
                    if 'filename' not in attachment or 'content' not in attachment:
                        raise ValueError("Each attachment must have 'filename' and 'content'")
                    
                    # Determine content and mimetype
                    file_content = attachment['content']
                    filename = attachment['filename']
                    mimetype = attachment.get('mimetype')
                    
                    # Convert string content to bytes if needed
                    if isinstance(file_content, str):
                        # Check if it's base64 encoded
                        try:
                            file_content = base64.b64decode(file_content)
                        except:
                            file_content = file_content.encode('utf-8')
                    
                    # Create attachment part
                    part = MIMEApplication(file_content, _subtype=mimetype or 'octet-stream')
                    part.add_header('Content-Disposition', 'attachment', filename=filename)
                    message.attach(part)
            
            # Encode message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            
            # Send message
            result = service.users().messages().send(
                userId=sender,
                body={'raw': raw_message}
            ).execute()
            
            return {
                'success': True,
                'message_id': result.get('id'),
                'thread_id': result.get('threadId')
            }
        
        except HttpError as error:
            print(f'An HTTP error occurred: {error}')
            return {
                'success': False,
                'error': str(error)
            }
        except Exception as error:
            print(f'An error occurred: {error}')
            return {
                'success': False,
                'error': str(error)
            }
        
    @staticmethod
    def notify_new_assignment_request(
        recipient_email: str,
        assignment: Assignment,
        origin: str,
    ) -> Dict[str, Any]:
        
        if recipient_email.endswith('@example.com'):
            return {"success": False, "error": "Invalid recipient email address."}

        """
        Notify about a new assignment request via email
        :param recipient_email: Email address of the recipient
        :param assignment_details: Details of the assignment request
        :return: Email sending result
        """
        subject = f"New Assignment Application: {assignment.title}"
        content = f"""
        You have a new assignment application for your posted assignment "{assignment.title}".

        You may view pending applications at {origin}/dashboard 
        """
        
        return GmailEmailService.send_email(
            recipient_email=recipient_email,
            subject=subject,
            content=content,
        )
    
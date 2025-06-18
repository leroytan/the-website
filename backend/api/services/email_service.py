import base64
import os
import json
import tempfile
from typing import Optional, Dict, Any, List, Union

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from api.config import settings
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
        credentials_json_str: str, 
        token_path: Optional[str] = None
    ) -> Credentials:
        """
        Obtain OAuth 2.0 credentials, refreshing or creating new if needed
        
        :param credentials_json_str: JSON string of OAuth credentials
        :param token_path: Path to store/load OAuth token
        :return: Google OAuth Credentials
        """
        token_path = token_path or os.getenv('GMAIL_TOKEN_PATH', 'token.json')
        credentials = None
        
        # Try to load existing credentials
        if os.path.exists(token_path):
            credentials = Credentials.from_authorized_user_file(
                token_path,
                GmailEmailService.SCOPES
            )
        
        # If no valid credentials, initiate OAuth flow
        if not credentials or not credentials.valid:
            # Create a temporary file with the credentials JSON
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_credentials_file:
                temp_credentials_file.write(credentials_json_str)
                temp_credentials_file_path = temp_credentials_file.name
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    temp_credentials_file_path,
                    GmailEmailService.SCOPES
                )
                credentials = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open(token_path, 'w') as token:
                    token.write(credentials.to_json())
            finally:
                # Clean up the temporary file
                os.unlink(temp_credentials_file_path)
        
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
        credentials_json_str: Optional[str] = None,
        token_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a password reset email via Gmail API
        
        :param recipient_email: Email address of the recipient
        :param reset_link: Secure password reset link
        :param sender_email: Optional sender email (defaults to authenticated user)
        :param credentials_json_str: Optional credentials JSON string (defaults to settings)
        :param token_path: Optional path to store/load OAuth token
        :return: Email sending result
        """
        try:
            # Use settings credentials if not provided
            credentials_json_str = credentials_json_str or settings.gmail_credentials_json
            
            if not credentials_json_str:
                raise ValueError("GMAIL_CREDENTIALS_JSON must be provided")
            
            # Get credentials and service
            credentials = GmailEmailService._get_credentials(
                credentials_json_str, 
                token_path
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
        base_url: str = "https://yourwebsite.com/reset-password"
    ) -> str:
        """
        Create a password reset link
        
        :param reset_token: Unique reset token
        :param base_url: Base URL for password reset page
        :return: Complete reset link
        """
        return f"{base_url}?token={reset_token}"
    
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
        credentials_json_str: Optional[str] = None,
        token_path: Optional[str] = None
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
        :param credentials_json_str: Optional credentials JSON string (defaults to settings)
        :param token_path: Optional path to store/load OAuth token
        :return: Email sending result
        """
        try:
            # Use settings credentials if not provided
            credentials_json_str = credentials_json_str or settings.gmail_credentials_json
            
            if not credentials_json_str:
                raise ValueError("GMAIL_CREDENTIALS_JSON must be provided")
            
            # Get credentials and service
            credentials = GmailEmailService._get_credentials(
                credentials_json_str,
                token_path
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
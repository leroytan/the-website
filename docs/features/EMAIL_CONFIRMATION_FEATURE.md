# Email Confirmation Feature

This document describes the email confirmation feature that has been implemented to enhance the security and user experience of the application.

## Overview

The email confirmation feature ensures that users verify their email addresses before their accounts are fully activated. This helps prevent fake accounts and ensures users have access to the email addresses they register with.

## How It Works

### For New Users
1. When a user signs up with an email that does NOT end with `@example.com`, the system:
   - Creates the user account with `email_verified = false`
   - Generates a secure email confirmation token
   - Sends a confirmation email with a link containing the token
   - **Returns a message asking the user to check their email (NO tokens provided)**
   - User must verify email before they can log in

2. When a user signs up with an email that ends with `@example.com` (for testing):
   - Creates the user account with `email_verified = true`
   - No confirmation email is sent
   - **Returns authentication tokens and logs user in immediately**

### Email Confirmation Process
1. User receives an email with a confirmation link
2. Clicking the link takes them to `/confirm-email?token=<confirmation_token>`
3. The frontend automatically calls the confirmation API
4. If successful, the user's email is marked as verified
5. User can then proceed to use the application normally

**Multiple Clicks Handling**: If a user clicks the confirmation link multiple times:
- First click: Email is verified, shows success message
- Subsequent clicks: Shows "Email Already Verified" message with appropriate UI

### Login Validation
- Users with unverified emails (non-example.com) cannot log in until they verify their email
- The login form shows a specific error message for unverified emails
- Users can request a new confirmation email directly from the login form
- Example.com emails are automatically verified and can log in immediately

## Database Changes

The following fields have been added to the `User` table:

- `email_verified` (Boolean, default: false) - Whether the email has been confirmed
- `email_confirmation_token` (String, nullable) - The current confirmation token
- `email_confirmation_token_expires_at` (DateTime, nullable) - When the token expires

## API Endpoints

### POST `/api/auth/confirm-email`
Confirms a user's email address using a confirmation token.

**Request Body:**
```json
{
  "confirmation_token": "string"
}
```

**Response:**
```json
{
  "message": "Email confirmed successfully"
}
```

### POST `/api/auth/resend-confirmation-email`
Resends a confirmation email to the specified email address.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "If the email is registered, a confirmation link has been sent."
}
```

### POST `/api/auth/signup` (Updated)
Now returns different responses based on email verification status.

**For verified users (example.com):**
```json
{
  "message": "Signed up successfully"
}
```
*Note: Authentication tokens are set as cookies*

**For unverified users (non-example.com):**
```json
{
  "message": "Account created successfully! Please check your email for a confirmation link to verify your account."
}
```
*Note: NO authentication tokens are provided*

### POST `/api/auth/login` (Updated)
Now validates email verification before allowing login.

**Error Response for Unverified Email:**
```json
{
  "detail": {
    "code": "EMAIL_NOT_VERIFIED",
    "message": "Please verify your email address before logging in. Check your inbox for a confirmation link."
  }
}
```

## Frontend Changes

### New Pages
- `/confirm-email` - Handles email confirmation when users click the confirmation link
  - Shows loading state while processing
  - Shows success message for new confirmations
  - Shows "already verified" message for repeated clicks
  - Shows error message for invalid/expired tokens

### Updated Components
- Signup form now shows different messages for example.com vs other emails
- Login form now validates email verification and allows resending confirmation emails
- User profile page shows email verification status
- Unverified users can request a new confirmation email from their profile or login form

## Email Template

The confirmation email includes:
- Personalized greeting with the user's name
- Clear confirmation link
- 24-hour expiration notice
- Professional branding

## Security Features

1. **No Tokens for Unverified Users**: Unverified users receive NO authentication tokens upon signup
2. **Login Validation**: Users cannot log in until their email is verified
3. **Token Expiration**: Confirmation tokens expire after 24 hours
4. **Token Type Validation**: Tokens are validated to ensure they're email confirmation tokens
5. **Token Version Checking**: Tokens are invalidated if the user's token version changes
6. **Email Enumeration Protection**: The resend endpoint always returns success to prevent email enumeration

## Configuration

The feature uses the following configuration from `settings`:
- Gmail OAuth credentials for sending emails

**Origin Detection**: The system automatically detects the frontend origin from the request headers:
- `origin` header (preferred)
- `referer` header (fallback)
- `settings.frontend_domain` (default fallback)

This ensures confirmation links work correctly across different environments (development, staging, production).

## Migration

To add the email confirmation fields to existing databases, run:

```bash
cd backend
python migrate_email_confirmation.py
```

This script will:
1. Add the new columns to the User table
2. Set existing @example.com users as verified
3. Leave other users as unverified (they'll need to confirm their emails)

## Testing

Run the email confirmation tests:

```bash
cd backend
python -m pytest test/api/auth/test_email_confirmation.py -v
```

## Usage Examples

### Testing with Example.com Emails
- Use any email ending with `@example.com` for immediate login without confirmation
- Useful for development and testing

### Production Usage
- Users with real email addresses will receive confirmation emails
- They must click the confirmation link to verify their account
- Unverified users can request new confirmation emails from their profile

## Troubleshooting

### Common Issues

1. **Confirmation emails not sending**
   - Check Gmail OAuth credentials in environment variables
   - Verify the email service is properly configured

2. **Confirmation links not working**
   - Ensure `frontend_domain` is correctly set in configuration
   - Check that the confirmation page is accessible

3. **Tokens expiring too quickly**
   - Default expiration is 24 hours, which can be adjusted in the code

### Debug Mode
For debugging, you can temporarily reduce token expiration time or add logging to track the confirmation process. 
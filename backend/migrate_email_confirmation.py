#!/usr/bin/env python3
"""
Migration script to add email confirmation fields to existing User table.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.config import settings
from api.storage.connection import engine
from sqlalchemy import text
from sqlalchemy.orm import Session

def migrate_email_confirmation():
    """Add email confirmation fields to the User table if they don't exist."""
    print("Starting email confirmation migration...")
    
    with Session(engine) as session:
        try:
            # Check if email_verified column exists
            result = session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'User' AND column_name = 'email_verified'
            """))
            
            if not result.fetchone():
                print("Adding email_verified column...")
                session.execute(text("""
                    ALTER TABLE "User" 
                    ADD COLUMN email_verified BOOLEAN DEFAULT FALSE
                """))
                print("✅ email_verified column added")
            else:
                print("✅ email_verified column already exists")
            
            # Check if email_confirmation_token column exists
            result = session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'User' AND column_name = 'email_confirmation_token'
            """))
            
            if not result.fetchone():
                print("Adding email_confirmation_token column...")
                session.execute(text("""
                    ALTER TABLE "User" 
                    ADD COLUMN email_confirmation_token VARCHAR
                """))
                print("✅ email_confirmation_token column added")
            else:
                print("✅ email_confirmation_token column already exists")
            
            # Check if email_confirmation_token_expires_at column exists
            result = session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'User' AND column_name = 'email_confirmation_token_expires_at'
            """))
            
            if not result.fetchone():
                print("Adding email_confirmation_token_expires_at column...")
                session.execute(text("""
                    ALTER TABLE "User" 
                    ADD COLUMN email_confirmation_token_expires_at TIMESTAMP WITH TIME ZONE
                """))
                print("✅ email_confirmation_token_expires_at column added")
            else:
                print("✅ email_confirmation_token_expires_at column already exists")
            
            # Set existing users with @example.com emails as verified
            print("Setting existing @example.com users as verified...")
            session.execute(text("""
                UPDATE "User" 
                SET email_verified = TRUE 
                WHERE email LIKE '%@example.com'
            """))
            
            session.commit()
            print("✅ Migration completed successfully!")
            
        except Exception as e:
            session.rollback()
            print(f"❌ Migration failed: {str(e)}")
            raise

if __name__ == "__main__":
    migrate_email_confirmation() 
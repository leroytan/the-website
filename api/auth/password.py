import bcrypt

def hash_password(password: str) -> str:
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

if __name__ == "__main__":
    print(hash_password("password123"))
    print(verify_password("password123", '$2b$12$wsyxh9HogoHWD6Sp1EmhSeKeBwC5zrsdxHFo87ZwGSPxzuwtwlZY6'))
    print(verify_password("password234", '$2b$12$wsyxh9HogoHWD6Sp1EmhSeKeBwC5zrsdxHFo87ZwGSPxzuwtwlZY6'))
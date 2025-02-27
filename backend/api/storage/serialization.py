def serialize_user(user: User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "contact": user.contact,
        "userType": user.userType.value,  # Convert enum to string
        "isProfileComplete": user.isProfileComplete,
    }
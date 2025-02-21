# contains all the mock data for each endpoint

from api.router.models import TutorProfile, TutorPublicSummary


def search_tutors():
    return [
        TutorPublicSummary(
            id=1,
            name="John Doe",
            photoUrl="https://example.com/photo1.jpg",
            rate=30.5,
            rating=4,
            subjectsTeachable=["Math", "Physics"],
            levelsTeachable=["Lower Primary", "Upper Primary"],
            experience="5 years of tutoring experience.",
            availability="Mon-Fri, 9 AM - 5 PM"
        ),
        TutorPublicSummary(
            id=2,
            name="Jane Smith",
            photoUrl="https://example.com/photo2.jpg",
            rate=25.0,
            rating=5,
            subjectsTeachable=["Chemistry", "Biology"],
            levelsTeachable=["Lower Secondary", "Upper Secondary"],
            experience="8 years of teaching and research experience.",
            availability="Mon, Wed, Fri, 10 AM - 2 PM"
        ),
        TutorPublicSummary(
            id=3,
            name="Alice Johnson",
            photoUrl=None,
            rate=None,
            rating=3,
            subjectsTeachable=["English", "History"],
            levelsTeachable=["Junior College"],
            experience="2 years of tutoring experience.",
            availability="Sat-Sun, 10 AM - 4 PM"
        )
    ]

def create_tutor():
    return TutorProfile(
        id="1",
        name="John Doe",
        contact=1234567890,
        email="johndoe@example.com",
        photoUrl="https://example.com/photo.jpg",
        highestEducation="Bachelors in Mathematics",
        rate=50.0,
        location="New York, NY",
        rating=5,
        aboutMe="I am a passionate tutor with 10 years of experience in teaching mathematics.",
        subjectsTeachable=["Math", "Physics"],
        levelsTeachable=["Lower Secondary", "Upper Secondary", "Junior College"],
        specialSkills=["Online tutoring", "Problem-solving"],
        resumeUrl="",
        experience="10 years of teaching math at high school and university level.",
        availability="Mon-Fri, 9 AM - 6 PM",
        isProfileComplete=True
    )

def get_tutor_profile():
    return TutorProfile(
        id="1",
        name="John Doe",
        contact=1234567890,
        email="johndoe@example.com",
        photoUrl="https://example.com/photo.jpg",
        highestEducation="Bachelors in Mathematics",
        rate=50.0,
        location="New York, NY",
        rating=5,
        aboutMe="I am a passionate tutor with 10 years of experience in teaching mathematics.",
        subjectsTeachable=["Math", "Physics"],
        levelsTeachable=["Lower Secondary", "Upper Secondary", "Junior College"],
        specialSkills=["Online tutoring", "Problem-solving"],
        resumeUrl="",
        experience="10 years of teaching math at high school and university level.",
        availability="Mon-Fri, 9 AM - 6 PM",
        isProfileComplete=True
    )

def update_tutor_profile():
    return TutorProfile(
        id="1",
        name="John Doe",
        contact=1234567890,
        email="johndoe@example.com",
        photoUrl="https://example.com/photo.jpg",
        highestEducation="Bachelors in Mathematics",
        rate=50.0,
        location="New York, NY",
        rating=5,
        aboutMe="I am a passionate tutor with 10 years of experience in teaching mathematics.",
        subjectsTeachable=["Math", "Physics"],
        levelsTeachable=["Lower Secondary", "Upper Secondary", "Junior College"],
        specialSkills=["Online tutoring", "Problem-solving"],
        resumeUrl="",
        experience="10 years of teaching math at high school and university level.",
        availability="Mon-Fri, 9 AM - 6 PM",
        isProfileComplete=True
    )


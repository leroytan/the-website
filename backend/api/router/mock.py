# contains all the mock data for each endpoint

from api.router.models import AssignmentPublicView, TutorProfile, TutorPublicSummary


def search_tutors():
    return [
        TutorPublicSummary(
            id=1,
            name="John Doe",
            photo_url="https://example.com/photo1.jpg",
            rate="30.5",
            rating=4,
            subjects_teachable=["Math", "Physics"],
            levels_teachable=["Lower Primary", "Upper Primary"],
            experience="5 years of tutoring experience.",
            availability="Mon-Fri, 9 AM - 5 PM",
        ),
        TutorPublicSummary(
            id=2,
            name="Jane Smith",
            photo_url="https://example.com/photo2.jpg",
            rate="25.0",
            rating=5,
            subjects_teachable=["Chemistry", "Biology"],
            levels_teachable=["Lower Secondary", "Upper Secondary"],
            experience="8 years of teaching and research experience.",
            availability="Mon, Wed, Fri, 10 AM - 2 PM",
        ),
        TutorPublicSummary(
            id=3,
            name="Alice Johnson",
            photo_url=None,
            rate=None,
            rating=3,
            subjects_teachable=["English", "History"],
            levels_teachable=["Junior College"],
            experience="2 years of tutoring experience.",
            availability="Sat-Sun, 10 AM - 4 PM",
        ),
    ]


def new_tutor():
    return TutorProfile(
        id="1",
        name="John Doe",
        contact="81234567",
        email="johndoe@example.com",
        photo_url="https://example.com/photo.jpg",
        highest_education="Bachelors in Mathematics",
        rate=50.0,
        location="New York, NY",
        rating=5,
        about_me="I am a passionate tutor with 10 years of experience in teaching mathematics.",
        subjects_teachable=["Math", "Physics"],
        levels_teachable=["Lower Secondary", "Upper Secondary", "Junior College"],
        special_skills=["Online tutoring", "Problem-solving"],
        resume_url="",
        experience="10 years of teaching math at high school and university level.",
        availability="Mon-Fri, 9 AM - 6 PM",
        isProfileComplete=True,
    )


def get_tutor_profile():
    return TutorProfile(
        id="1",
        name="John Doe",
        contact="81234567",
        email="johndoe@example.com",
        photo_url="https://example.com/photo.jpg",
        highest_education="Bachelors in Mathematics",
        rate="50.0",
        location="New York, NY",
        rating=5,
        about_me="I am a passionate tutor with 10 years of experience in teaching mathematics.",
        subjects_teachable=["Math", "Physics"],
        levels_teachable=["Lower Secondary", "Upper Secondary", "Junior College"],
        special_skills=["Online tutoring", "Problem-solving"],
        resume_url="",
        experience="10 years of teaching math at high school and university level.",
        availability="Mon-Fri, 9 AM - 6 PM",
        isProfileComplete=True,
    )


def update_tutor_profile():
    return TutorProfile(
        id="1",
        name="John Doe",
        contact="81234567",
        email="johndoe@example.com",
        photo_url="https://example.com/photo.jpg",
        highest_education="Bachelors in Mathematics",
        rate=50.0,
        location="New York, NY",
        rating=5,
        about_me="I am a passionate tutor with 10 years of experience in teaching mathematics.",
        subjects_teachable=["Math", "Physics"],
        levels_teachable=["Lower Secondary", "Upper Secondary", "Junior College"],
        special_skills=["Online tutoring", "Problem-solving"],
        resume_url="",
        experience="10 years of teaching math at high school and university level.",
        availability="Mon-Fri, 9 AM - 6 PM",
        isProfileComplete=True,
    )


def get_assignments():
    return [
        AssignmentPublicView(
            id=1,
            clientId=1,
            tutor_id=1,
            weekly_frequency=2,
            available_slots=["Mon 2 PM", "Wed 4 PM", "Fri 6 PM"],
            datetime="2022-01-01T10:00:00",
            special_requests="Please bring additional materials for the lesson.",
            status="Pending",
        ),
        AssignmentPublicView(
            id=2,
            clientId=2,
            tutor_id=2,
            weekly_frequency=1,
            available_slots=["Tue 3 PM", "Thu 5 PM"],
            datetime="2022-01-01T14:00:00",
            special_requests="Student requires additional help with homework.",
            status="Confirmed",
        ),
        AssignmentPublicView(
            id=3,
            clientId=3,
            tutor_id=3,
            weekly_frequency=3,
            available_slots=["Sat 10 AM", "Sun 2 PM"],
            datetime="2022-01-01T16:00:00",
            special_requests="Student has upcoming exams and needs intensive tutoring.",
            status="Completed",
        ),
    ]

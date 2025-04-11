from api.storage.models import (Assignment, AssignmentLevel, AssignmentRequest,
                                AssignmentRequestStatus, AssignmentSlot,
                                AssignmentStatus, AssignmentSubject, Level,
                                SpecialSkill, Subject, Tutor, TutorLevel,
                                TutorRequest, TutorRequestStatus,
                                TutorSpecialSkill, TutorSubject, User)


def insert_test_data(engine: object) -> bool:
    """
    Populate the database with test data for development and testing purposes.
    
    Args:
        session: SQLAlchemy engine object
    """
    import datetime

    from sqlalchemy.orm import Session

    session = Session(engine)

    # Check if tables already have data to avoid duplicates
    def table_has_data(model):
        return session.query(model).count() > 0
    
    # Only add data if tables are empty
    if any([
        table_has_data(User),
        table_has_data(Tutor),
        table_has_data(Subject),
        table_has_data(Level),
        table_has_data(SpecialSkill),
        table_has_data(Assignment)
    ]):
        print("Database already contains data. Skipping test data insertion.")
        return False
    
    # Create test subjects
    subjects = [
        Subject(name="Mathematics"),
        Subject(name="Physics"),
        Subject(name="Chemistry"),
        Subject(name="Biology"),
        Subject(name="English Literature"),
        Subject(name="Computer Science"),
        Subject(name="History"),
        Subject(name="Spanish"),
        Subject(name="Economics"),
        Subject(name="Music")
    ]
    session.add_all(subjects)
    
    # Create test levels
    levels = [
        Level(name="Elementary School"),
        Level(name="Middle School"),
        Level(name="High School"),
        Level(name="College"),
        Level(name="University"),
        Level(name="Graduate"),
        Level(name="Professional")
    ]
    session.add_all(levels)
    
    # Create test special skills
    special_skills = [
        SpecialSkill(name="Test Preparation"),
        SpecialSkill(name="Special Education"),
        SpecialSkill(name="Advanced Placement"),
        SpecialSkill(name="Project-Based Learning"),
        SpecialSkill(name="Homework Help"),
        SpecialSkill(name="Career Counseling"),
        SpecialSkill(name="English as Second Language")
    ]
    session.add_all(special_skills)
    
    # Commit these tables first to get IDs
    session.commit()
    
    # Create test users (mix of regular users and tutors)
    users = [
        User(
            name="John Doe",
            email="john.doe@example.com",
            passwordHash="someHash"
        ),
        User(
            name="Jane Smith",
            email="jane.smith@example.com",
            passwordHash="someHash"
        ),
        User(
            name="Alice Johnson",
            email="alice.johnson@example.com",
            passwordHash="someHash"
        ),
        User(
            name="Bob Williams",
            email="bob.williams@example.com",
            passwordHash="someHash"
        ),
        User(
            name="Carol Brown",
            email="carol.brown@example.com",
            passwordHash="someHash"
        ),
        User(
            name="David Miller",
            email="david.miller@example.com",
            passwordHash="someHash"
        ),
        User(
            name="Eva Garcia",
            email="eva.garcia@example.com",
            passwordHash="someHash"
        ),
        User(
            name="Frank Rodriguez",
            email="frank.rodriguez@example.com",
            passwordHash="someHash"
        )
    ]
    session.add_all(users)
    session.commit()
    
    # Create tutors (for users 3-8)
    tutors = [
        Tutor(
            id=users[2].id,  # Alice
            photoUrl="https://randomuser.me/api/portraits/women/1.jpg",
            highestEducation="Ph.D. in Mathematics",
            availability="Weekdays 3PM-8PM, Weekends 10AM-4PM",
            resumeUrl="https://example.com/alice_resume.pdf",
            rate="$45/hour",
            location="New York, NY",
            rating=4.8,
            aboutMe="I've been teaching mathematics for over 10 years with a focus on calculus and statistics.",
            experience="10+ years"
        ),
        Tutor(
            id=users[3].id,  # Bob
            photoUrl="https://randomuser.me/api/portraits/men/1.jpg",
            highestEducation="Master's in Physics",
            availability="Weekends and evenings",
            resumeUrl="https://example.com/bob_resume.pdf",
            rate="$40/hour",
            location="Boston, MA",
            rating=4.6,
            aboutMe="Passionate physics teacher with experience preparing students for AP exams.",
            experience="5 years"
        ),
        Tutor(
            id=users[4].id,  # Carol
            photoUrl="https://randomuser.me/api/portraits/women/2.jpg",
            highestEducation="Bachelor's in English Literature",
            availability="Flexible schedule",
            resumeUrl="https://example.com/carol_resume.pdf",
            rate="$35/hour",
            location="San Francisco, CA",
            rating=4.9,
            aboutMe="I help students improve their writing skills and critical analysis of literature.",
            experience="7 years"
        ),
        Tutor(
            id=users[5].id,  # David
            photoUrl="https://randomuser.me/api/portraits/men/2.jpg",
            highestEducation="Master's in Computer Science",
            availability="Weekday evenings",
            resumeUrl="https://example.com/david_resume.pdf",
            rate="$50/hour",
            location="Seattle, WA",
            rating=4.7,
            aboutMe="Software engineer by day, programming tutor by night. I specialize in Python and Java.",
            experience="8 years"
        ),
        Tutor(
            id=users[6].id,  # Eva
            photoUrl="https://randomuser.me/api/portraits/women/3.jpg",
            highestEducation="Ph.D. in Chemistry",
            availability="Weekends only",
            resumeUrl="https://example.com/eva_resume.pdf",
            rate="$45/hour",
            location="Chicago, IL",
            rating=4.5,
            aboutMe="I make complex chemistry concepts easy to understand for students of all levels.",
            experience="6 years"
        ),
        Tutor(
            id=users[7].id,  # Frank
            photoUrl="https://randomuser.me/api/portraits/men/3.jpg",
            highestEducation="Master's in Spanish",
            availability="Afternoons and weekends",
            resumeUrl="https://example.com/frank_resume.pdf",
            rate="$38/hour",
            location="Miami, FL",
            rating=4.9,
            aboutMe="Native Spanish speaker with a passion for teaching language and culture.",
            experience="9 years"
        )
    ]
    session.add_all(tutors)
    session.commit()
    
    # Assign subjects to tutors
    tutor_subjects = [
        # Alice teaches Math and Statistics
        TutorSubject(tutorId=tutors[0].id, subjectId=subjects[0].id),  # Math
        
        # Bob teaches Physics and Math
        TutorSubject(tutorId=tutors[1].id, subjectId=subjects[1].id),  # Physics
        TutorSubject(tutorId=tutors[1].id, subjectId=subjects[0].id),  # Math
        
        # Carol teaches English Literature and History
        TutorSubject(tutorId=tutors[2].id, subjectId=subjects[4].id),  # English Literature
        TutorSubject(tutorId=tutors[2].id, subjectId=subjects[6].id),  # History
        
        # David teaches Computer Science and Math
        TutorSubject(tutorId=tutors[3].id, subjectId=subjects[5].id),  # Computer Science
        TutorSubject(tutorId=tutors[3].id, subjectId=subjects[0].id),  # Math
        
        # Eva teaches Chemistry and Biology
        TutorSubject(tutorId=tutors[4].id, subjectId=subjects[2].id),  # Chemistry
        TutorSubject(tutorId=tutors[4].id, subjectId=subjects[3].id),  # Biology
        
        # Frank teaches Spanish and Music
        TutorSubject(tutorId=tutors[5].id, subjectId=subjects[7].id),  # Spanish
        TutorSubject(tutorId=tutors[5].id, subjectId=subjects[9].id)   # Music
    ]
    session.add_all(tutor_subjects)
    
    # Assign levels to tutors
    tutor_levels = [
        # Alice teaches High School, College, University
        TutorLevel(tutorId=tutors[0].id, levelId=levels[2].id),  # High School
        TutorLevel(tutorId=tutors[0].id, levelId=levels[3].id),  # College
        TutorLevel(tutorId=tutors[0].id, levelId=levels[4].id),  # University
        
        # Bob teaches High School, College
        TutorLevel(tutorId=tutors[1].id, levelId=levels[2].id),  # High School
        TutorLevel(tutorId=tutors[1].id, levelId=levels[3].id),  # College
        
        # Carol teaches Middle School, High School, College
        TutorLevel(tutorId=tutors[2].id, levelId=levels[1].id),  # Middle School
        TutorLevel(tutorId=tutors[2].id, levelId=levels[2].id),  # High School
        TutorLevel(tutorId=tutors[2].id, levelId=levels[3].id),  # College
        
        # David teaches High School, College, University, Graduate
        TutorLevel(tutorId=tutors[3].id, levelId=levels[2].id),  # High School
        TutorLevel(tutorId=tutors[3].id, levelId=levels[3].id),  # College
        TutorLevel(tutorId=tutors[3].id, levelId=levels[4].id),  # University
        TutorLevel(tutorId=tutors[3].id, levelId=levels[5].id),  # Graduate
        
        # Eva teaches Middle School, High School, College
        TutorLevel(tutorId=tutors[4].id, levelId=levels[1].id),  # Middle School
        TutorLevel(tutorId=tutors[4].id, levelId=levels[2].id),  # High School
        TutorLevel(tutorId=tutors[4].id, levelId=levels[3].id),  # College
        
        # Frank teaches Elementary, Middle School, High School
        TutorLevel(tutorId=tutors[5].id, levelId=levels[0].id),  # Elementary School
        TutorLevel(tutorId=tutors[5].id, levelId=levels[1].id),  # Middle School
        TutorLevel(tutorId=tutors[5].id, levelId=levels[2].id)   # High School
    ]
    session.add_all(tutor_levels)
    
    # Assign special skills to tutors
    tutor_special_skills = [
        # Alice: Test Prep, AP
        TutorSpecialSkill(tutorId=tutors[0].id, specialSkillId=special_skills[0].id),  # Test Prep
        TutorSpecialSkill(tutorId=tutors[0].id, specialSkillId=special_skills[2].id),  # AP
        
        # Bob: Test Prep, AP, Project-Based Learning
        TutorSpecialSkill(tutorId=tutors[1].id, specialSkillId=special_skills[0].id),  # Test Prep
        TutorSpecialSkill(tutorId=tutors[1].id, specialSkillId=special_skills[2].id),  # AP
        TutorSpecialSkill(tutorId=tutors[1].id, specialSkillId=special_skills[3].id),  # Project-Based
        
        # Carol: Homework Help, Career Counseling
        TutorSpecialSkill(tutorId=tutors[2].id, specialSkillId=special_skills[4].id),  # Homework Help
        TutorSpecialSkill(tutorId=tutors[2].id, specialSkillId=special_skills[5].id),  # Career Counseling
        
        # David: Project-Based Learning, Homework Help
        TutorSpecialSkill(tutorId=tutors[3].id, specialSkillId=special_skills[3].id),  # Project-Based
        TutorSpecialSkill(tutorId=tutors[3].id, specialSkillId=special_skills[4].id),  # Homework Help
        
        # Eva: AP, Special Education
        TutorSpecialSkill(tutorId=tutors[4].id, specialSkillId=special_skills[2].id),  # AP
        TutorSpecialSkill(tutorId=tutors[4].id, specialSkillId=special_skills[1].id),  # Special Education
        
        # Frank: ESL, Special Education
        TutorSpecialSkill(tutorId=tutors[5].id, specialSkillId=special_skills[6].id),  # ESL
        TutorSpecialSkill(tutorId=tutors[5].id, specialSkillId=special_skills[1].id)   # Special Education
    ]
    session.add_all(tutor_special_skills)
    
    # Create test assignments
    assignments = [
        Assignment(
            title="Calculus Finals Prep",
            requesterId=users[0].id,  # John Doe requesting 
            tutorId=None,  # No tutor assigned yet
            estimatedRate="$45/hour",
            weeklyFrequency=2,
            specialRequests="Need help preparing for calculus final exam",
            status=AssignmentStatus.OPEN
        ),
        Assignment(
            title="Essay-Writing Clinic",
            requesterId=users[1].id,  # Jane Smith requesting
            tutorId=tutors[2].id,     # Carol as tutor
            estimatedRate="$35/hour",
            weeklyFrequency=1,
            specialRequests="Essay writing assistance needed",
            status=AssignmentStatus.FILLED
        ),
        Assignment(
            title="Programming Coaching (Python)",
            datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            requesterId=users[0].id,  # John Doe requesting
            tutorId=None,  # No tutor assigned yet
            estimatedRate="$50/hour",
            weeklyFrequency=3,
            specialRequests="Need help with Python programming project",
            status=AssignmentStatus.OPEN
        )
    ]
    session.add_all(assignments)
    session.commit()
    
    # Create assignment slots
    assignment_slots = [
        # For assignment 1 (John & Alice)
        AssignmentSlot(
            assignmentId=assignments[0].id,
            day="Monday",
            startTime="16:00",
            endTime="18:00"
        ),
        AssignmentSlot(
            assignmentId=assignments[0].id,
            day="Wednesday",
            startTime="16:00",
            endTime="18:00"
        ),
        
        # For assignment 2 (Jane & Carol)
        AssignmentSlot(
            assignmentId=assignments[1].id,
            day="Saturday",
            startTime="10:00",
            endTime="12:00"
        ),
        
        # For assignment 3 (John & David)
        AssignmentSlot(
            assignmentId=assignments[2].id,
            day="Tuesday",
            startTime="18:00",
            endTime="19:30"
        ),
        AssignmentSlot(
            assignmentId=assignments[2].id,
            day="Thursday",
            startTime="18:00",
            endTime="19:30"
        ),
        AssignmentSlot(
            assignmentId=assignments[2].id,
            day="Sunday",
            startTime="15:00",
            endTime="16:30"
        )
    ]
    session.add_all(assignment_slots)
    
    # Link subjects to assignments
    assignment_subjects = [
        # Assignment 1: Math
        AssignmentSubject(assignmentId=assignments[0].id, subjectId=subjects[0].id),
        
        # Assignment 2: English Literature
        AssignmentSubject(assignmentId=assignments[1].id, subjectId=subjects[4].id),
        
        # Assignment 3: Computer Science
        AssignmentSubject(assignmentId=assignments[2].id, subjectId=subjects[5].id)
    ]
    session.add_all(assignment_subjects)
    
    # Link levels to assignments
    assignment_levels = [
        # Assignment 1: College level math
        AssignmentLevel(assignmentId=assignments[0].id, levelId=levels[3].id),
        
        # Assignment 2: High School English
        AssignmentLevel(assignmentId=assignments[1].id, levelId=levels[2].id),
        
        # Assignment 3: College Computer Science
        AssignmentLevel(assignmentId=assignments[2].id, levelId=levels[3].id)
    ]
    session.add_all(assignment_levels)
    
    # Create tutor requests
    tutor_requests = [
        TutorRequest(
            datetime=datetime.datetime.now(),
            requesterId=users[0].id,  # John requesting Alice
            tutorId=tutors[0].id,
            status=TutorRequestStatus.PENDING
        ),
        TutorRequest(
            datetime=datetime.datetime.now() - datetime.timedelta(days=2),
            requesterId=users[1].id,  # Jane requesting Carol
            tutorId=tutors[2].id,
            status=TutorRequestStatus.ACCEPTED
        ),
        TutorRequest(
            datetime=datetime.datetime.now() - datetime.timedelta(days=5),
            requesterId=users[0].id,  # John requesting Eva
            tutorId=tutors[4].id,
            status=TutorRequestStatus.REJECTED
        )
    ]
    session.add_all(tutor_requests)
    
    # Create assignment requests
    assignment_requests = [
        AssignmentRequest(
            datetime=datetime.datetime.now() - datetime.timedelta(days=1),
            tutorId=tutors[1].id,  # Bob requesting assignment
            status=AssignmentRequestStatus.PENDING,
            assignment=assignments[0]  # For the first assignment
        ),
        AssignmentRequest(
            datetime=datetime.datetime.now() - datetime.timedelta(days=3),
            tutorId=tutors[2].id,  # Carol requesting assignment
            status=AssignmentRequestStatus.ACCEPTED,
            assignment=assignments[1]  # For the second assignment
        ),
        AssignmentRequest(
            datetime=datetime.datetime.now() - datetime.timedelta(days=4),
            tutorId=tutors[5].id,  # Frank requesting assignment
            status=AssignmentRequestStatus.REJECTED,
            assignment=assignments[0]  # For the first assignment
        )
    ]
    session.add_all(assignment_requests)
    
    # Final commit
    session.commit()
    
    print("Test data successfully inserted into the database.")
    return True
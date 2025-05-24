from api.storage.models import (Assignment, AssignmentRequest,
                                AssignmentRequestStatus, AssignmentSlot,
                                AssignmentStatus, AssignmentSubject,
                                ChatMessage, Level, PrivateChat, SpecialSkill,
                                Subject, Tutor, TutorLevel, TutorSpecialSkill,
                                TutorSubject, User)


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
        Level(name="Primary 1"),
        Level(name="Primary 2"),
        Level(name="Primary 3"),
        Level(name="Primary 4"),
        Level(name="Primary 5"),
        Level(name="Primary 6"),
        Level(name="Secondary 1"),
        Level(name="Secondary 2"),
        Level(name="Secondary 3"),
        Level(name="Secondary 4"),
        Level(name="Secondary 5"),
        Level(name="Junior College 1"),
        Level(name="Junior College 2"),
    ]
    session.add_all(levels)
    
    # Create test special skills
    populate_special_skills = [
        SpecialSkill(name="Test Preparation"),
        SpecialSkill(name="Special Education"),
        SpecialSkill(name="Advanced Placement"),
        SpecialSkill(name="Project-Based Learning"),
        SpecialSkill(name="Homework Help"),
        SpecialSkill(name="Career Counseling"),
        SpecialSkill(name="English as Second Language")
    ]
    session.add_all(populate_special_skills)
    
    # Commit these tables first to get IDs
    session.commit()
    
    # Create test users (mix of regular users and tutors)
    users = [
        User(
            name="John Doe",
            email="john@example.com",
            password_hash="$2b$12$mZzAAXmyGtilH5mlwosyNuz5v56iacPnXAfo0v6XPhNLCgzAQBsTC"
        ),
        User(
            name="Jane Smith",
            email="jane@example.com",
            password_hash="$2b$12$evEA25gWMQM.wXxgc0BNmua4AMzXY5HeJHZv1ARI7PqAxBNKoOIrW"
        ),
        User(
            name="Alice Johnson",
            email="alice@example.com",
            password_hash="$2b$12$TaklfiCGynwG22JiBxL3v.xJrZ4Xj3P3jWV.O9gjf3DYxNmqJ18xe"
        ),
        User(
            name="Bob Williams",
            email="bob@example.com",
            password_hash="$2b$12$eycYqtvIeFMU2UcHokCVQuzKvQVoIN32gSnU2wWlzI6.RRCVPWLpK"
        ),
        User(
            name="Carol Brown",
            email="carol@example.com",
            password_hash="$2b$12$Hx2sLVhoiwYrqBC4fTkrC.HHsI3YS73QEvyUDNzYak4yoKWeSIgCi"
        ),
        User(
            name="David Miller",
            email="david@example.com",
            password_hash="$2b$12$r6ENReONet3RHULZrCGiqOhdESByFdHLrDAdsCU97mILx4wpFjSVa"
        ),
        User(
            name="Eva Garcia",
            email="eva@example.com",
            password_hash="$2b$12$f/2ZDD/EeIMKn6OXo.a2GeWsNWVcI/KZLmsIoeMUCEKhaU.14DXBW"
        ),
        User(
            name="Frank Rodriguez",
            email="frank@example.com",
            password_hash="$2b$12$ojmyO9IQEu4EDmpRuOykEuRl6Lu3pN9dkuMyUn6NDNNWTCfP37HE6"
        )
    ]
    session.add_all(users)
    session.commit()
    
    # Create tutors (for users 3-8)
    tutors = [
        Tutor(
            id=users[2].id,  # Alice
            photo_url="https://randomuser.me/api/portraits/women/1.jpg",
            highest_education="Ph.D. in Mathematics",
            availability="Weekdays 3PM-8PM, Weekends 10AM-4PM",
            resume_url="https://example.com/alice_resume.pdf",
            rate="$45/hour",
            location="New York, NY",
            rating=4.8,
            about_me="I've been teaching mathematics for over 10 years with a focus on calculus and statistics.",
            experience="10+ years"
        ),
        Tutor(
            id=users[3].id,  # Bob
            photo_url="https://randomuser.me/api/portraits/men/1.jpg",
            highest_education="Master's in Physics",
            availability="Weekends and evenings",
            resume_url="https://example.com/bob_resume.pdf",
            rate="$40/hour",
            location="Boston, MA",
            rating=4.6,
            about_me="Passionate physics teacher with experience preparing students for AP exams.",
            experience="5 years"
        ),
        Tutor(
            id=users[4].id,  # Carol
            photo_url="https://randomuser.me/api/portraits/women/2.jpg",
            highest_education="Bachelor's in English Literature",
            availability="Flexible schedule",
            resume_url="https://example.com/carol_resume.pdf",
            rate="$35/hour",
            location="San Francisco, CA",
            rating=4.9,
            about_me="I help students improve their writing skills and critical analysis of literature.",
            experience="7 years"
        ),
        Tutor(
            id=users[5].id,  # David
            photo_url="https://randomuser.me/api/portraits/men/2.jpg",
            highest_education="Master's in Computer Science",
            availability="Weekday evenings",
            resume_url="https://example.com/david_resume.pdf",
            rate="$50/hour",
            location="Seattle, WA",
            rating=4.7,
            about_me="Software engineer by day, programming tutor by night. I specialize in Python and Java.",
            experience="8 years"
        ),
        Tutor(
            id=users[6].id,  # Eva
            photo_url="https://randomuser.me/api/portraits/women/3.jpg",
            highest_education="Ph.D. in Chemistry",
            availability="Weekends only",
            resume_url="https://example.com/eva_resume.pdf",
            rate="$45/hour",
            location="Chicago, IL",
            rating=4.5,
            about_me="I make complex chemistry concepts easy to understand for students of all levels.",
            experience="6 years"
        ),
        Tutor(
            id=users[7].id,  # Frank
            photo_url="https://randomuser.me/api/portraits/men/3.jpg",
            highest_education="Master's in Spanish",
            availability="Afternoons and weekends",
            resume_url="https://example.com/frank_resume.pdf",
            rate="$38/hour",
            location="Miami, FL",
            rating=4.9,
            about_me="Native Spanish speaker with a passion for teaching language and culture.",
            experience="9 years"
        )
    ]
    session.add_all(tutors)
    session.commit()
    
    # Assign subjects to tutors
    tutor_subjects = [
        # Alice teaches Math and Statistics
        TutorSubject(tutor_id=tutors[0].id, subjectId=subjects[0].id),  # Math
        
        # Bob teaches Physics and Math
        TutorSubject(tutor_id=tutors[1].id, subjectId=subjects[1].id),  # Physics
        TutorSubject(tutor_id=tutors[1].id, subjectId=subjects[0].id),  # Math
        
        # Carol teaches English Literature and History
        TutorSubject(tutor_id=tutors[2].id, subjectId=subjects[4].id),  # English Literature
        TutorSubject(tutor_id=tutors[2].id, subjectId=subjects[6].id),  # History
        
        # David teaches Computer Science and Math
        TutorSubject(tutor_id=tutors[3].id, subjectId=subjects[5].id),  # Computer Science
        TutorSubject(tutor_id=tutors[3].id, subjectId=subjects[0].id),  # Math
        
        # Eva teaches Chemistry and Biology
        TutorSubject(tutor_id=tutors[4].id, subjectId=subjects[2].id),  # Chemistry
        TutorSubject(tutor_id=tutors[4].id, subjectId=subjects[3].id),  # Biology
        
        # Frank teaches Spanish and Music
        TutorSubject(tutor_id=tutors[5].id, subjectId=subjects[7].id),  # Spanish
        TutorSubject(tutor_id=tutors[5].id, subjectId=subjects[9].id)   # Music
    ]
    session.add_all(tutor_subjects)
    
    # Assign levels to tutors
    tutor_levels = [
        # Alice teaches 
        TutorLevel(tutor_id=tutors[0].id, level_id=levels[2].id),
        TutorLevel(tutor_id=tutors[0].id, level_id=levels[3].id),
        TutorLevel(tutor_id=tutors[0].id, level_id=levels[4].id),
        
        # Bob teaches 
        TutorLevel(tutor_id=tutors[1].id, level_id=levels[2].id),
        TutorLevel(tutor_id=tutors[1].id, level_id=levels[3].id),
        
        # Carol teaches 
        TutorLevel(tutor_id=tutors[2].id, level_id=levels[1].id),
        TutorLevel(tutor_id=tutors[2].id, level_id=levels[2].id),
        TutorLevel(tutor_id=tutors[2].id, level_id=levels[3].id),
        
        # David teaches
        TutorLevel(tutor_id=tutors[3].id, level_id=levels[2].id),
        TutorLevel(tutor_id=tutors[3].id, level_id=levels[3].id),
        TutorLevel(tutor_id=tutors[3].id, level_id=levels[4].id),
        TutorLevel(tutor_id=tutors[3].id, level_id=levels[5].id),
        
        # Eva teaches 
        TutorLevel(tutor_id=tutors[4].id, level_id=levels[1].id),
        TutorLevel(tutor_id=tutors[4].id, level_id=levels[2].id),
        TutorLevel(tutor_id=tutors[4].id, level_id=levels[3].id),
        
        # Frank teaches
        TutorLevel(tutor_id=tutors[5].id, level_id=levels[0].id),
        TutorLevel(tutor_id=tutors[5].id, level_id=levels[1].id),
        TutorLevel(tutor_id=tutors[5].id, level_id=levels[2].id) 
    ]
    session.add_all(tutor_levels)
    
    # Assign special skills to tutors
    tutor_populate_special_skills = [
        # Alice: Test Prep, AP
        TutorSpecialSkill(tutor_id=tutors[0].id, special_skill_id=populate_special_skills[0].id),  # Test Prep
        TutorSpecialSkill(tutor_id=tutors[0].id, special_skill_id=populate_special_skills[2].id),  # AP
        
        # Bob: Test Prep, AP, Project-Based Learning
        TutorSpecialSkill(tutor_id=tutors[1].id, special_skill_id=populate_special_skills[0].id),  # Test Prep
        TutorSpecialSkill(tutor_id=tutors[1].id, special_skill_id=populate_special_skills[2].id),  # AP
        TutorSpecialSkill(tutor_id=tutors[1].id, special_skill_id=populate_special_skills[3].id),  # Project-Based
        
        # Carol: Homework Help, Career Counseling
        TutorSpecialSkill(tutor_id=tutors[2].id, special_skill_id=populate_special_skills[4].id),  # Homework Help
        TutorSpecialSkill(tutor_id=tutors[2].id, special_skill_id=populate_special_skills[5].id),  # Career Counseling
        
        # David: Project-Based Learning, Homework Help
        TutorSpecialSkill(tutor_id=tutors[3].id, special_skill_id=populate_special_skills[3].id),  # Project-Based
        TutorSpecialSkill(tutor_id=tutors[3].id, special_skill_id=populate_special_skills[4].id),  # Homework Help
        
        # Eva: AP, Special Education
        TutorSpecialSkill(tutor_id=tutors[4].id, special_skill_id=populate_special_skills[2].id),  # AP
        TutorSpecialSkill(tutor_id=tutors[4].id, special_skill_id=populate_special_skills[1].id),  # Special Education
        
        # Frank: ESL, Special Education
        TutorSpecialSkill(tutor_id=tutors[5].id, special_skill_id=populate_special_skills[6].id),  # ESL
        TutorSpecialSkill(tutor_id=tutors[5].id, special_skill_id=populate_special_skills[1].id)   # Special Education
    ]
    session.add_all(tutor_populate_special_skills)
    
    # Create test assignments
    assignments = [
        Assignment(
            title="Calculus Finals Prep",
            owner_id=users[0].id,  # John Doe requesting 
            tutor_id=None,  # No tutor assigned yet
            level_id=levels[3].id,
            estimated_rate="$45/hour",
            weekly_frequency=2,
            special_requests="Need help preparing for calculus final exam",
            status=AssignmentStatus.OPEN,
            location="Jurong East, Singapore"  # Example location
        ),
        Assignment(
            title="Essay-Writing Clinic",
            owner_id=users[1].id,  # Jane Smith requesting
            tutor_id=tutors[2].id,     # Carol as tutor
            level_id=levels[2].id,
            estimated_rate="$35/hour",
            weekly_frequency=1,
            special_requests="Essay writing assistance needed",
            status=AssignmentStatus.FILLED,
            location="Bukit Batok, Singapore"  # Example location
        ),
        Assignment(
            title="Programming Coaching (Python)",
            owner_id=users[0].id,  # John Doe requesting
            tutor_id=None,  # No tutor assigned yet
            level_id=levels[3].id,
            estimated_rate="$50/hour",
            weekly_frequency=3,
            special_requests="Need help with Python programming project",
            status=AssignmentStatus.OPEN,
            location="Bedok South, Singapore"  # Example location
        )
    ]
    session.add_all(assignments)
    session.flush()
    
    # Create assignment slots
    assignment_slots = [
        # For assignment 1 (John & Alice)
        AssignmentSlot(
            assignment_id=assignments[0].id,
            day="Monday",
            start_time="16:00",
            end_time="18:00"
        ),
        AssignmentSlot(
            assignment_id=assignments[0].id,
            day="Wednesday",
            start_time="16:00",
            end_time="18:00"
        ),
        
        # For assignment 2 (Jane & Carol)
        AssignmentSlot(
            assignment_id=assignments[1].id,
            day="Saturday",
            start_time="10:00",
            end_time="12:00"
        ),
        
        # For assignment 3 (John & David)
        AssignmentSlot(
            assignment_id=assignments[2].id,
            day="Tuesday",
            start_time="18:00",
            end_time="19:30"
        ),
        AssignmentSlot(
            assignment_id=assignments[2].id,
            day="Thursday",
            start_time="18:00",
            end_time="19:30"
        ),
        AssignmentSlot(
            assignment_id=assignments[2].id,
            day="Sunday",
            start_time="15:00",
            end_time="16:30"
        )
    ]
    session.add_all(assignment_slots)
    
    # Link subjects to assignments
    assignment_subjects = [
        # Assignment 1: Math
        AssignmentSubject(assignment_id=assignments[0].id, subjectId=subjects[0].id),
        
        # Assignment 2: English Literature
        AssignmentSubject(assignment_id=assignments[1].id, subjectId=subjects[4].id),
        
        # Assignment 3: Computer Science
        AssignmentSubject(assignment_id=assignments[2].id, subjectId=subjects[5].id)
    ]
    session.add_all(assignment_subjects)
    
    # Create assignment requests
    assignment_requests = [
        AssignmentRequest(
            created_at=datetime.datetime.now() - datetime.timedelta(days=1),
            tutor_id=tutors[1].id,  # Bob requesting assignment
            status=AssignmentRequestStatus.PENDING,
            assignment_id=assignments[0].id  # For the first assignment
        ),
        AssignmentRequest(
            created_at=datetime.datetime.now() - datetime.timedelta(days=3),
            tutor_id=tutors[2].id,  # Carol requesting assignment
            status=AssignmentRequestStatus.ACCEPTED,
            assignment_id=assignments[1].id  # For the second assignment
        ),
        AssignmentRequest(
            created_at=datetime.datetime.now() - datetime.timedelta(days=4),
            tutor_id=tutors[5].id,  # Frank requesting assignment
            status=AssignmentRequestStatus.REJECTED,
            assignment_id=assignments[0].id  # For the first assignment
        )
    ]
    session.add_all(assignment_requests)

    # Create private chatrooms
    private_chats = [
        PrivateChat(
            user1_id=users[0].id,  # John
            user2_id=users[1].id,  # Jane
            is_locked=False
        ),
        PrivateChat(
            user1_id=users[2].id,  # Alice
            user2_id=users[3].id,  # Bob
            is_locked=True  # Locked chat
        ),
        PrivateChat(
            user1_id=users[4].id,  # Carol
            user2_id=users[5].id,  # David
            is_locked=False
        )
    ]

    session.add_all(private_chats)
    session.commit()
    for chat in private_chats:
        session.refresh(chat)

    # Create chat messages
    chat_messages = [
        ChatMessage(
            chat_id=private_chats[0].id,
            sender_id=users[0].id,
            content="Hi Jane, I need help with my calculus finals.",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=2)
        ),
        ChatMessage(
            chat_id=private_chats[0].id,
            sender_id=users[1].id,
            content="Sure John, I can help you with that!",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=1, minutes=50)
        ),
        ChatMessage(
            chat_id=private_chats[0].id,
            sender_id=users[0].id,
            content="Awesome! I'm struggling with integration by parts.",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=1, minutes=40)
        ),
        ChatMessage(
            chat_id=private_chats[0].id,
            sender_id=users[1].id,
            content="Let's go through an example. Do you have a problem in mind?",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=1, minutes=30)
        ),
        ChatMessage(
            chat_id=private_chats[0].id,
            sender_id=users[0].id,
            content="Yes! ∫x·e^x dx. I don't know where to start.",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=1, minutes=25)
        ),
        ChatMessage(
            chat_id=private_chats[0].id,
            sender_id=users[1].id,
            content="Perfect example. You'll want to set u = x and dv = e^x dx.",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=1, minutes=20)
        ),
        ChatMessage(
            chat_id=private_chats[0].id,
            sender_id=users[0].id,
            content="Ah, got it. So du = dx and v = e^x?",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=1, minutes=15)
        ),
        ChatMessage(
            chat_id=private_chats[0].id,
            sender_id=users[1].id,
            content="Exactly! Now use the formula: ∫u·dv = uv - ∫v·du.",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=1, minutes=10)
        ),
        ChatMessage(
            chat_id=private_chats[1].id,
            sender_id=users[2].id,
            content="Bob, are you available for a study session?",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=2)
        ),
        ChatMessage(
            chat_id=private_chats[1].id,
            sender_id=users[3].id,
            content="Yes Alice, let's meet this weekend.",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=1, minutes=50)
        ),
        ChatMessage(
            chat_id=private_chats[1].id,
            sender_id=users[2].id,
            content="Saturday afternoon works for me. Maybe 2 PM?",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=1, minutes=40)
        ),
        ChatMessage(
            chat_id=private_chats[1].id,
            sender_id=users[3].id,
            content="Perfect. Should we meet at the library?",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=1, minutes=35)
        ),
        ChatMessage(
            chat_id=private_chats[1].id,
            sender_id=users[2].id,
            content="Yes, third floor study room. I’ll reserve it.",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=1, minutes=30)
        ),
        ChatMessage(
            chat_id=private_chats[1].id,
            sender_id=users[3].id,
            content="Great! Let’s cover chapters 5 to 7?",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=1, minutes=25)
        ),
        ChatMessage(
            chat_id=private_chats[1].id,
            sender_id=users[2].id,
            content="Sounds good. I’ll bring my notes and problem sets.",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=1, minutes=20)
        ),
        ChatMessage(
            chat_id=private_chats[2].id,
            sender_id=users[4].id,
            content="David, I have some questions about the assignment.",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=2)
        ),
        ChatMessage(
            chat_id=private_chats[2].id,
            sender_id=users[5].id,
            content="Sure Carol, feel free to ask me anytime.",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=1, minutes=50)
        ),
        ChatMessage(
            chat_id=private_chats[2].id,
            sender_id=users[4].id,
            content="I'm stuck on question 3. What's the best approach?",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=1, minutes=40)
        ),
        ChatMessage(
            chat_id=private_chats[2].id,
            sender_id=users[5].id,
            content="Start by identifying the variables. It's mostly substitution.",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=1, minutes=35)
        ),
        ChatMessage(
            chat_id=private_chats[2].id,
            sender_id=users[4].id,
            content="Got it. And question 5? The logic section confused me.",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=1, minutes=30)
        ),
        ChatMessage(
            chat_id=private_chats[2].id,
            sender_id=users[5].id,
            content="Focus on truth tables. Want me to walk through one?",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=1, minutes=25)
        ),
        ChatMessage(
            chat_id=private_chats[2].id,
            sender_id=users[4].id,
            content="Yes, please! That would help a lot.",
            created_at=datetime.datetime.now() - datetime.timedelta(hours=1, minutes=20)
        ),
    ]

    session.add_all(chat_messages)
    
    # Final commit
    session.commit()
    
    print("Test data successfully inserted into the database.")
    return True
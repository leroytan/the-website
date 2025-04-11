from api.storage.connection import engine
from api.storage.models import (Assignment, AssignmentRequest, AssignmentSlot,
                                AssignmentStatus, Client, ClientSubject, Level,
                                SpecialSkill, Subject, Tutor, TutorLevel,
                                TutorSpecialSkill, TutorSubject, User)
from sqlalchemy.orm import sessionmaker


def check_data():
    """Validate that all data has been inserted correctly into the database."""
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Validate Users
        users = session.query(User).all()
        if len(users) != 4:  # Expecting 2 clients + 2 tutors
            return False, f"Expected 4 users, found {len(users)}"

        # Validate Clients
        clients = session.query(Client).all()
        if len(clients) != 2:
            return False, f"Expected 2 clients, found {len(clients)}"
        client1 = session.query(Client).filter_by(email="john@example.com").first()
        if not client1 or client1.name != "John Doe" or client1.userType != UserType.CLIENT:
            return False, "Client 1 data is incorrect"

        # Validate Tutors
        tutors = session.query(Tutor).all()
        if len(tutors) != 2:
            return False, f"Expected 2 tutors, found {len(tutors)}"
        tutor1 = session.query(Tutor).filter_by(email="alice@example.com").first()
        if not tutor1 or tutor1.name != "Alice Johnson" or tutor1.userType != UserType.TUTOR:
            return False, "Tutor 1 data is incorrect"

        # Validate SpecialSkills
        skills = session.query(SpecialSkill).all()
        if len(skills) != 2:
            return False, f"Expected 2 special skills, found {len(skills)}"
        skill1 = session.query(SpecialSkill).filter_by(name="Mathematics").first()
        if not skill1:
            return False, "SpecialSkill 'Mathematics' not found"

        # Validate Subjects
        subjects = session.query(Subject).all()
        if len(subjects) != 2:
            return False, f"Expected 2 subjects, found {len(subjects)}"
        subject1 = session.query(Subject).filter_by(name="Algebra").first()
        if not subject1:
            return False, "Subject 'Algebra' not found"

        # Validate Levels
        levels = session.query(Level).all()
        if len(levels) != 2:
            return False, f"Expected 2 levels, found {len(levels)}"
        level1 = session.query(Level).filter_by(name="High School").first()
        if not level1:
            return False, "Level 'High School' not found"

        # Validate Assignments
        assignments = session.query(Assignment).all()
        if len(assignments) != 2:
            return False, f"Expected 2 assignments, found {len(assignments)}"
        assignment1 = session.query(Assignment).filter_by(clientId=client1.id).first()
        if not assignment1 or assignment1.status != AssignmentStatus.PENDING:
            return False, "Assignment 1 data is incorrect"

        # Validate AssignmentSlots
        slots = session.query(AssignmentSlot).all()
        if len(slots) != 2:
            return False, f"Expected 2 assignment slots, found {len(slots)}"
        slot1 = session.query(AssignmentSlot).filter_by(assignment_id=assignment1.id).first()
        if not slot1 or slot1.day != "Monday":
            return False, "AssignmentSlot 1 data is incorrect"

        # If all checks pass
        return True, "All data has been inserted correctly"

    except Exception as e:
        return False, f"Validation failed with error: {str(e)}"

    finally:
        session.close()
from datetime import datetime

from api.storage.connection import engine
from api.storage.models import (Assignment, AssignmentRequest, AssignmentSlot,
                                AssignmentStatus, Client, ClientSubject, Level,
                                SpecialSkill, Subject, Tutor, TutorLevel,
                                TutorRequest, TutorSpecialSkill, TutorSubject,
                                User, UserType)
from sqlalchemy.orm import sessionmaker


def insert_test_data():

    # Create a configured "Session" class
    Session = sessionmaker(bind=engine)

    # Create a Session
    session = Session()

    # Adding Users
    client1 = Client(name="John Doe", email="john@example.com", contact="1234567890", userType=UserType.CLIENT, passwordHash="hash1", school="High School", level="Grade 12")
    client2 = Client(name="Jane Smith", email="jane@example.com", contact="0987654321", userType=UserType.CLIENT, passwordHash="hash2", school="College", level="Year 2")
    tutor1 = Tutor(name="Alice Johnson", email="alice@example.com", contact="1122334455", userType=UserType.TUTOR, passwordHash="hash3", photoUrl="url1", highestEducation="Masters", rate="30", location="City1", rating=4.5, aboutMe="Experienced tutor")
    tutor2 = Tutor(name="Bob Brown", email="bob@example.com", contact="5566778899", userType=UserType.TUTOR, passwordHash="hash4", photoUrl="url2", highestEducation="PhD", rate="50", location="City2", rating=4.8, aboutMe="Specialist in Mathematics")

    session.add_all([client1, client2, tutor1, tutor2])
    session.commit()

    # Adding SpecialSkills
    skill1 = SpecialSkill(name="Piano")
    skill2 = SpecialSkill(name="Patient with children")

    session.add_all([skill1, skill2])
    session.commit()

    # Adding Subjects
    subject1 = Subject(name="Mathematics")
    subject2 = Subject(name="Physics")

    session.add_all([subject1, subject2])
    session.commit()

    # Adding Levels
    level1 = Level(name="Lower Primary")
    level2 = Level(name="Upper Primary")

    session.add_all([level1, level2])
    session.commit()

    # # Adding TutorSpecialSkills
    # tutor_skill1 = TutorSpecialSkill(tutorId=tutor1.id, specialSkillId=skill1.id)
    # tutor_skill2 = TutorSpecialSkill(tutorId=tutor2.id, specialSkillId=skill2.id)

    # session.add_all([tutor_skill1, tutor_skill2])
    # session.commit()

    # # Adding TutorSubjects
    # tutor_subject1 = TutorSubject(tutorId=tutor1.id, subjectId=subject1.id)
    # tutor_subject2 = TutorSubject(tutorId=tutor2.id, subjectId=subject2.id)

    # session.add_all([tutor_subject1, tutor_subject2])
    # session.commit()

    # Adding ClientSubjects
    client_subject1 = ClientSubject(clientId=client1.id, subjectId=subject1.id)
    client_subject2 = ClientSubject(clientId=client2.id, subjectId=subject2.id)

    session.add_all([client_subject1, client_subject2])
    session.commit()

    # # Adding TutorLevels
    # tutor_level1 = TutorLevel(tutorId=tutor1.id, levelId=level1.id)
    # tutor_level2 = TutorLevel(tutorId=tutor2.id, levelId=level2.id)

    # session.add_all([tutor_level1, tutor_level2])
    # session.commit()

    # Adding Assignments
    assignment1 = Assignment(datetime=datetime.now(), clientId=client1.id, tutorId=tutor1.id, subjectId=subject1.id, estimatedRate="30", weeklyFrequency=2, specialRequests="Need help with integrals", status=AssignmentStatus.PENDING)
    assignment2 = Assignment(datetime=datetime.now(), clientId=client2.id, tutorId=tutor2.id, subjectId=subject2.id, estimatedRate="50", weeklyFrequency=1, specialRequests="Advanced topics", status=AssignmentStatus.ACCEPTED)

    session.add_all([assignment1, assignment2])
    session.commit()

    # Adding AssignmentSlots
    slot1 = AssignmentSlot(assignmentId=assignment1.id, day="Monday", startTime="10:00", endTime="12:00")
    slot2 = AssignmentSlot(assignmentId=assignment2.id, day="Wednesday", startTime="14:00", endTime="16:00")

    session.add_all([slot1, slot2])
    session.commit()

    # Adding TutorRequests
    tutor_request1 = TutorRequest(tutorId=tutor1.id, clientId=client1.id, datetime=datetime.now())
    tutor_request2 = TutorRequest(tutorId=tutor2.id, clientId=client2.id, datetime=datetime.now())

    session.add_all([tutor_request1, tutor_request2])
    session.commit()

    # Adding AssignmentRequests
    assignment_request1 = AssignmentRequest(assignmentId=assignment1.id, tutorId=tutor1.id, datetime=datetime.now())
    assignment_request2 = AssignmentRequest(assignmentId=assignment2.id, tutorId=tutor2.id, datetime=datetime.now())

    session.add_all([assignment_request1, assignment_request2])
    session.commit()

    # Close the session
    session.close()
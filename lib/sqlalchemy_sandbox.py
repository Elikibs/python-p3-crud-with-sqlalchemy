#!/usr/bin/env python3

from datetime import datetime

from sqlalchemy import (create_engine, desc, func,
    CheckConstraint, PrimaryKeyConstraint, UniqueConstraint,
    Index, Column, DateTime, Integer, String)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'

    __table_args__ = (
        PrimaryKeyConstraint(
            'id',
            name= 'id_pk'
        ),
        UniqueConstraint(
            'email',
            name= 'unique_email'
        ),
        CheckConstraint(
            'grade BETWEEN 1 and 12',
            name= 'grade_between_1_and_12'
        )
    )

    Index('index_name', 'name')

    id = Column(Integer())
    name = Column(String())
    email = Column(String(55))
    grade = Column(Integer())
    birthday = Column(DateTime())
    enrolled_date = Column(DateTime(), default=datetime.now())

    def __repr__(self):
        return f"Student {self.id}: " \
            + f"{self.name}, " \
            + f"Grade {self.grade}"

if __name__ == '__main__':
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)


    # use our engine to configure a 'Session' class
    Session = sessionmaker(bind=engine)
    # use 'Session' class to create 'session' object
    session = Session()

    # creating a new record in our db
    elisha_kibet = Student(
        name="Elisha Kibet",
        email="elishakibet67@gmail.com",
        grade=8,
        birthday= datetime(
            year=2002,
            month=12,
            day=6
        ),
    )

    alan_turing = Student(
        name="Alan Turing",
        email="alan.turing@sherborne.edu",
        grade=11,
        birthday=datetime(
            year=1912,
            month=6,
            day=23
        ),
    )

    #Saving one record
    # session.add(elisha_kibet)

    # saving multiple records
    session.bulk_save_objects([elisha_kibet, alan_turing])
    session.commit()

    print(f"New Srudent ID is {elisha_kibet.id}.")
    print(f"New student ID is {alan_turing.id}.")

    # retrieving records from db
    students = session.query(Student).all()
    print(students)

    # selecting only certain columns
    names = [name for name in session.query(Student.name)]
    print(names)

    # ordering
    students_by_name = [student for student in session.query(Student.name).order_by(Student.grade)]
    print(students_by_name)

    # sort results in descending order use the 'desc()' function
    students_by_grade_desc = [student for student in session.query(Student.name, Student.grade).order_by(desc(Student.grade))]
    print(students_by_grade_desc)

    # limiting
    oldest_student = [student for student in session.query(Student.name, Student.birthday).order_by(desc(Student.grade)).limit(1)]
    print(oldest_student)

    # 'first() method, fucntions the same as limit(1) and does not require a list interpretation
    oldest_student = session.query(Student.name, Student.birthday).order_by(desc(Student.grade)).first()
    print(oldest_student)

    # 'func()' for operations ie. count(), sum()
    student_count = session.query(func.count(Student.id)).first()
    print(student_count)

    # filtering; retrieving specific records
    query = session.query(Student).filter(Student.name.like('%Alan%'), Student.grade == 11)
    for record in query:
        print(record.name)

    # update() method
    session.query(Student).update({
        Student.grade: Student.grade + 1
    })
    print([(
        student.name,
        student.grade
    ) for student in session.query(Student)])

    #deleting a record
    query = session.query(Student).filter(Student.name == "Elisha Kibet")
    elisha_kibet = query.first()

    # 'delete()
    session.delete(elisha_kibet)
    session.commit()

    # check if deleted by trying to retrive the data again
    elisha_kibet = query.first()
    print(elisha_kibet)
# Use faker library to generate fake data and dump to postgresql database

import psycopg2
import os
import faker
import random
from faker.providers import BaseProvider
from faker import Faker


conn = psycopg2.connect(
        host=os.environ['PGHOST'],
        port=os.environ['PGPORT'],
        user=os.environ['PGUSER'],
        database=os.environ['PGDATABASE']
    )

# Create a Faker object
faker = faker.Faker()

# Create a cursor
cur = conn.cursor()

# Create the students table
cur.execute('''CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    duke_id VARCHAR(255),
    major VARCHAR(255),
    graduation_year INTEGER
);''')

# Create the courses table
cur.execute('''CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    department VARCHAR(255),
    course_number VARCHAR(255),
    credits INTEGER
);''')

# Create the enrollments table
cur.execute('''CREATE TABLE enrollments (
    student_id INTEGER REFERENCES students(id),
    course_id INTEGER REFERENCES courses(id),
    grade VARCHAR(255)
);''')

# Create the transcripts table
cur.execute('''CREATE TABLE transcripts (
    student_id INTEGER REFERENCES students(id),
    course_id INTEGER REFERENCES courses(id),
    grade VARCHAR(255),
    semester VARCHAR(255)
);''')

# Create the degrees table
cur.execute('''CREATE TABLE degrees (
    student_id INTEGER REFERENCES students(id),
    degree VARCHAR(255),
    major VARCHAR(255),
    graduation_date DATE
);''')


# create new provider class
class MajorProvider(BaseProvider):
    def major(self) -> str:
        majors = ['Computer Science', 'Mathematics', 'Physics', 
                  'Biology', 'Chemistry', 'Economics', 'English', 
                  'History', 'Political Science', 'Psychology', 'Sociology']
        return random.choice(majors)

# then add new provider to faker instance
fake = Faker()
fake.add_provider(MajorProvider)

# Insert fake data into the tables
# Students table
for i in range(100):
    cur.execute('''INSERT INTO students
                (name, email, duke_id, major, graduation_year) 
                VALUES (%s, %s, %s, %s, %s)''',
                (faker.name(), 
                 faker.email(), 
                 faker.uuid4(), 
                 fake.major(), 
                 faker.year()))

# Courses table

class CourseProvider(BaseProvider):
    def course_name(self) -> str:
        course_names = ['Data Eng', 'Data Model', 'NLP', 
                  'Cal 1', 'Cal 2', 'Probabilty', 'Statistics',
                  'Stochastic', 'Convex Opt', 'Non Convex opt', 'ML']
        return random.choice(course_names)
fake.add_provider(CourseProvider)

class DepartProvider(BaseProvider):
    def department_name(self) -> str:
        department_names = ['SSRI', 'MATHS', 'STATS']
        return random.choice(department_names)
fake.add_provider(DepartProvider)

class CourseCodeProvider(BaseProvider):
    def course_code(self) -> str:
        course_codes = ['IDS111', 'IDS112', 'IDS113', 
                  'IDS114', 'MATH111', 'MATH112', 'MATH113', 
                  'MATH114', 'MATH115', 'MATH116', 'MATH117']
        return random.choice(course_codes)
fake.add_provider(CourseCodeProvider)

for i in range(50):
    cur.execute('''INSERT INTO courses 
                (name, department, course_number, credits) 
                VALUES (%s, %s, %s, %s)''',
                (fake.course_name(), 
                 fake.department_name(), 
                 fake.course_code(), 
                 faker.random_int(2, 4)))

# Enrollments table
for i in range(1000):
    cur.execute('''INSERT INTO enrollments 
                (student_id, course_id, grade) 
                VALUES (%s, %s, %s)''',
                (faker.random_int(1, 100), 
                 faker.random_int(1, 50), 
                 faker.random_int(0, 100)))

# Transcripts table
for i in range(1000):
    cur.execute('''INSERT INTO transcripts 
                (student_id, course_id, grade, semester) 
                VALUES (%s, %s, %s, %s)''',
                (faker.random_int(1, 100), 
                 faker.random_int(1, 50), 
                 faker.random_int(0, 100), 
                 faker.random_int(1, 4)))

# Degrees table

class DegreeProvider(BaseProvider):
    def degree_name(self) -> str:
        degree_names = ['MIDS', 'Health Analytics', 'MBA']
        return random.choice(degree_names)
fake.add_provider(DegreeProvider)

for i in range(100):
    cur.execute('''INSERT INTO degrees 
                (student_id, degree, major, graduation_date) 
                VALUES (%s, %s, %s, %s)''',
                (faker.random_int(1, 100), 
                 fake.degree_name(), 
                 fake.major(), 
                 faker.date()))

# usual boilerplate to commit and close
conn.commit()
cur.close()
conn.close()

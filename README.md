[![CI](https://github.com/nogibjj/python-template/actions/workflows/cicd.yml/badge.svg)](https://github.com/nogibjj/python-template/actions/workflows/cicd.yml)
## SQL aggregations

In this repo, we demostrate the power of a managed cloud database on Azure Cloud with the `faker` python library 

To flow along Clone this repository or download the script.

Open the script (`utils/data_dump.py`), one request the connection params can be shared safely.

To dump the data using the script:
Run 
```python
python3 utils/data_dump.py
```
This will create tables and populate them with fake student data.
### Tables Created
`students`: Contains student information such as name, email, Duke ID, major, and graduation year.
`courses`: Stores course details including name, department, course number, and credits.
`enrollments`: Records student enrollments in courses with corresponding grades.
`transcripts`: Stores student transcripts with grades and semester information.
`degrees`: Contains data about degrees pursued by students, including the degree name, major, and graduation date.

An example complex query for the data is below
```python
cur.execute('''
SELECT students.name, students.duke_id, 
            COUNT(enrollments.course_id) AS total_courses, 
            SUM(CAST(enrollments.grade AS DECIMAL(10,2))) AS total_grade_points, 
            AVG(CAST(enrollments.grade AS DECIMAL(10,2))) AS score
FROM students
INNER JOIN enrollments ON students.id = enrollments.student_id
GROUP BY students.name, students.duke_id
ORDER BY score DESC;
''')
```
This query retrieves a list of students along with their Duke IDs, the total number of courses they've enrolled in, the total grade points they've earned across all courses, and their average grade point average  across all courses. The result set is ordered by the average score in descending order, so students with higher score appear at the top of the list As follows:

`SELECT Clause`

`students.name`: It selects the name column from the students table, which represents the name of each student.
`students.duke_id`: It selects the duke_id column from the students table, which is assumed to be a unique identifier for each student.
`COUNT(enrollments.course_id) AS total_courses`: It calculates the total number of courses each student has enrolled in and aliases the result as total_courses.
`SUM(CAST(enrollments.grade AS DECIMAL(10,2))) AS total_grade_points`: It calculates the sum of grade points earned by a student across all courses. The CAST function is used to convert the grade column (assumed to be numeric) into a decimal with two decimal places. The result is aliased as `total_grade_points`.
`AVG(CAST(enrollments.grade AS DECIMAL(10,2))) AS score`: It calculates the average score (grade point average) of a student across all courses. Again, the CAST function is used to ensure that the grade column is treated as a decimal with two decimal places. The result is aliased as score.

`FROM Clause`

students: It specifies the students table as the primary table for the query.
`INNER JOIN` `enrollments ON students.id = enrollments.student_id`: It performs an inner join between the students and enrollments tables based on the id column in the students table and the `student_id` column in the enrollments table. This join links students to their course enrollments.

`GROUP BY Clause`

`GROUP BY students.name, students.duke_id`: It groups the results by the name and `duke_id` columns of the students table. This means that the calculations in the `SELECT` clause will be performed for each unique combination of a student's name and Duke ID.

`ORDER BY Clause`

`ORDER BY score DESC`: It orders the result set in descending order based on the calculated score (average grade point average) column. Students with higher average scores will appear at the top of the result set.

### Example output
![Output](/results/output.png?raw=true)


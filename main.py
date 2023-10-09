"""
Main cli or app entry point
"""

import psycopg2
import tabulate
from tabulate import tabulate
import os

# Connect to the database
conn = psycopg2.connect(
    host=os.environ['PGHOST'],
    port=os.environ['PGPORT'],
    user=os.environ['PGUSER'],
    database=os.environ['PGDATABASE']
)

cur = conn.cursor()
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

results = cur.fetchall()


cur.close()
conn.close()
headers = ['Name', 'Duke ID', 'Total Courses', 'Total Grade Points', 'Average_Score']
print(tabulate(results, headers=headers, tablefmt='pipe'))

# Save the results to a CSV file
with open('results.csv', 'w') as f:
    f.write('name,duke_id,total_courses,total_grade_points,score\n')

    for result in results:
        f.write('{},{},{},{},{}\n'.format(*result))

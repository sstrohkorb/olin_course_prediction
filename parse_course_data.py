import csv
from Student import *
from Course import *
from Course_Offering import *
from Graduating_Class import *
from Major import *
from Professor import *

# ['Academic Status Code',
#  'Degree Grant Year',
#  'Student ID Number',
#  'AcadYr_Session',
#  'Gender Code',
#  'Session Classification Code',
#  'Session Major 1 Description',
#  'Concentration 1 Description',
#  'Course Work Course Number',
#  'Section Number',
#  'Course Work Course Title',
#  'Section Title (Actual)',
#  'Faculty Full Name (Last, First)']

students = {} #id:Student
courses = {} #course_number:Course
professors = {}#name:Professor

with open('../anonymizeddata_UpToFall2013.csv','rb') as f:
    contents = csv.reader(f)
    matrix = list()
    for row in contents:
    	academic_status = row[0].strip()
    	grad_year = row[1].strip()
    	stud_id = row[2].strip()
    	course_semester = row[3].strip()
    	gender = row[4].strip()
    	year = row[5].strip() # year when student took course (eg FF, FR, SO, ..)
    	major = row[6].strip()
    	concentration = row[7].strip()
    	course_number = row[8].strip()
    	section_no = row[9].strip()
    	course_title = row[10].strip()
    	section_title = row[11].strip()
    	professor_name = row[12].strip()

    	if academic_status == 'Academic Status Code':
    		continue



    	courses[course_number] = courses.get(course_number, Course(course_title, course_number))
    	course = courses[course_number]
    	professors[professor_name] = professors.get(professor_name, Professor(professor_name))
    	# (self, semester, section_title, section_no, Course)
    	course_offering = Course_Offering(course_semester, section_title, section_no, course)
    	course_offering.set_professor(professors[professor_name])


    	if stud_id not in students:
    		#(self, ID, gender, graduating_class, major, academic_status)
    		new_student = Student(stud_id, gender, grad_year, major, academic_status)
    		students[stud_id] = new_student

    	students[stud_id].add_course_offering(course_offering)

    	if students[stud_id].major == 'Undeclared' and major != 'Undeclared':
    		students[stud_id].major = major

course_list = []
for course in courses:
    course_list.append((courses[course].course_number, courses[course].title))
    course_list.sort()

for (a,b) in course_list:
    print a + "\t : " + b







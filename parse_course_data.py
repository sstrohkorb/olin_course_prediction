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

def get_course_data(filename):
    students = {} #id:Student
    courses = {} #course_number:Course
    professors = {}#name:Professor

    with open(filename,'rb') as f:
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

            # keys = course #
            # values = equivalent course #
            equivalent_courses = {}

            # Populating equivalent courses with the AHS/AHSE stuff
            
            if course_number == 'AHS1110':
                course_number = 'AHSE1100'
            if course_number == 'AHS1111':
                course_number = 'AHSE2131'
            if course_number == 'AHS1140':
                course_number = 'AHSE2120'

            if 'AHS' in course_number and 'AHSE' not in course_number:
                course_number = course_number[:3] + 'E' + course_number[3:]


            # Populating equivalent courses with the Speical Topics stuff
            special_topics = ['AHSE2199','AHSE3199','AHSE3599','AHSE4199','ENGR1199','ENGR2199','ENGR2299','ENGR2599','ENGR2699','ENGR3199','ENGR3299','ENGR3399','ENGR3499','ENGR3599','ENGR3699','ENGR3899','MTH2188','MTH2199','MTH3199','SCI2099','SCI2199','SCI2299','SCI2399','SCI3199']
            for st in special_topics:
                for letter in 'ABC':
                    equivalent_courses[st+letter] = st


            # Populating equivalent courses with other random stuff
            if course_number.endswith('X'):
                course_number = course_number[:-1]

            if course_number in equivalent_courses:
                course_number = equivalent_courses[course_number]

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

    return [students, courses, professors]







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

    with open(filename,'rU') as f:
        contents = csv.reader(f)
        matrix = list()
        for row in contents:
            academic_status = row[0].strip()
            grad_year = row[1].strip()
            stud_id = row[2].strip()
            course_semester = row[3].strip()
            gender = row[4].strip()
            student_semester_str = row[5].strip() # year when student took course (eg FF, FR, SO, ..)
            major = row[6].strip()
            concentration = row[7].strip()
            course_number = row[8].strip()
            section_no = row[9].strip()
            course_title = row[10].strip()
            section_title = row[11].strip()
            professor_name = row[12].strip()

            if academic_status == 'Academic Status Code':
                continue

            # Don't include Lab classes 
            if ' L' in course_number:
                continue

            
            # Combine the course_semester and year into one meaningful variable that describes
            # what the student's standing is at the time they take a course offering by semester
            # number (from 0 to 7)

            if student_semester_str == 'TF': student_semester_str = 'FF'
            
            student_semester_no = 0     # 'FF'

            if student_semester_str == 'FR':
                student_semester_no = 1
            elif student_semester_str == 'SO':
                student_semester_no = 2
            elif student_semester_str == 'JR':
                student_semester_no = 4
            elif student_semester_str == 'SR':
                student_semester_no = 6

            if 'SP' in course_semester: student_semester_no += 1

            # Cleaning course data by setting equivalent course information
            
            # keys = course #
            # values = equivalent course #
            equivalent_courses = {}

            classes_to_convert = [
                ('AHS1110', 'AHSE1100'),
                ('AHS1111', 'AHSE2131'),
                ('AHS1140', 'AHSE2120'),
                ('FND2710', 'SCI1210'),     # Mod Bio
                ('ENG1510', 'ENGR2510')     # Software design (before it was Soft Des)
            ]
            for old, current in classes_to_convert:
                equivalent_courses[old] = current

            # Populating equivalent courses with the Speical Topics stuff
            special_topics = ['AHSE2199','AHSE3199','AHSE3599','AHSE4199','ENGR1199','ENGR2199','ENGR2299','ENGR2599','ENGR2699','ENGR3199','ENGR3299','ENGR3399','ENGR3499','ENGR3599','ENGR3699','ENGR3899','MTH2188','MTH2199','MTH3199','SCI2099','SCI2199','SCI2299','SCI2399','SCI3199']
            for st in special_topics:
                for letter in 'ABC':
                    equivalent_courses[st+letter] = st

            if course_number in equivalent_courses:
                course_number = equivalent_courses[course_number]

            # AHS vs. AHSE problem 
            if 'AHS' in course_number and 'AHSE' not in course_number:
                course_number = course_number[:3] + 'E' + course_number[3:]


            # Removing the X on the end of course numbers (For an IS)
            if course_number.endswith('X'):
                course_number = course_number[:-1]

            courses[course_number] = courses.get(course_number, Course(course_title, course_number))
            course = courses[course_number]
            course.total_number_of_students += 1
            professors[professor_name] = professors.get(professor_name, Professor(professor_name))
            # (self, semester, section_title, section_no, Course)
            course_offering = Course_Offering(course_semester, student_semester_no, section_title, section_no, course)
            course_offering.set_professor(professors[professor_name])


            if stud_id not in students:
                #(self, ID, gender, graduating_class, major, academic_status)
                new_student = Student(stud_id, gender, grad_year, major, academic_status, concentration)
                students[stud_id] = new_student

            students[stud_id].add_course_offering(course_offering)

            if students[stud_id].major == 'Undeclared' and major != 'Undeclared':
                students[stud_id].major = major

            students[stud_id].major_history[student_semester_no] = major
    
    for s in students:
        students[s].set_final_semester()
        students[s].set_major_history()

    return [students, courses, professors]







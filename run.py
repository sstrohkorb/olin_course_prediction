from make_train_test_data import *
from parse_course_data import *

def initialize_input_data(enrollment_history_filepath='../course_enrollments_2002-2014spring_anonymized.csv', prereg_data_filepath="../pre_reg_survey_data/*"):
    [students, courses, professors] = get_course_data(enrollment_history_filepath)
    prereg_data = get_prereg_data(prereg_data_filepath)
    enter_prereg_data(courses, prereg_data)

    all_courses_list = []
    for course in courses: 
        all_courses_list.append([courses[course].course_number, courses[course].title])

    return students, courses, all_courses_list

def make_random_train_test(students, all_courses_list, desired_course, current_semester, desired_semester, starting_semester, ending_semester):
    [x_matrix, y_values] = make_student_feature_data(students, all_courses_list, desired_course, current_semester, desired_semester, starting_semester, ending_semester)
    [x_train, y_train, x_test, y_test] = make_random_training_data(x_matrix, y_values, len(y_values)/2)
    return [x_train, y_train, x_test, y_test]

def make_semester_specific_train_test(students, all_courses_list, desired_course, current_semester, desired_semester, starting_semester, ending_semester):
    current_students, past_students = get_current_and_past_students(students, ending_semester)
    [x_train, y_train] = make_student_feature_data(past_students, all_courses_list, desired_course, current_semester, desired_semester, starting_semester, ending_semester)
    [x_test, y_test] = make_student_feature_data(current_students, all_courses_list, desired_course, current_semester, desired_semester, starting_semester, ending_semester)

if __name__ == '__main__':
    students, courses, all_courses_list = initialize_input_data()

    desired_course = 'ENGR3525' #Softsys
    current_semester = 2 #SO1
    desired_semester = 3 #SO2
    starting_semester = '0910FA'
    ending_semester = '1314SP'

    make_random_train_test(students, all_courses_list, desired_course, current_semester, desired_semester, starting_semester, ending_semester)

    make_semester_specific_train_test(students, all_courses_list, desired_course, current_semester, desired_semester, starting_semester, ending_semester)




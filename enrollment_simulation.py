import big_3_majors_linear_regression as bmlg
from parse_course_data import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import linear_model

def tune_c(x_vector, y_vector, all_courses_list, c_values=None, num_iter=20):

    averaged_results = []

    if c_values is None:
        c_values = np.logspace(-1, 4, num=20)

    for c_value in c_values:
      temp_list = []
      for i in range(num_iter):
        [actual_result, description] = bmlg.prediction_strength_for_a_course(x_vector, y_vector, all_courses_list, 20, c_value)
        temp_list.append(actual_result)
      averaged_result = sum(temp_list)/len(temp_list)
      averaged_results.append(averaged_result)

    max_result = max(averaged_results)
    best_c = c_values[averaged_results.index(max_result)]
    return best_c, max_result, averaged_results

def expected_enrollment_for_course(x_train, y_train, x_test, c_value):
    """
    for a given course, find the probabilities of taking that course
    """
    logistic = linear_model.LogisticRegression(C=c_value)
    logistic.fit(x_train, y_train)

    prob = logistic.predict_proba(x_test)
    return [(1-p[0]) for p in prob]

def true_enrollment(students, courses, semester):
    """
    find true enrollment in all courses for a given semester
    """
    course_list = []
    for course in courses:
        course_list.append(course[0])

    course_dict = {course_list[i]: i for i in range(len(course_list))}

    enrollment = [0] * len(courses)

    for s in students:
        for c in s.list_of_course_offerings:
            course_no = c.course.course_number
            enrollment[course_dict[course_no]] += 1

    return enrollment


def get_testing_sets(students, semester):
    """
    return list of students who are enrolled that semester
    and students who were enrolled previous to that semester
    """
    # note that students who are away during semester will be considered past students
    # even if they are enrolled in later semesters
    current_students = [{} for i in range(8)]
    non_current_students = {} #students who are not enrolled in given semester
    past_students = {} #students who are not current but were enrolled previously
    for s_id in students:
        student = students[s_id]
        # find all current students
        for c in student.list_of_course_offerings:
            if c.semester == semester:
                current_students[c.student_semester_no][s_id] = student
                break

        if student in current_students:
            continue
        # find all past students if not current
        for c in student.list_of_course_offerings:
            if c.semester < semester:
                # Kludge warning! This relies on a lexicographic string comparison
                past_students[s_id] = student
                break
    return current_students, past_students




if __name__ == '__main__':
    [students, courses, professors] = get_course_data('../course_enrollments_2002-2014spring_anonymized.csv')
    
    all_courses_list = []
    for course in courses: 
        all_courses_list.append([courses[course].course_number, courses[course].title])

    current_students, past_students = get_testing_sets(students, '1314FA')
    for sem in current_students:
        print len(sem)

    c_vals = np.logspace(-1, 4, num=10)

    # course = 'ENGR3525' #softsys
    course = 'ENGR2250' #uocd
    # course = 'ENGR3380' #dfm
    # current_semester = 2
    # desired_semester = 3
    starting_semester = '0203FA'
    end_sem = '1314FA'
    expected_enrollement = 0
    #TODO: only look at spring semesters, weight c-values?
    for current_semester in range(7):
        if len(current_students[current_semester]) == 0:
            continue
        desired_semester = current_semester + 1
        [x_vector, y_vector] = bmlg.create_course_enrollment_data(students, all_courses_list, professors, starting_semester, course, current_semester, desired_semester, ending_semester=end_sem)
        [x_test, y_test] = bmlg.create_course_enrollment_data(current_students[current_semester], all_courses_list, professors, starting_semester, course, current_semester, current_semester, ending_semester=end_sem)
        if len(x_vector) < 5 or len(x_test) < 1:
            continue

        best_c, max_result, averaged_results = tune_c(x_vector, y_vector, all_courses_list, c_values=c_vals, num_iter=3)
        print 'best c: %s'%best_c
        print 'max_result:%s'%max_result

        enr_for_sem = sum(expected_enrollment_for_course(x_vector, y_vector, x_test, best_c))
        print 'enrollment for semester %s: %s'%(current_semester, enr_for_sem)
        expected_enrollement += enr_for_sem

    print 'total expected enrollment: %s'%(expected_enrollement)

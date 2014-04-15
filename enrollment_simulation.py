import big_3_majors_linear_regression as bmlg
from parse_course_data import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import linear_model
import math

def tune_c(x_vector, y_vector, all_courses_list, c_values=None, num_iter=100):
    """
    Finds the c value that yields the maximal area under the ROC for a given
    x_vector and y_vector
    Parameters:
        x_vector : list of lists containing attribute data for each student
        y_vector : list of classification of each student
        all_courses_list: this is the list of all courses used to generate the data
        c_values: list of c values to sweep, default is np.logspace(-1, 4, num=20)
        num_iter: number of times area under the roc is computed for each c value
    """

    averaged_results = []

    if c_values is None:
        c_values = np.logspace(-1, 4, num=20)

    for c_value in c_values:
      [averaged_result, description] = bmlg.prediction_strength_for_a_course(x_vector, y_vector, all_courses_list, num_iter, c_value)
      averaged_results.append(averaged_result)

    max_result = max(averaged_results)
    best_c = c_values[averaged_results.index(max_result)]
    return best_c, max_result, averaged_results

def sweep_c_squared_error(x_train, y_train, x_test, true_enrollment, c_values=None):
    if c_values is None:
        c_values = np.logspace(-1, 4, num=20)
    # true_enrollment = sum(y_test)
    error = []

    for c_value in c_values:
        logistic = linear_model.LogisticRegression(C=c_value)
        logistic.fit(x_train, y_train)

        prob = logistic.predict_proba(x_test)

        expected_enrollement = sum([(1-p[0]) for p in prob])
        squared_error = (true_enrollment - expected_enrollement) ** 2
        error.append(squared_error)

    return c_values, error

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
        for semester_course_offerings in s.list_of_course_offerings:
            for c in semester_course_offerings:
                course_no = c.course.course_number
                enrollment[course_dict[course_no]] += 1

    return enrollment



def simulate_course(students, all_courses_list, professors, course, current_students, c_vals, num_iter=100, start_sem='0607FA', end_sem='1314FA'):
    """
    Get expected enrollment for course
    """
    # starting_semester = '0203FA'
    starting_semester = start_sem
    expected_enrollments = [0] * 7
    max_rocs = [0] * 7
    #TODO: only look at spring semesters, weight c-values?
    for current_semester in range(7):
        if len(current_students[current_semester]) == 0:
            continue
        desired_semester = current_semester + 1
        [x_vector, y_vector] = bmlg.create_course_enrollment_data(students, all_courses_list, professors, starting_semester, course, current_semester, desired_semester, ending_semester=end_sem)
        [x_test, y_test] = bmlg.create_course_enrollment_data(current_students[current_semester], all_courses_list, professors, starting_semester, course, current_semester, current_semester, ending_semester=end_sem)
        if len(x_vector) < 5 or len(x_test) < 1:
            continue

        best_c, max_result, averaged_results = tune_c(x_vector, y_vector, all_courses_list, c_values=c_vals, num_iter=num_iter)
        # print 'best c: %s'%best_c
        # print 'max_result:%s'%max_result
        max_rocs[current_semester] = max_result

        expected_enrollments[current_semester] = sum(expected_enrollment_for_course(x_vector, y_vector, x_test, best_c))
        
    total_expected = sum(expected_enrollments)
    try:
        weighted_avg_roc = sum(map(lambda x,y: x*y, max_rocs, expected_enrollments))/ total_expected
    except ZeroDivisionError:
        weighted_avg_roc = 0

    return total_expected, weighted_avg_roc, expected_enrollments, max_rocs

def sweep_c_for_course(students, all_courses_list, professors, course, current_students, c_vals=None, start_sem='0607FA', end_sem='1314FA'):
    """
    Get expected enrollment for course
    """
    # starting_semester = '0203FA'
    starting_semester = start_sem
    best_c_vals = [] #list of tuples: (best_c, true_enrollment)
    #TODO: only look at spring semesters, weight c-values?
    for current_semester in range(7):
        if len(current_students[current_semester]) == 0:
            continue
        desired_semester = current_semester + 1
        [x_vector, y_vector] = bmlg.create_course_enrollment_data(students, all_courses_list, professors, starting_semester, course, current_semester, desired_semester, ending_semester=end_sem)
        [x_test, y_test] = bmlg.create_course_enrollment_data(current_students[current_semester], all_courses_list, professors, starting_semester, course, current_semester, current_semester, ending_semester=end_sem)
        if len(x_vector) < 1 or len(x_test) < 1:
            continue

        true_enrollment = sum(y_test)
        print "true enrollment: %s"%true_enrollment

        c_values, error = sweep_c_squared_error(x_vector, y_vector, x_test, true_enrollment, c_values=c_vals)
        print course
        print 'error: %s'%str(error)
        print 'c_vals: %s'%str(c_values)

        best_c = sorted(zip(c_values,error), key=lambda x: x[1])[0][0]
        best_c_vals.append((best_c, true_enrollment))
        plt.plot(c_values, error, label=str(current_semester))

    # title = [c[1] for c in all_courses_list if c[0] == course]

    # plt.xscale('log')
    # plt.legend()
    # plt.title('%s: %s'%(course, title[0]))
    # plt.show()

    return best_c_vals


if __name__ == '__main__':
    [students, courses, professors] = get_course_data('../course_enrollments_2002-2014spring_anonymized.csv')
    
    all_courses_list = []
    for course in courses: 
        all_courses_list.append([courses[course].course_number, courses[course].title])

    current_students, past_students = get_testing_sets(students, '1314FA')
    for sem in current_students:
        print len(sem)

    c_vals = np.logspace(-1, 4, num=10)



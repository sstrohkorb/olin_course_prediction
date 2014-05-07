Olin Course Prediction
======================

An attempt to predict the enrollment of Olin College courses based on preregistration survey data and Olin's course history. 

# Usage

    python olin_course_prediction.py

# Predictive Model

We used scikit learn's Linear Regression model: 

http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html 

Using the linear regression model, we can predict whether or not a student is likely to take a course in a specific semester, given their grade level. 

So, to predict the enrollment of Software Design in the 1415FA semester, we make 4 separate linear regression models, one for each grade of students. These models consider the course histories of all students, noting those who took Software Design in the fall semester of the specified grade as well as the preregistration data for how many students within that grade said that they would take Software Design. The model then predicts for each student at Olin that semester the probability that the student would take Software Design. These probabilities are summed to determine the predicted total enrollment of the course. 
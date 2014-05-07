Olin Course Prediction
======================

An attempt to predict the enrollment of Olin College courses based on preregistration survey data and Olin's course history. 

# Usage

    python olin_course_prediction.py

# Predictive Model

We used scikit learn's Linear Regression model: 
http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html 
Using the linear regression model, we can predict whether or not a student is likely to take a course in a specific semester, given their grade level. 
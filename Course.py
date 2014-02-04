class Course: 
  
  def __init__(self, title, course_number):
    self.title = title
    self.course_number = course_number

  def __str__(self):
    return self.course_number + ' : ' + self.title


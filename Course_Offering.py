class Course_Offering: 
  
  def __init__(self, semester, student_semester_no, section_no, Course):
    self.semester = semester
    self.student_semester_no = student_semester_no #FF, FR, SO, JR, SR
    self.section_no = section_no
    self.professor = None
    self.course = Course

  def __str__(self):
    return self.course.title + ": " + self.section_no + ", " + self.semester + " -- " + self.professor

  def set_professor(self, professor):
    self.professor = professor


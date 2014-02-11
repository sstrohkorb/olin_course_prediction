class Course_Offering: 
  
  def __init__(self, semester, student_year, section_title, section_no, Course):
    self.semester = semester
    self.student_year = student_year #FF, FR, SO, JR, SR
    self.section_title = section_title
    self.section_no = section_no
    self.professor = None
    self.course = Course

  def __str__(self):
    return self.course.title + ": " + self.section_title + " - " + self.section_no + ", " + self.semester + " -- " + self.professor

  def set_professor(self, professor):
    self.professor = professor


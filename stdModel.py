class CourseModel():
    def __init__(self,id:int,subject:str,grade:str,\
            title:str,school:str,teacher:str):
        self.id = id
        self.subject = subject
        self.grade = grade
        self.title = title
        self.school = school
        self.teacher = teacher
    def add_plus_item(self,**kw):
        for k in kw.keys():
            expr = "self.{}='{}'".format(k,kw[k])
            exec(expr,globals(),locals())
    def generate_std_tuple(self):
        return (self.id,self.subject,self.grade,self.title,\
            self.school,self.teacher)
    def __str__(self):
        return "{} {} {} {} {} {}".format(self.id,\
            self.subject,self.grade,self.title,self.school,\
                self.teacher)
    def __repr__(self):
        return "<stdModel.CourseModel class> CONTENT:{} {} {} {} {} {}".format(self.id,\
            self.subject,self.grade,self.title,self.school,\
                self.teacher)
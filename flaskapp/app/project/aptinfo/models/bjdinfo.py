from project import db

class BjdInfo(db.Model):
    __tablename__ = '법정동정보'

    index = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    법정동코드 = db.Column(db.Integer,  unique=True, nullable=False)
    법정동명 = db.Column(db.String(30), unique=False, nullable=False)

    def __repr__(self):

        rtform = "<BjdInfo(index = '%s' ,법정동코드 = '%s', 법정동명 = '%s')>"
        return rtform % (self.index, self.법정동코드, self.법정동명)



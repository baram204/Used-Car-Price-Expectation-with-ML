from project import db

class UsedCar(db.Model):
    __tablename__ = 'used_car'

    index = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    brand = db.Column(db.String(16), unique=False, nullable=False)
    model = db.Column(db.String(16), unique=False, nullable=False)
    title = db.Column(db.String(200), unique=False, nullable=False)
    miles = db.Column(db.Integer, unique=False, nullable=False)
    vendor = db.Column(db.String(100), unique=False, nullable=False)
    photos = db.Column(db.Integer, unique=False, nullable=False)
    video = db.Column(db.Integer, unique=False, nullable=False)
    exterior_color = db.Column(db.String(16), unique=False, nullable=False)
    interior_color = db.Column(db.String(16), unique=False, nullable=False)
    transmission = db.Column(db.String(16), unique=False, nullable=False)
    drivetrain = db.Column(db.String(16), unique=False, nullable=False)
    star = db.Column(db.Float, unique=False, nullable=False)
    review_no = db.Column(db.String(16), unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        rtform = "<UsedCar(id = '%s', year = '%s', brand = '%s', model = '%s',title = '%s', miles = '%s', vendor = '%s', photos = '%s', video = '%s', exterior_color = '%s', interior_color = '%s', transmission = '%s', drivertrain = '%s', star = '%s', review_no = '%s', price = '%s)>"
        return rtform % (
            self.index, self.year, self.brand, self.model,
            self.title, self.miles, self.vendor,
            self.photos, self.video, self.exterior_color,
            self.interior_color, self.transmission, self.drivetrain,
            self.star, self.review_no, self.price,)

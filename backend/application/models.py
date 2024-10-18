from application.database import db

class Admin(db.Model):
    __tablename__ = "admin"
    admin_email = db.Column(db.String(100), primary_key=True, unique=True)
    admin_password = db.Column(db.String, nullable=False)

    def to_json(self):
        return {
            "admin_email": self.admin_email,
            "admin_password": self.admin_password
        }

class Professional(db.Model):
    __tablename__ = "professional"
    prof_email = db.Column(db.String(100), primary_key=True, unique=True)
    prof_password = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    service_type = db.Column(db.String, nullable=False)
    experience = db.Column(db.String, nullable=False)
    date_created = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    pincode = db.Column(db.String)
    blocked = db.Column(db.Integer, default=0)
    approved = db.Column(db.Integer, default=0)
    rating = db.Column(db.Numeric(1, 1), default=0)
    sev_num_rating = db.Column(db.Integer, default=0)
    sev_total_rating = db.Column(db.Numeric, default=0)
    
    # Establishing relationship with Sevrequest
    prof_req = db.relationship('Sevrequest', backref='professional', cascade='all, delete-orphan')

class Customer(db.Model):
    __tablename__ = "customer"
    cust_email = db.Column(db.String(100), primary_key=True, unique=True)
    cust_password = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    pincode = db.Column(db.String, nullable=False)
    blocked = db.Column(db.Integer, default=0)
    
    # Establishing relationship with Sevrequest
    cust_req = db.relationship('Sevrequest', backref='customer', cascade='all, delete-orphan')

class Service(db.Model):
    __tablename__ = "service"
    sev_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sev_name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    time_req = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    address = db.Column(db.String)

    # Establishing relationship with Sevrequest
    sev_req = db.relationship("Sevrequest", backref='service', cascade='all, delete-orphan')

class Sevrequest(db.Model):
    __tablename__ = "sevrequest"
    sevreq_id = db.Column(db.Integer, primary_key=True, nullable=False)
    cust_email = db.Column(db.String, db.ForeignKey("customer.cust_email"), nullable=False)
    prof_email = db.Column(db.String, db.ForeignKey("professional.prof_email"), nullable=False)  # Corrected this line
    sev_id = db.Column(db.Integer, db.ForeignKey("service.sev_id"), nullable=False)
    date_of_request = db.Column(db.String, nullable=False)
    date_of_completion = db.Column(db.String, nullable=False)
    remarks = db.Column(db.String)
    sev_status = db.Column(db.String, nullable=False, default="requested")  # closed, requested, accepted(assigned), rejected

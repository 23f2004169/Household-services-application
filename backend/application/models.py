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
    image = db.Column(db.String)
    file=db.Column(db.String)
    phone=db.Column(db.String)
    blocked = db.Column(db.Integer, default=0)
    approval = db.Column(db.String, default='pending')
    rating=db.Column(db.Numeric(1,1), default=0)
    # Establishing relationship with Sevrequest
    prof_req = db.relationship('Sevrequest', backref='professional', cascade='all, delete-orphan')
    def to_json(self):
        return {
            "prof_email": self.prof_email,
            "prof_password": self.prof_password,
            "description": self.description,
            "service_type": self.service_type,
            "experience": self.experience,
            "date_created": self.date_created,
            "address": self.address,
            "pincode": self.pincode,
            "blocked": self.blocked,
            "approval": self.approval,
            "phone": self.phone,
            "rating": self.rating
        }
    
class Customer(db.Model):
    __tablename__ = "customer"
    cust_email = db.Column(db.String(100), primary_key=True, unique=True)
    cust_password = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    pincode = db.Column(db.String, nullable=False)
    blocked = db.Column(db.Integer, default=0)
    phone=db.Column(db.String)
    cust_req = db.relationship('Sevrequest', backref='customer', cascade='all, delete-orphan')
    def to_json(self):
        return {
            "cust_email": self.cust_email,
            "cust_password": self.cust_password,
            "address": self.address,
            "pincode": self.pincode,
            "blocked": self.blocked,
            "phone": self.phone
        }

class Service(db.Model):
    __tablename__ = "service"
    sev_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sev_name = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    time_req = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    pincode = db.Column(db.String)
    #Establishing relationship with Sevrequest
    sev_req = db.relationship("Sevrequest", backref='service', cascade='all, delete-orphan')
    def to_json(self):
        return {
            "sev_id": self.sev_id,
            "sev_name": self.sev_name,
            "price": self.price,
            "time_req": self.time_req,
            "description": self.description,
            "category": self.category,
            "address": self.address,
            "pincode": self.pincode
        }
    
class Sevrequest(db.Model):
    __tablename__ = "sevrequest"
    sevreq_id = db.Column(db.Integer, primary_key=True, nullable=False)
    cust_email = db.Column(db.String, db.ForeignKey("customer.cust_email"), nullable=False)
    prof_email = db.Column(db.String, db.ForeignKey("professional.prof_email"), nullable=False) 
    sev_id = db.Column(db.Integer, db.ForeignKey("service.sev_id"), nullable=False)
    date_of_request = db.Column(db.String, nullable=False) 
    date_of_completion = db.Column(db.String, nullable=False)
    remarks = db.Column(db.String)
    sev_status = db.Column(db.String, nullable=False, default="requested")  # closed, requested, accepted(assigned), rejected
    rating = db.Column(db.Numeric(1, 1), default=0)
    def to_json(self):
        return {
            "sevreq_id": self.sevreq_id,
            "cust_email": self.cust_email,
            "prof_email": self.prof_email,
            "sev_id": self.sev_id,
            "date_of_request": self.date_of_request,
            "date_of_completion": self.date_of_completion,
            "remarks": self.remarks,
            "sev_status": self.sev_status,
            "rating": self.rating,
        }
    
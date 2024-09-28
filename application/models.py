from application.database import db

class Admin(db.Model):
    __tablename__="admin"
    admin_id=db.Column(db.String,primary_key=True)
    admin_password=db.Column(db.String,nullable=False)

class Professional(db.Model):
    __tablename__="professional"
    prof_id=db.Column(db.String,primary_key=True,nullable=False)
    prof_name=db.Column(db.String)
    prof_password=db.Column(db.String,nullable=False)
    description=db.Column(db.String,nullable=False)
    service_type=db.Column(db.String,nullable=False)
    experience=db.Column(db.String,nullable=False)
    date_created=db.Column(db.String,nullable=False)
    blocked=db.Column(db.Integer, default=0)
    prof_req=db.relationship('Sevrequest',cascade='all, delete-orphan')
    def to_json(self):
        return{"prof_id":self.prof_id,"prof_name":self.prof_name,"prof_password":self.prof_password,"description":self.description,"service_type":self.service_type,"experience":self.experience,"blocked":self.blocked,"date_create":self.date_create,"prof_req":[req.to_json() for req in self.prof_req]}

class Customer(db.Model):
    __tablename__="customer"
    cust_id=db.Column(db.String,primary_key=True,nullable=False)
    cust_name=db.Column(db.String,nullable=False)
    cust_password=db.Column(db.String,nullable=False)
    address=db.Column(db.String,nullable=False)
    pincode=db.Column(db.String,nullable=False)
    blocked=db.Column(db.Integer, default=0)
    cust_req=db.relationship('Sevrequest',cascade='all, delete-orphan')
    def to_json(self):
        return{"cust_id":self.cust_id,"cust_name":self.cust_name,"cust_password":self.cust_password,"address":self.address,"pincode":self.pincode,"blocked":self.blocked,"cust_req":[req.to_json() for req in self.cust_req]}

class Sevrequest(db.Model):
    __tablename__="sevrequest"
    sevreq_id=db.Column(db.Integer,primary_key=True,nullable=False)
    prof_id=db.Column(db.String,db.ForeignKey("professional.prof_id"),nullable=False)
    cust_id=db.Column(db.Integer,db.ForeignKey("customer.cust_id"),nullable=False)
    sev_id=db.Column(db.Integer,db.ForeignKey("service.sev_id"),nullable=False)
    date_of_request=db.Column(db.String,nullable=False)
    date_of_completion=db.Column(db.String,nullable=False)
    remarks=db.Column(db.String)
    sev_status=db.Column(db.String,nullable=False,default="pending")
    rating=db.Column(db.Numeric(1,1),default=0)
    sev_num_rating=db.Column(db.Integer, default=0)
    sev_total_rating=db.Column(db.Numeric, default=0)
    def to_json(self):
        return{"sevreq_id":self.sevreq_id,"prof_id":self.prof_id,"cust_id":self.cust_id,"sev_id":self.sev_id,"date_of_request":self.date_of_request,"date_of_completion":self.date_of_completion,"remarks":self.remarks,"sev_status":self.sev_status,"rating":self.rating,"sev_num_rating":self.sev_num_rating,"sev_total_rating":self.sev_total_rating}
    
class Service(db.Model):
    __tablename__="service"
    sev_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    sev_name=db.Column(db.String,nullable=False)
    price=db.Column(db.Integer,nullable=False)
    time_req=db.Column(db.String,nullable=False)
    description=db.Column(db.String,nullable=False)
    sev_req=db.relationship("Sevrequest",cascade='all, delete-orphan')
    def to_json(self):
        return{"sev_id":self. sev_id,"sev_name":self.sev_name,"price":self.price,"time_req":self.time_req,"description":self.description,"sev_req":[req.to_json() for req in self.sev_req]}






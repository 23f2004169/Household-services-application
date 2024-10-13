from flask import current_app as app #alias for current running app
from flask import render_template,url_for,redirect,request
from application.models import *
from datetime import datetime,date
import decimal
#stats
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import numpy as np



@app.route("/")
def home():
    return render_template("index.html")

#------------------------------------------------------------------ADMIN-------------------------------------------------------------------------
#login
#home- sev(CRUD), +  prof(R),sevreqs(R) list click on then individual info
#search-sev,sevreq,cust,prof or text search(closed req)
#summary graphs
#prof(block/unblock,approve)  cust(block/unblock)

# admin_exist = Admin.query.filter_by(admin_email="irina@gmail.com").first()
# if admin_exist is None:
#     user= Admin(admin_email="irina@gmail.com", 
#                 admin_password=generate_password_hash("irina24"), admin_id="irina")
#     db.session.add(user)
#     db.session.commit()

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/admin_login",methods=["GET","POST"])
def admin_login():
    data = request.get_json()
    email = data.get("email", None)
    password = data.get("password", None)
    print(email, password)
    admin_from_db=Admin.query.filter_by(admin_email=email).first()
    if admin_from_db:
        if check_password_hash(admin_from_db.admin_password, password):
            access_token = create_access_token(identity=admin_from_db.admin_email)
            response = jsonify(msg="login successful")
            set_access_cookies(response, access_token)
            return response
        return jsonify(error="Authentication failed"), 401
    
    return jsonify(error="wrong credentials"), 404
#HOME
@app.route("/admin_dashboard",methods=["GET","POST"])
def admin_dashboard():
    global logged_admin
    if not logged_admin:
        return redirect(url_for("admin_login"))
    prof=Professional.query.all() 
    cust=Customer.query.all()
    req=Sevrequest.query.all()
    sev=Service.query.all()
    #save data in each table as a list of objects
    if request.method=="GET":
        return render_template("admin_dashboard.html",prof=prof,cust=cust,req=req,sev=sev)
    if request.method=="POST":
        current_date=date.today().strftime('%d-%m-%Y')
        return render_template("ongoing_req.html",current_date=current_date,req=req)
    
#view all info list in platform     
@app.route("/admin_all_prof",methods=["GET"])
def admin_all_prof():
    prof=Professional.query.all() 
    return render_template('all_prof.html',prof=prof)

@app.route("/admin_all_cust",methods=["GET"])
def admin_all_cust():
    cust=Customer.query.all() 
    return render_template('all_cust.html',cust=cust)

@app.route("/admin_all_sev",methods=["GET"])
def admin_all_sev():
    sev=Service.query.all()
    return render_template('all_prof.html',sev=sev)

@app.route("/admin_all_req",methods=["GET"])
def admin_all_req():
    req=Sevrequest.query.all() 
    return render_template('all_prof.html',req=req)

#block
@app.route("/customer/<cust_id>/block",methods=["GET","POST"])
def admin_block_cust(cust_id):
    i=Customer.query.get(cust_id)
    i.blocked= not i.blocked
    db.session.commit()
    return render_template('cust_details.html',cust=i)

@app.route("/professional/<prof_id>/block",methods=["GET","POST"])
def admin_block_prof(prof_id):
    i=Professional.query.get(prof_id)
    i.blocked= not i.blocked
    db.session.commit()
    return render_template('prof_details.html',prof=i)

#approve and review professional
@app.route("/professional/<prof_id>/approve",methods=["GET","POST"])
def admin_approve_prof(prof_id):
    i=Professional.query.get(prof_id)
    i.approved= not i.approved
    db.session.commit()
    return render_template('prof_details.html',prof=i)

#individual details
@app.route("/professional_info/<prof_id>",methods=["GET","POST"])
def admin_prof_details(prof_id):
    prof=Professional.query.get(prof_id)
    if request.method=="GET":
        return render_template("prof_details.html",prof=prof)

@app.route("/service_request_info/<sevreq_id>",methods=["GET","POST"])
def admin_sevreq_details(sevreq_id):
    req=Sevrequest.query.get(sevreq_id)
    if request.method=="GET":
        return render_template("sevreq_details.html",req=req)
    
@app.route("/service_info/<sevreq_id>",methods=["GET","POST"])
def admin_sev_details(sev_id):
    sev=Service.query.get(sev_id)
    if request.method=="GET":
        return render_template("sev_details.html",sev=sev)
    
@app.route("/customer_info/<cust_id>",methods=["GET","POST"])
def admin_cust_details(cust_id):
    cust=Customer.query.get(cust_id)
    if request.method=="GET":
        return render_template("cust_details.html",cust=cust)
    
#service management
@app.route("/create_sev",methods=["GET", "POST"])
def admin_create_sev():
    if request.method=="GET":
        return render_template("create_sev.html")
    if request.method=="POST":
        sev_name=request.form.get("sev_name")
        price=request.form.get("price")
        time_req=request.form.get("time_req")
        description=request.form.get("description")
        category=request.form.get("category")
        new_sev=Service(sev_name=sev_name,price=price,time_req=time_req,description=description,category=category)
        db.session.add(new_sev)
        db.session.commit()
        return redirect(url_for("admin_dashboard"))
       
@app.route("/delete_sev", methods=["GET", "POST"])
def admin_delete_sev():
    if request.method=="GET":
        services=Service.query.all()
        return render_template("delete_venue.html", services=services)
    if request.method=="POST":
        sev_id=request.form.get("sev_id")
        sev_to_delete=Service.query.get(sev_id)
        db.session.delete(sev_to_delete)
        db.session.commit()
        return redirect(url_for("admin_dashboard"))

@app.route("/update_sev", methods=["GET", "POST"])
def admin_update_sev():
    if request.method=="GET":
        services=Service.query.all()
        return render_template("update_sev.html",services=services)
    if request.method=="POST":
        sev_id=request.form.get("sev_id")
        sev_name=request.form.get("sev_name")
        price=request.form.get("price")
        time_req=request.form.get("time_req")
        description=request.form.get("description")
        category=request.form.get("category")
        # update new sev in db
        sev_to_update=Service.query.get(sev_id)
        sev_to_update.sev_name=sev_name
        sev_to_update.price=price
        sev_to_update.time_req=time_req
        sev_to_update.description=description
        sev_to_update.category=category
        db.session.commit()
        return redirect(url_for("admin_dashboard"))
    
#search
#implement drop down feature, all in one search, add multiple filters -all 4 by name or search text(closed requests)
@app.route("/admin_search",methods=["GET","POST"])
def admin_search():
    if request.method=="GET":
            return render_template("asearch.html")
    if request.method=="POST":
            sev_name=request.form.get("sev_name").strip()
            result=Service.query.filter(Service.sev_name.ilike(f"%{sev_name}%")).all()
            return render_template("aresult.html",result=result)

#statistics
@app.route("/admin_summary", methods=["GET"])
def admin_summary():
    # return a list of all the json objects of chart data for each venue
    profs=Professional.query.all() 
    custs=Customer.query.all()
    reqs=Sevrequest.query.all()
    sevs=Service.query.all()
    services_json=[sev.to_json() for sev in sevs]
    profs_json=[prof.to_json() for prof in profs]
    custs_json=[cust.to_json() for cust in custs]
    reqs_json=[req.to_json() for req in reqs]
    return render_template("summary.html", sevs=sevs,custs=custs,reqs=reqs,profs=profs,services_json=services_json,profs_json=profs_json,custs_json=custs_json,reqs_json=reqs_json)

#--------------------------------------------------------------PROFESSIONAL-----------------------------------------------------------------------
#register
#login
#home- todays services, closed services , view+edit profile
#search- Customers ,Requests by name,loc, pin , or by text- date
   #view all the service requests from all the customers
   #accept/reject a particular service request
   #close the service request once completed*
#summary graphs 

@app.route('/prof_reg', methods=['GET','POST'])
def prof_reg():
    if request.method=="GET":
        return render_template("prof_reg.html")
    if request.method=="POST":
        prof_id =request.form.get("prof_id")
        prof_name=request.form.get("prof_name")
        prof_password=request.form.get("prof_password")
        service_type=request.form.get("service_type")
        experience=request.form.get("experience")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        description=request.form.get("description")
        date_created=datetime.now().date()
        try:
            exist=Professional.query.filter_by(prof_id=prof_id).first()
            if exist:
                return render_template("prof_reg.html",message="Professional username already exists")
            else:
                new_prof=Professional(prof_id=prof_id,prof_name=prof_name,prof_password=prof_password, service_type=service_type,experience=experience, address= address, pincode= pincode,description=description,date_created=date_created)
                db.session.add(new_prof)
                db.session.commit()
                return redirect(url_for("prof_dashboard",prof_id=prof_id))
        except:
            return "some error"
    return render_template("prof_reg.html")
    
@app.route("/prof_login",methods=["GET","POST"])
def prof_login():
    if request.method=="GET":
        return render_template("prof_reg.html")
    if request.method=="POST":
        prof_id=request.form.get("prof_id")
        prof_password=request.form.get("prof_password")
        try:
            prof_from_db=Professional.query.get(prof_id)
            if prof_from_db:
                password_from_db=prof_from_db.prof_password
                if password_from_db==prof_password:
                    return redirect(url_for("prof_dashboard",prof_id=prof_id))
                else:
                    return render_template("prof_login.html",message="Password failed")
            else:
                return render_template("prof_login.html",message="Id failed")

        except:
            return "some error"
    return render_template("prof_login.html")

#HOME 

@app.route("/prof_dashboard/<prof_id>",methods=["GET","POST"])  
def prof_dashboard(prof_id):
    prof=Professional.query.get(prof_id)  
    sevs=Service.query.all()
    reqs=Sevrequest.query.all()
    if request.method=="GET":
        return render_template("prof_dashboard.html",prof=prof,sevs=sevs,reqs=reqs)
    
@app.route("/prof_sevs_today/<prof_id>",methods=["GET"])
def prof_sevs_today(prof_id):
    prof=Professional.query.get(prof_id)
    sevreqs=Sevrequest.query.all()
    reqstoday=[]
    for i in sevreqs:
        current_date=datetime.now().date()
        if i.date_of_request==current_date:
            reqstoday.append(i)
    return render_template('sevs_today.html',sevstoday=reqstoday,prof=prof)

#close if completed
@app.route("/prof_closed_sevs/<prof_id>",methods=["GET"])
def prof_closed_sevs(prof_id):
    prof=Professional.query.get(prof_id)
    sevreqs=Sevrequest.query.all()
    closedreqs=[]
    for i in sevreqs:
        if i.sev_status=='closed':
            closedreqs.append(i)
    return render_template('sevs_today.html',sevsclosed=closedreqs,prof=prof)


#view profile details on dashboard
@app.route("/prof_update/<prof_id>",methods=["GET", "POST"])
def prof_update(prof_id):
    if request.method=="GET":
        prof=Professional.query.get(prof_id)
        return render_template("update_prof.html",prof=prof)
    if request.method=="POST":
        prof_name=request.form.get("prof_name")
        prof_password=request.form.get("prof_password")
        service_type=request.form.get("service_type")
        experience=request.form.get("experience")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        description=request.form.get("description")
        update_prof=Professional.query.get(prof_id)
        update_prof.prof_name=prof_name     
        update_prof.prof_password=prof_password
        update_prof.service_type=service_type
        update_prof.experience=experience
        update_prof.address=address
        update_prof.pincode=pincode
        update_prof.description=description
        db.session.commit()
        return redirect(url_for("prof_dashboard",prof_id=prof_id))
    
#SEARCH cust+sevrequest
@app.route("/prof_search/<prof_id>",methods=["GET","POST"])
def prof_search(prof_id):
    prof=Professional.query.get(prof_id)
    if request.method=="GET":
            return render_template("psearch.html",prof=prof)
    if request.method=="POST":
            sevreq_name=request.form.get("sevreq_name").strip()
            result=Sevrequest.query.filter(Sevrequest.sevreq_name.ilike(f"%{sevreq_name}%")).all()
            return render_template("presult.html",result=result,prof=prof)
    
#from search results click on id of sevrequest for details
@app.route("/sevreq_details/<int:sevreq_id>/<prof_id>",methods=["GET"])
def prof_sevreq_details(sevreq_id,prof_id):
    prof=Professional.query.get(prof_id)
    sevreq=Sevrequest.query.get(sevreq_id)
    if request.method=="GET":
        return render_template("prof_req_details.html",sevreq=sevreq,prof=prof)
    
#dealing with service requests
@app.route('/accept_sevreq/<sevreq_id>/<prof_id>',methods=['GET','POST'])
def prof_reqaccept(sevreq_id,prof_id):
    newlist=[]
    prof=Professional.query.get(prof_id)
    req=Sevrequest.query.get(sevreq_id)
    req.sev_status="accepted"
    db.session.commit()
    return render_template("prof_req_details.html",prof=prof,sevreq=newlist)

@app.route('/reject_sevreq/<sevreq_id>/<prof_id>',methods=['GET','POST'])
def prof_reqreject(sevreq_id,prof_id):
    newlist=[]
    prof=Professional.query.get(prof_id)
    req=Sevrequest.query.get(sevreq_id)
    req.sev_status="rejected"
    db.session.commit()
    return render_template("prof_req_details.html",prof=prof,sevreq=newlist)

@app.route('/close_sevreq/<sevreq_id>/<prof_id>',methods=['GET','POST'])
def prof_reqclose(sevreq_id,prof_id):
    newlist=[]
    prof=Professional.query.get(prof_id)
    req=Sevrequest.query.get(sevreq_id)
    req.sev_status="closed"
    db.session.commit()
    return render_template("prof_req_details.html",prof=prof,sevreq=newlist)

#statistics
@app.route("/prof_summary", methods=["GET"])
def prof_summary():
    # return a list of all the json objects of chart data for each venue
    profs=Professional.query.all() 
    custs=Customer.query.all()
    reqs=Sevrequest.query.all()
    sevs=Service.query.all()
    services_json=[sev.to_json() for sev in sevs]
    profs_json=[prof.to_json() for prof in profs]
    custs_json=[cust.to_json() for cust in custs]
    reqs_json=[req.to_json() for req in reqs]
    return render_template("prof_summary.html", sevs=sevs,custs=custs,reqs=reqs,profs=profs,services_json=services_json,profs_json=profs_json,custs_json=custs_json,reqs_json=reqs_json)

#--------------------------------------------------------------CUSTOMER-----------------------------------------------------------------------
#register
#login
#home- Card for each category, service req HISTORY all, view+edit profile
      #Card category service- go to avail services/cleaning packages then BOOK - then create service request
#Create a new service request based on the services available
  #Edit an existing service request - e.g. date_of_request, completion status, remarks etc
   #Close an existing service request.
#rate servicereq after closing sevrequest
#search - Services based on their location, name, pin code etc. OR text- category
#summary graphs 

@app.route('/cust_reg', methods=['GET','POST'])
def cust_reg():
    if request.method=="GET":
        return render_template("cust_reg.html")
    if request.method=="POST":
        cust_id =request.form.get("cust_id")
        cust_name=request.form.get("cust_name")
        cust_password=request.form.get("cust_password")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        try:
            exist=Customer.query.filter_by(cust_id=cust_id).first()
            if exist:
                return render_template("cust_reg.html",message="Customer username already exists")
            else:
                new_cust=Customer(cust_id=cust_id,cust_name=cust_name,cust_password=cust_password,address= address, pincode= pincode)
                db.session.add(new_cust)
                db.session.commit()
                return redirect(url_for("cust_dashboard",cust_id=cust_id))
        except:
            return "some error"
    return render_template("cust_reg.html")
    
@app.route("/cust_login",methods=["GET","POST"])
def cust_login():
    if request.method=="GET":
        return render_template("cust_reg.html")
    if request.method=="POST":
        cust_id=request.form.get("cust_id")
        cust_password=request.form.get("cust_password")
        try:
            cust_from_db=Customer.query.get(cust_id)
            if cust_from_db:
                password_from_db=cust_from_db.cust_password
                if password_from_db==cust_password:
                    return redirect(url_for("cust_dashboard",cust_id=cust_id))
                else:
                    return render_template("cust_login.html",message="Password failed")
            else:
                return render_template("cust_login.html",message="Id failed")

        except:
            return "some error"
    return render_template("cust_login.html")

#HOME 

@app.route("/cust_dashboard/<prof_id>",methods=["GET","POST"])  
def cust_dashboard(cust_id):
    cust=Customer.query.get(cust_id)  
    sevs=Service.query.all()
    reqs=Sevrequest.query.all()
    if request.method=="GET":
        return render_template("prof_dashboard.html",cust=cust,sevs=sevs,reqs=reqs)
    
#CREATE CARDS FOR EACH CATEGORY FIRST 
#send categ value then view all services under that categ
@app.route("/cust_sev/<cust_id>/categ",methods=["GET"])
def cust_sev(cust_id,categ):
    sev=Service.query.all()
    cust=Customer.query.get(cust_id)
    sevlist=[]
    for i in sev:
        if i.category==categ:
            sevlist.append(i)
    return render_template('cust_sev.html',sev=sevlist,cust=cust)

#list of all sev requests by the customer
@app.route("/cust_req/<cust_id>",methods=["GET"])
def cust_req(cust_id):
    req=Sevrequest.query.all()
    cust=Customer.query.get(cust_id)
    reqlist=[]
    for i in cust.cust_req:
        reqlist.append(i)
    return render_template('cust_sev.html',reqs=reqlist,cust=cust)

#view details of a sev req
@app.route("/cust_sevreq_details/<cust_id>/<sevreq_id>",methods=["GET","POST"])
def cust_sevreq_details(cust_id,sevreq_id):
    sevreq=Sevrequest.query.get(sevreq_id)
    return render_template('cust_sevreq_details',sevreq=sevreq,cust_id=cust_id)

# Requests--create , edit, close
@app.route("/cust_create_sevreq/<cust_id>",methods=["GET", "POST"])
def cust_create_sevreq(cust_id):
    if request.method=="GET":
        return render_template("create_sevreq.html")
    if request.method=="POST":
        prof_id=request.form.get("prof_id") #dropdown
        sev_id=request.form.get("sev_id")   #insert var
        date_of_request=request.form.get("date_of_request")
        date_of_completion=request.form.get("date_of_completion")
        remarks=request.form.get("remarks")
        new_sevreq=Sevrequest(cust_id=cust_id,prof_id=prof_id,sev_id=sev_id,date_of_request=date_of_request,date_of_completion=date_of_completion,remarks=remarks,rating=rating)
        db.session.add(new_sevreq)
        db.session.commit()
        return redirect(url_for("cust_sevreq_details"),cust_id=cust_id,sevreq_id=sevreq_id)

@app.route("/cust_update_sevreq/<cust_id>/<sevreq_id>", methods=["GET", "POST"])
def cust_update_sevreq(cust_id,sevreq_id):
    if request.method=="GET":
        sevreqs=Service.query.all()
        return render_template("update_sevreq.html",sevreqs=sevreqs)
    if request.method=="POST":
        cust_id=cust_id
        prof_id=request.form.get("prof_id")
        sev_id=request.form.get("sev_id")
        date_of_request=request.form.get("date_of_request")
        date_of_completion=request.form.get("date_of_completion")
        remarks=request.form.get("remarks")
        # update new sev in db
        sev_to_update=Sevrequest.query.get(sevreq_id)
        sev_to_update.cust_id=cust_id
        sev_to_update.prof_id=prof_id
        sev_to_update.sev_id=sev_id
        sev_to_update.date_of_request=date_of_request
        sev_to_update.date_of_completion=date_of_completion
        sev_to_update.remarks=remarks
        db.session.commit()
        return redirect(url_for("cust_sevreq_details"),cust_id=cust_id,sevreq_id=sevreq_id)
    
#close service request
@app.route("/cust_close_sevreq/<cust_id>/<sevreq_id>",methods=["GET"])
def cust_close_sevreq(cust_id,sevreq_id):
    sevreq=Sevrequest.query.get(sevreq_id)
    sevreq.sev_status='closed'
    return redirect(url_for("cust_sevreq_details"),cust_id=cust_id,sevreq_id=sevreq_id)

#rate sevreq after closing req
@app.route("/cust_rate_sev/<cust_id>/<sevreq_id>",methods=["GET"])
def cust_rate_sev(cust_id,sevreq_id):
    sevreq=Sevrequest.query.get(sevreq_id)
    sev_id=sevreq.sev_id
    sev=Service.query.get(sev_id)
    if request.method=="GET":
        return render_template("rate.html",cust_id=cust_id,sevreq_id=sevreq_id)
    if request.method=="POST":
        if sevreq.sev_status=='closed':
            sev.sev_total_rating+=decimal.Decimal(request.form.get("rating"))
            sev.sev_num_rating+=1
            sev.rating=((sev.sev_total_rating)/sev.sev_num_rating)
            db.session.commit()
        else:
            return render_template("cust_dashboard.html",message="Close the Service request to rate")

        return redirect(url_for("cust_dashboard",cust_id=cust_id,sevreq_id=sevreq_id))

#SEARCH service
@app.route("/cust_search/<cust_id>",methods=["GET","POST"])
def cust_search(cust_id):
    cust=Customer.query.get(cust_id)
    if request.method=="GET":
            return render_template("cust_search.html",cust=cust)
    if request.method=="POST":
            sev_name=request.form.get("sev_name").strip()
            result=Service.query.filter(Service.sev_name.ilike(f"%{sev_name}%")).all()
            return render_template("presult.html",result=result,cust=cust)
    
#statistics
@app.route("/cust_summary", methods=["GET"])
def cust_summary():
    # return a list of all the json objects of chart data for each venue
    profs=Professional.query.all() 
    custs=Customer.query.all()
    reqs=Sevrequest.query.all()
    sevs=Service.query.all()
    services_json=[sev.to_json() for sev in sevs]
    profs_json=[prof.to_json() for prof in profs]
    custs_json=[cust.to_json() for cust in custs]
    reqs_json=[req.to_json() for req in reqs]
    return render_template("cust_summary.html", sevs=sevs,custs=custs,reqs=reqs,profs=profs,services_json=services_json,profs_json=profs_json,custs_json=custs_json,reqs_json=reqs_json)
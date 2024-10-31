from flask import current_app as app #alias for current running app
from flask import render_template,url_for,redirect,request
from application.models import *
from datetime import datetime,date
import decimal
from flask import Flask
from flask import jsonify
from flask import request
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required, set_access_cookies
from datetime import timedelta

@app.route("/")
def home():
    return render_template("index.html")

#------------------------------------------------------------------ADMIN-------------------------------------------------------------------------
#login
#home- sev(CRUD), +  prof(R),sevreqs(R) list click on then individual info
#search-sev,sevreq,cust,prof or text search(closed req)
#summary graphs
#prof(block/unblock,approve)  cust(block/unblock)


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/api/login",methods=['GET','POST'])
def login():
    data = request.get_json()
    email = data.get("email", None)
    password = data.get("password", None)
    role=data.get("role",None)
    print(email, password,role)
    if role=="admin":
        admin_exist = Admin.query.filter_by(admin_email="irina@gmail.com").first()
        print(admin_exist)
        if not admin_exist:
            user= Admin(admin_email="irina@gmail.com", 
            admin_password=generate_password_hash("irina24"))
            db.session.add(user)
            db.session.commit()
        admin_from_db=Admin.query.filter_by(admin_email=email).first()
        if admin_from_db:
            if check_password_hash(admin_from_db.admin_password, password):
                access_token = create_access_token(identity=admin_from_db.admin_email)
                response = jsonify(msg="login successful")
                set_access_cookies(response, access_token)
                return response  
        return jsonify(error="Authentication failed"), 401  
    if role=="prof":
        prof_from_db=Professional.query.filter_by(prof_email=email).first() 
        print('received',prof_from_db)
        if prof_from_db:
            if check_password_hash(prof_from_db.prof_password, password):            
                access_token = create_access_token(identity=prof_from_db.prof_email)
                response = jsonify(msg="login successful",email=prof_from_db.prof_email)
                set_access_cookies(response, access_token)
                return response                                 
        return jsonify(error="Authentication failed"), 401
    if role=="cust":
        cust_from_db=Customer.query.filter_by(cust_email=email).first() 
        print('received',cust_from_db)
        if cust_from_db:
            if check_password_hash(cust_from_db.cust_password, password):            
                access_token = create_access_token(identity=cust_from_db.cust_email)
                response = jsonify(msg="login successful",email=cust_from_db.cust_email)
                set_access_cookies(response, access_token)
                return response                                 
        return jsonify(error="Authentication failed"), 401
    return jsonify(error="wrong credentials"), 404

@app.route("/api/cust_reg", methods=['POST'])
def cust_reg():
    if request.method == "POST":
        data = request.get_json()
        cust_email = data.get("cust_email")
        cust_password = data.get("cust_password")
        address = data.get("address")
        pincode = data.get("pincode")
        # try:
            # Check if customer email already exists
        if not cust_password or cust_password.strip() == "":
            return jsonify({"error":"Password cannot be empty"}), 400
        
        exist = Customer.query.filter_by(cust_email=cust_email).first()
        if exist:
            return jsonify({"error":"Customer username already exists"}), 400  # Bad Request
        print(cust_password)
        
        # Create a new customer
        print(generate_password_hash(cust_password), "sachin") # Hash the password
        new_cust = Customer(
            cust_email=cust_email,
            cust_password=generate_password_hash(cust_password),
            address=address,
            pincode=pincode
        )
        db.session.add(new_cust)
        db.session.commit()

        # Return a success message along with the customer email
        return jsonify({"msg":"Registration successful", "cust_email":"cust_email"}), 201  # Created

        # except Exception as e:
        # print(str(e))  # Log the error for debugging
    return jsonify({"error":"An error occurred during registration"}), 500  # Internal Server Error

@app.route('/api/prof_reg', methods=['GET','POST'])
def prof_reg():
    if request.method=="POST":
        data = request.get_json()
        prof_email =data.get("prof_email")
        prof_password=data.get("prof_password")
        service_type=data.get("service_type")
        experience=data.get("experience")
        address=data.get("address")
        pincode=data.get("pincode")
        description=data.get("description")
        date_created=datetime.now().date()
        if not prof_password or prof_password.strip() == "":
            return jsonify({"error":"Password cannot be empty"}), 400
        
        exist = Professional.query.filter_by(prof_email=prof_email).first()
        if exist:
            print('hello2')
            return jsonify({"error":"Professional username already exists"}), 400  # Bad Request
        
        # Create a new customer
        print(generate_password_hash(prof_password)) # Hash the password
        new_prof =Professional(
            prof_email=prof_email,
            prof_password=generate_password_hash(prof_password),
            service_type=service_type,
            experience=experience,
            address=address,
            pincode=pincode,
            description=description,
            date_created=date_created
        )
        db.session.add(new_prof)
        db.session.commit()

        # Return a success message along with the customer email
        return jsonify({"msg":"Registration successful", "prof_email":"prof_email"}), 201  

#===================================ADMIN======================================================================================   
@app.route('/api/services', methods=['GET','POST'])
def get_services():
    try:
        category = request.args.get('category')
        if category:
            services = Service.query.filter_by(category=category).all()
        else:
            services = Service.query.all()
        services_list = [
            {
                'sev_id': service.sev_id,
                'sev_name': service.sev_name,
                'description': service.description,
                'price': service.price,
                'time_req': service.time_req,
                'address': service.address,
                'category': service.category,
                'pincode' : service.pincode
            } for service in services
        ]
        print(services_list)
        return jsonify(services_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route("/api/professionals", methods=["GET"])
def get_professionals():
    try:
        professionals = Professional.query.all()
        # Prepare a list of professionals in JSON format
        professionals_list = [
            {
                'prof_email': professional.prof_email,
                'description': professional.description,
                'service_type': professional.service_type,
                'experience': professional.experience,
                'date_created': professional.date_created,
                'address': professional.address,
                'pincode': professional.pincode,
                'blocked': professional.blocked,
                'approval': professional.approval
            } for professional in professionals
        ]
        # Return the list of professionals as a JSON response
        return jsonify(professionals_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/service_requests", methods=["GET"])
def get_service_requests():
    try:
        cust= request.args.get('email')
        if cust:    
            service_requests = Sevrequest.query.filter_by(cust_email=cust).all()
        else:
            service_requests = Sevrequest.query.all()
        # Prepare a list of service requests in JSON format
        service_requests_list = [
            {
                'sevreq_id': service_request.sevreq_id,
                'prof_email': service_request.prof_email,
                'cust_email': service_request.cust_email,
                'sev_id': service_request.sev_id,
                'date_of_request': service_request.date_of_request,
                'date_of_completion': service_request.date_of_completion,
                'remarks': service_request.remarks,
                'sev_status': service_request.sev_status,
                'rating': service_request.rating,
                'sev_num_rating': service_request.sev_num_rating,
                'sev_total_rating': service_request.sev_total_rating
            } for service_request in service_requests
        ]
        return jsonify(service_requests_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route("/api/customer", methods=["GET"])
def get_customers():
    try:
        customers = Customer.query.all()
        # Prepare a list of customers in JSON format
        customers_list = [
            {
                'cust_email': customer.cust_email,
                'address': customer.address,
                'pincode': customer.pincode
            } for customer in customers
        ]
        # Return the list of customers as a JSON response
        return jsonify(customers_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/create_sev", methods=["POST"])
def admin_create_sev():
    if request.method == "POST":
        # Get the data from the request body as JSON
        data = request.get_json()
        print(data)
        if data:
            # Check if the service with the same name already exists
            existing_service = Service.query.filter_by(sev_name=data['sev_name']).first()
            print(existing_service)
            if not existing_service:
                # Extract values from the JSON payload
                sev_name = data.get("sev_name")
                price = data.get("price")
                time_req = data.get("time_req")
                description = data.get("description")
                category = data.get("category")
                address=data.get("address")
                pincode = data.get("pincode") 
                # Create a new Service object
                new_sev = Service(
                    sev_name=sev_name,
                    price=price,
                    time_req=time_req,
                    description=description,
                    category=category,
                    address=address,
                    pincode=pincode
                )
                db.session.add(new_sev)
                db.session.commit()
                # Return a success message with the new service details
                return jsonify({
                    "message": "Service created successfully",
                    "service": {
                        "sev_id": new_sev.sev_id,
                        "sev_name": new_sev.sev_name,
                        "price": new_sev.price,
                        "time_req": new_sev.time_req,
                        "description": new_sev.description,
                        "category": new_sev.category,
                        "address":new_sev.address,
                        "pincode":new_sev.pincode,
                    }
                }), 201 
            

            else:
                return jsonify({"error": "Service with this name already exists"}), 409  
        else:
            return jsonify({"error": "Invalid data"}), 400 

@app.route("/api/edit_sev/<int:sev_id>", methods=["GET", "POST"])
def admin_update_sev(sev_id):
    if request.method == "GET":
        service = Service.query.filter_by(sev_id=sev_id).first()
        if service:
            service_data = {
                "sev_name": service.sev_name,
                "price": service.price,
                "time_req": service.time_req,
                "description": service.description,
                "category": service.category,
                "address": service.address,
                "pincode": service.pincode
            }
            return jsonify(service_data), 200
        else:
            return jsonify({"error": "Service not found"}), 404
    if request.method == "POST":
        try:
            data = request.json
            sev_to_update = Service.query.get(sev_id)
            if sev_to_update:
                sev_to_update.sev_name = data.get("sev_name", sev_to_update.sev_name)
                sev_to_update.price = data.get("price", sev_to_update.price)
                sev_to_update.time_req = data.get("time_req", sev_to_update.time_req)
                sev_to_update.description = data.get("description", sev_to_update.description)
                sev_to_update.category = data.get("category", sev_to_update.category)
                sev_to_update.address = data.get("address", sev_to_update.address)
                sev_to_update.pincode = data.get("pincode", sev_to_update.pincode)  
                db.session.commit()
                # Convert the updated service object to a dictionary for JSON serialization
                updated_service_data = {
                    "sev_name": sev_to_update.sev_name,
                    "price": sev_to_update.price,
                    "time_req": sev_to_update.time_req,
                    "description": sev_to_update.description,
                    "category": sev_to_update.category,
                    "address": sev_to_update.address,
                    "pincode": sev_to_update.pincode
                }
                
                return jsonify({"message": "Service updated successfully", "service": updated_service_data}), 200
            else:
                return jsonify({"error": "Service not found"}), 404
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            return jsonify({"error": str(e)}), 500

@app.route("/api/delete_sev/<int:sev_id>", methods=["DELETE"])
def admin_delete_sev(sev_id):
    try:
        # Fetch the service to delete by sev_id
        sev_to_delete = Service.query.get(sev_id)
        if not sev_to_delete:
            return jsonify({"error": "Service not found"}), 404
        
        # Delete the service
        db.session.delete(sev_to_delete)
        db.session.commit()

        return jsonify({"message": "Service deleted successfully"}), 200
    
    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return jsonify({"error": str(e)}), 500

@app.route("/api/professional/approve/<prof_email>", methods=["POST"])
def admin_approve_prof(prof_email):
    professionals = Professional.query.get(prof_email)
    if professionals is None:
        return {"error": "Professional not found"}, 404
    professionals.approval ="approved"
    db.session.commit()
    return jsonify({"message": "Professional approval status updated successfully"}), 200
@app.route("/api/professional/reject/<prof_email>", methods=["POST"])
def admin_reject_prof(prof_email):
    professionals = Professional.query.get(prof_email)
    if professionals is None:
        return {"error": "Professional not found"}, 404
    professionals.approval ="rejected"
    db.session.commit()
    return jsonify({"message": "Professional approval status updated successfully"}), 200
@app.route("/api/professional/block/<prof_email>", methods=["POST"])
def admin_block_prof(prof_email):
    professionals = Professional.query.get(prof_email)
    if professionals is None:
        return {"error": "Professional not found"}, 404
    professionals.blocked = not professionals.blocked
    db.session.commit()
    return jsonify({"message": "Professional approval status updated successfully"}), 200


@app.route("/api/admin_summary", methods=["GET"])
def api_admin_summary():
    profs = Professional.query.all()
    custs = Customer.query.all()
    reqs = Sevrequest.query.all()
    sevs = Service.query.all()
    services_json = [sev.to_json() for sev in sevs]
    profs_json = [prof.to_json() for prof in profs]
    custs_json = [cust.to_json() for cust in custs]
    reqs_json = [req.to_json() for req in reqs]
    return jsonify({
        "services": services_json,
        "professionals": profs_json,
        "customers": custs_json,
        "requests": reqs_json
    })

#=========================================CUSTOMER=================================================================================

@app.route('/api/create_sevrequest/<cust_email>', methods=['POST'])
def create_service_request(cust_email):
    try:
        data = request.get_json()
        prof_email = data.get("prof_email")
        sev_id = data.get("sev_id")
        date_of_request = data.get("date_of_request")
        date_of_completion = data.get("date_of_completion")
        # Create a new service request
        new_request = Sevrequest(
            cust_email=cust_email,
            prof_email=prof_email,
            sev_id=sev_id,
            date_of_request=date_of_request,
            date_of_completion=date_of_completion,)
        db.session.add(new_request)
        db.session.commit()
        # Return a JSON response
        return jsonify({
            "status": "success",
            "message": "Service request created successfully",
            "new_request":{ "sevreq_id": new_request.sevreq_id,
           "cust_email": new_request.cust_email,
           "prof_email": new_request.prof_email,
           "sev_id": new_request.sev_id,
           "date_of_request": new_request.date_of_request,
           "date_of_completion": new_request.date_of_completion,
                  }}), 201
    except Exception as e:
        # Handle exceptions and return an error response
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
    
@app.route("/api/edit_sevreq/<int:sevreq_id>/<cust_email>", methods=["GET", "POST"])
def update_service_request(sevreq_id,cust_email):
    if request.method == "GET":
        service_request= Sevrequest.query.filter_by(sevreq_id=sevreq_id).first()
        if service_request:
            service_data = {
                "sevreq_id": service_request.sevreq_id,
                "prof_email": service_request.prof_email,
                "date_of_request": service_request.date_of_request,
                "date_of_completion": service_request.date_of_completion,
                "sev_status": service_request.sev_status,
                "remarks": service_request.remarks
            }
            
            return jsonify(service_data), 200
        else:
            return jsonify({"error": "Service not found"}), 404
    if request.method == "POST":
        try:
            data = request.json
            sev_to_update = Sevrequest.query.get(sevreq_id)
            if sev_to_update:
                sev_to_update.prof_email = data.get("prof_email", sev_to_update.prof_email) 
                sev_to_update.date_of_request = data.get("date_of_request", sev_to_update.date_of_request)
                sev_to_update.date_of_completion = data.get("date_of_completion", sev_to_update.date_of_completion)
                sev_to_update.sev_status = data.get("sev_status", sev_to_update.sev_status)
                sev_to_update.remarks = data.get("remarks", sev_to_update.remarks)
                db.session.commit()
                # Convert the updated service object to a dictionary for JSON serialization
                updated_service_data = {
                    "prof_email": sev_to_update.prof_email,
                    "cust_email": cust_email,
                    "date_of_request": sev_to_update.date_of_request,
                    "date_of_completion": sev_to_update.date_of_completion,
                    "sev_status": sev_to_update.sev_status,
                    "remarks": sev_to_update.remarks
                }
                
                return jsonify({"message": "Service updated successfully", "service_request": updated_service_data}), 200
            else:
                return jsonify({"error": "Service not found"}), 404
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            return jsonify({"error": str(e)}), 500
        
@app.route("/api/delete_sevreq/<int:sevreq_id>", methods=["DELETE"])
def delete_service_request(sevreq_id):
    try:
        sev_to_delete = Sevrequest.query.get(sevreq_id)
        print(sev_to_delete)
        if not sev_to_delete:
            return jsonify({"error": "Service request not found"}), 404
        
        # Delete the service
        db.session.delete(sev_to_delete)
        db.session.commit()

        return jsonify({"message": "Service request deleted successfully"}), 200
    
    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return jsonify({"error": str(e)}), 500

@app.route("/api/close_sevreq/<int:sevreq_id>", methods=["POST"])
def close_service_request(sevreq_id):
    sevreq = Sevrequest.query.get(sevreq_id)
    print(sevreq,sevreq_id)
    if sevreq is None:
        return {"error": "Sevrequest not found"}, 404
    sevreq.sev_status = "closed"
    db.session.commit()
    return jsonify({"message": "Professional approval status updated successfully"}), 200


@app.route("/api/rate_sevreq/<sevreq_id>", methods=["POST"])
def cust_rate_sev(sevreq_id):
    sevreq = Sevrequest.query.get(sevreq_id)
    if not sevreq:
        return jsonify({"error": "Service request not found"}), 404
    if sevreq.sev_status == 'closed':
        data = request.get_json()
        get_rating = data.get("rating",None)
        remarks=data.get("remarks",None)
        sevreq.rating = get_rating
        sevreq.remarks = remarks
        db.session.commit()
        try:
            rate_sevreq_list= {
                    "sevreq_id": sevreq.sevreq_id,
                    "prof_email": sevreq.prof_email,
                    "cust_email": sevreq.cust_email,
                    "rating": sevreq.rating,
                    "sev_status": sevreq.sev_status,
                    "remarks": sevreq.remarks,
                    "sev_id": sevreq.sev_id
                    }  
            return jsonify({"message": "Service updated successfully", "service_request": rate_sevreq_list}), 200
            
        except (decimal.InvalidOperation, TypeError):
            return jsonify({"error": "Invalid rating value"}), 400
    else:
        return jsonify({
            "error": "Service request must be closed to rate"
        }), 400

@app.route("/api/cust_summary/<cust_email>", methods=["GET"])
def cust_summary(cust_email):
    try:
        requests = Sevrequest.query.filter_by(cust_email=cust_email).all()
        if not requests:
            return jsonify({"message": "No service requests found for this professional."}), 404
        
        requests_json = [request.to_json() for request in requests]
        return jsonify({
            "email": cust_email,
            "requests": requests_json
        })
    except Exception as e:
        print("Error in cust_summary:", e)
        return jsonify({"error": "An error occurred while fetching data."}), 500
    
#=================================================PROFESSIONAL==========================================================
@app.route("/api/prof_sevs_today/<prof_email>", methods=["GET"])
def prof_sevs_today(prof_email):
    try:
        prof= Professional.query.get(prof_email)
        sevreqs = Sevrequest.query.all()
        current_date = datetime.now().date()
        formatted_date = current_date.strftime("%d-%m-%Y")
        service_requests_today = [i for i in sevreqs if i.date_of_request== formatted_date and i.prof_email == prof.prof_email]
        requests_today= [
          {
              "sevreq_id":  requests_today.sevreq_id,
              "date_of_request":requests_today.date_of_request,
              "date_of_completion":requests_today.date_of_completion,
              "sev_status":requests_today.sev_status,
              "remarks":requests_today.remarks,
              "prof_email":requests_today.prof_email,
              "cust_email":requests_today.cust_email,
              "sev_id":requests_today.sev_id
          }for requests_today in service_requests_today
          ]
        return jsonify(requests_today), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500  
  
@app.route("/api/prof_closed_sevs/<prof_email>", methods=["GET"])
def prof_closed_sevs(prof_email):
    try:
        prof = Professional.query.get(prof_email)
        sevreqs = Sevrequest.query.all()
        trial=[i for i in sevreqs if i.prof_email == prof.prof_email]
        closed_service_requests = [i for i in sevreqs if i.sev_status == "closed" and i.prof_email == prof.prof_email]
        closed_requests= [
          {
              "sevreq_id":  closed_requests.sevreq_id,
              "date_of_request":closed_requests.date_of_request,
              "date_of_completion":closed_requests.date_of_completion,
              "sev_status":closed_requests.sev_status,
              "remarks":closed_requests.remarks,
              "prof_email":closed_requests.prof_email,
              "cust_email":closed_requests.cust_email,
              "sev_id":closed_requests.sev_id,
              "rating":closed_requests.rating
          }for closed_requests in closed_service_requests
          ]
        print(closed_service_requests)
        return jsonify(closed_requests), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500  
  
@app.route("/api/prof_accept_sev/<int:sevreq_id>", methods=["POST"])
def prof_accept_sev(sevreq_id):
    try:
        sevreq = Sevrequest.query.get(sevreq_id)
        sevreq.sev_status = "accepted"
        db.session.commit()
        return jsonify({"message": "Service request accepted"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/prof_reject_sev/<int:sevreq_id>", methods=["POST"])
def prof_reject_sev(sevreq_id):
    try:
        sevreq = Sevrequest.query.get(sevreq_id)
        sevreq.sev_status = "rejected"
        db.session.commit()
        return jsonify({"message": "Service request rejected"}), 200
    
    except Exception as e:  
        return jsonify({"error": str(e)}), 500  
    
@app.route("/api/prof_close_sev/<int:sevreq_id>", methods=["POST"])
def prof_close_sev(sevreq_id):
    try:
        sevreq = Sevrequest.query.get(sevreq_id)
        sevreq.sev_status = "closed"
        db.session.commit()
        return jsonify({"message": "Service request closed"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500  
    

@app.route("/api/prof_update/<prof_email>", methods=["GET", "POST"])
def prof_update(prof_email):
    if request.method == "GET":
        prof = Professional.query.get(prof_email)
        if not prof:
            return jsonify({"error": "Professional not found"}), 404
        else:
            prof_data = { "prof_email": prof.prof_email,
                           "prof_password": prof.prof_password,
                           "service_type": prof.service_type,
                           "experience": prof.experience,
                           "address": prof.address,
                           "pincode": prof.pincode,
                           "description": prof.description}
        return jsonify(prof_data), 200
    if request.method == "POST":
        data = request.get_json() 
        prof_email= data.get("prof_email")
        prof_password = data.get("prof_password")
        service_type = data.get("service_type")
        experience = data.get("experience")
        address = data.get("address")
        pincode = data.get("pincode")
        description = data.get("description")

        update_prof = Professional.query.get(prof_email)
        if not update_prof:
            return jsonify({"error": "Professional not found"}), 404

        update_prof.prof_email = prof_email
        update_prof.prof_password = prof_password
        update_prof.service_type = service_type
        update_prof.experience = experience
        update_prof.address = address
        update_prof.pincode = pincode
        update_prof.description = description
        db.session.commit()
        updated_prof_data = { "prof_email": update_prof.prof_email,
                              "prof_password": update_prof.prof_password,
                              "service_type": update_prof.service_type,
                              "experience": update_prof.experience,
                              "address": update_prof.address,
                              "pincode": update_prof.pincode,
                              "description": update_prof.description}
        return jsonify({"message": "Professional profile updated successfully", "prof_data": updated_prof_data}), 200

@app.route("/api/professional/<prof_email>", methods=["GET"])
def get_professional_info(prof_email):
    prof = Professional.query.get(prof_email)
    print(prof)
    if not prof:
        return jsonify({"error": "Professional not found"}), 404
    prof_data = {
        "prof_email": prof.prof_email,
        "prof_password": prof.prof_password,
        "service_type": prof.service_type,
        "experience": prof.experience,
        "address": prof.address,
        "pincode": prof.pincode,
        "description": prof.description
    }
    
    # Return JSON response with status code 200
    return jsonify(prof_data), 200

@app.route("/api/prof_summary/<prof_email>", methods=["GET"])
def prof_summary(prof_email):
    try:
        requests = Sevrequest.query.filter_by(prof_email=prof_email).all()
        if not requests:
            return jsonify({"message": "No service requests found for this professional."}), 404
        
        requests_json = [request.to_json() for request in requests]
        return jsonify({
            "email": prof_email,
            "requests": requests_json
        })
    except Exception as e:
        print("Error in prof_summary:", e)
        return jsonify({"error": "An error occurred while fetching data."}), 500



#========================================================================================================================
# -------------------------------------HOME----------------------------------------------------------------------
    
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


#--------------------------------------------------------------PROFESSIONAL-----------------------------------------------------------------------
#register
#login
#home- todays services, closed services , view+edit profile
#search- Customers ,Requests by name,loc, pin , or by text- date
   #view all the service requests from all the customers
   #accept/reject a particular service request
   #close the service request once completed*
#summary graphs 


    
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
    
# #statistics
# @app.route("/cust_summary", methods=["GET"])
# def cust_summary():
#     # return a list of all the json objects of chart data for each venue
#     profs=Professional.query.all() 
#     custs=Customer.query.all()
#     reqs=Sevrequest.query.all()
#     sevs=Service.query.all()
#     services_json=[sev.to_json() for sev in sevs]
#     profs_json=[prof.to_json() for prof in profs]
#     custs_json=[cust.to_json() for cust in custs]
#     reqs_json=[req.to_json() for req in reqs]
#     return render_template("cust_summary.html", sevs=sevs,custs=custs,reqs=reqs,profs=profs,services_json=services_json,profs_json=profs_json,custs_json=custs_json,reqs_json=reqs_json)
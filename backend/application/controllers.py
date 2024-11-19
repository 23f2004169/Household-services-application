from flask import current_app as app 
from flask import render_template,request,Flask,jsonify,send_from_directory
from application.models import *
from datetime import datetime,date
import os,decimal,logging
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required,get_jwt,verify_jwt_in_request,current_user
from werkzeug.utils import secure_filename
from sqlalchemy import or_
from flask_caching import Cache
from functools import wraps

cache = Cache(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    try:
        token = get_jwt()
        if not token:
            return jsonify({"error": "Missing token"}), 401   
        current_user = get_jwt_identity()
        if not current_user:
            return jsonify({"error": "Invalid token format"}), 422 
        return jsonify({"message": f"Hello, {current_user}!"}), 200 
    except Exception as e:
        logging.error(f"Token validation error: {str(e)}")
        return jsonify({"error": "Token validation failed"}), 500
    
def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get('role')
            print(user_role,allowed_roles)
            if not user_role or user_role not in allowed_roles:
                return {'message': 'Your role is not authorized'}, 401
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route("/api/login",methods=['GET','POST'])
def login():
    data = request.get_json()
    email = data.get("email", None)
    password = data.get("password", None)
    role=data.get("role",None)
    if role=="admin":
        admin_exist = Admin.query.filter_by(admin_email="irina@gmail.com").first()
        if not admin_exist:
            user= Admin(admin_email="irina@gmail.com", 
            admin_password=generate_password_hash("irina24"))
            db.session.add(user)
            db.session.commit()
        admin_from_db=Admin.query.filter_by(admin_email=email).first()
        if not admin_from_db:
            return jsonify(error="Admin account with this email does not exist"), 404

        if not check_password_hash(admin_from_db.admin_password, password):
            return jsonify(error="Incorrect password"), 401

        if admin_from_db and check_password_hash(admin_from_db.admin_password, password):
                access_token = create_access_token(identity=admin_from_db.admin_email,additional_claims={'role':'admin'})
                return {"message": "login successful","access_token":access_token,"role":"admin"}
        return jsonify(error="Authentication failed"), 401  
    
    if role=="prof":
        prof_from_db=Professional.query.filter_by(prof_email=email).first() 
        if not prof_from_db:
            return jsonify(error="Professional account with this email does not exist"), 404
        if not check_password_hash(prof_from_db.prof_password, password):
            return jsonify(error="Incorrect password"), 401
        if prof_from_db and check_password_hash(prof_from_db.prof_password, password):
            if prof_from_db.blocked:
                return jsonify(error="Your account has been blocked"), 403          
            access_token = create_access_token(identity=prof_from_db.prof_email,additional_claims={'role': 'prof'})
            return {"message": "login successful","access_token":access_token,"role":"prof"}                      
        return jsonify(error="Authentication failed"), 401
    
    if role=="cust":
        cust_from_db=Customer.query.filter_by(cust_email=email).first() 
        if not cust_from_db:
            return jsonify(error="Customer account with this email does not exist"), 404
        if not check_password_hash(cust_from_db.cust_password, password):
            return jsonify(error="Incorrect password"), 401
        if cust_from_db and check_password_hash(cust_from_db.cust_password, password):
            if cust_from_db.blocked:
                return jsonify(error="Your account has been blocked"), 403
            access_token = create_access_token(identity=cust_from_db.cust_email,additional_claims={'role': 'cust'})
            return {"message": "login successful","access_token":access_token,"role":"cust"}                   
        return jsonify(error="Authentication failed"), 401
    
    return jsonify(error="Invalid role specified"), 400

@app.route("/api/cust_reg", methods=['POST'])
def cust_reg():
    if request.method == "POST":
        data = request.get_json()
        cust_email = data.get("cust_email")
        cust_password = data.get("cust_password")
        address = data.get("address")
        pincode = data.get("pincode")
        phone=data.get("phone")
        if not cust_password or cust_password.strip() == "":
            return jsonify({"error":"Password cannot be empty"}), 400
        
        exist = Customer.query.filter_by(cust_email=cust_email).first()
        if exist:
            return jsonify({"error":"Customer username already exists"}), 400          
        new_cust = Customer(
            cust_email=cust_email,
            cust_password=generate_password_hash(cust_password),
            address=address,
            pincode=pincode,
            phone=phone
        )
        db.session.add(new_cust)
        db.session.commit()
        return jsonify({"msg":"Registration successful", "cust_email":"cust_email"}), 201 
    return jsonify({"error":"An error occurred during registration"}), 500  

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORT_FOLDER'] = "reports"  
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
def allowed_file(filename):
  return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/prof_reg', methods=['GET', 'POST'])
def prof_reg():
    if request.method == "POST":
        prof_email = request.form.get("prof_email")
        prof_password = request.form.get("prof_password")
        service_type = request.form.get("service_type")
        experience = request.form.get("experience")
        address = request.form.get("address")
        pincode = request.form.get("pincode")
        description = request.form.get("description")
        phone = request.form.get("phone")
        image_file = request.files.get('image')
        document_file = request.files.get('file')   

        image_filename = None
        document_filename = None
      
    if image_file and allowed_file(image_file.filename):
        image_filename=prof_email.split("@")[0]+"."+ image_file.filename.split(".")[-1]
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename) )         
    if document_file and allowed_file(document_file.filename):
        document_filename=prof_email.split("@")[0]+"."+ document_file.filename.split(".")[-1]
        document_file.save(os.path.join(app.config['UPLOAD_FOLDER'], document_filename) ) 

    if not prof_password or prof_password.strip() == "":
        return jsonify({"error": "Password cannot be empty"}), 400
      
    exist = Professional.query.filter_by(prof_email=prof_email).first()
    if exist:
        return jsonify({"error": "Professional username already exists"}), 400

    new_prof = Professional(
        prof_email=prof_email,
        prof_password=generate_password_hash(prof_password),
        service_type=service_type,
        experience=experience,
        address=address,
        pincode=pincode,
        description=description,
        date_created=datetime.now().date(),
        phone=phone,
        image=image_filename,  
        file=document_filename  
    )  
    db.session.add(new_prof)
    db.session.commit()
    return jsonify({"msg": "Registration successful", "prof_email": prof_email}), 201
  
@app.route('/api/view-document/<prof_email>', methods=['GET'])
def view_document(prof_email):
    try:
        professional = Professional.query.filter_by(prof_email=prof_email).first()
        if not professional or not professional.file:
            return jsonify({"error": "Document not found"}), 404    
        filename = os.path.basename(professional.file)
        return send_from_directory(app.config['UPLOAD_FOLDER'],filename,as_attachment=False  # This will display in browser instead of downloading
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
  
@app.route('/api/view-image/<prof_email>', methods=['GET'])
def view_image(prof_email):
  try:
      professional = Professional.query.filter_by(prof_email=prof_email).first()
      if not professional or not professional.image:
          return jsonify({"error": "Image not found"}), 404
          
      filename = os.path.basename(professional.image)
      return send_from_directory(
          app.config['UPLOAD_FOLDER'],
          filename,
          as_attachment=False  # This will display in browser instead of downloading
      )
  except Exception as e:
      return jsonify({"error": str(e)}), 500

@app.route('/api/reports/<filename>', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_reports(filename):
    try:
        return send_from_directory(app.config['REPORT_FOLDER'], filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#async trigger job
@app.route('/api/export-professional/<prof_email>', methods=['POST'])
@jwt_required()
def export_professional(prof_email):
    from main import user_triggered_async_job  
    if not prof_email:
        return jsonify({'error': 'Professional email is required'}), 400
    var=user_triggered_async_job.delay(prof_email)
    print("triggered job",var)
    return jsonify({'message': 'Export job started successfully, you will be notified when it completes.'}), 202

@app.route('/api/reg_servicenames', methods=['GET'])
def reg_servicenames():
    try:
        services = Service.query.all()
        services_list = [
            { 'sev_name': service.sev_name,
            } for service in services
        ]
        return jsonify(services_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

#===========================================ADMIN====================================================================================================
@app.route('/api/services', methods=['GET'])
@jwt_required()
@role_required(['admin'])
@cache.memoize(timeout=50)
def get_services():
    try:
        services = Service.query.all()
        services_list = [
            {   'sev_id': service.sev_id,
                'sev_name': service.sev_name,
                'description': service.description,
                'price': service.price,
                'time_req': service.time_req,
                'address': service.address,
                'category': service.category,
                'pincode' : service.pincode
            } for service in services
        ]
        return jsonify(services_list), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/professionals", methods=["GET"])
@jwt_required()
@role_required(['admin','cust'])
@cache.memoize(timeout=50)
def get_professionals():
    try:
        prof= request.args.get('email')
        if prof:    
            professionals= Professional.query.filter_by(prof_email=prof).all()
        else:
            professionals = Professional.query.all()
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
                'approval': professional.approval,
                'phone': professional.phone,
                'rating': professional.rating
            } for professional in professionals
        ]
        return jsonify(professionals_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/service_requests", methods=["GET"])
@jwt_required()
@role_required(['admin'])
@cache.memoize(timeout=50)
def get_service_requests():
    try:
        service_requests = Sevrequest.query.all()
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
                'rating': service_request.rating
            } for service_request in service_requests
        ]
        return jsonify(service_requests_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/customers", methods=["GET"])
@jwt_required()
@role_required(['admin'])
@cache.memoize(timeout=50)
def get_customers():
    try:
        cust= request.args.get('email')
        if cust:    
            customers = Customer.query.filter_by(cust_email=cust).all()
        else:
            customers = Customer.query.all()
        customers_list = [
            {
                'cust_email': customer.cust_email,
                'address': customer.address,
                'pincode': customer.pincode,
                'blocked': customer.blocked,
                'phone': customer.phone
            } for customer in customers
        ]
        return jsonify(customers_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/create_sev", methods=["POST"])
@jwt_required()
@role_required(['admin'])
def admin_create_sev():
    if request.method == "POST":
        data = request.get_json()
        if data:
            existing_service = Service.query.filter_by(sev_name=data['sev_name']).first()
            if not existing_service:
                sev_name = data.get("sev_name")
                price = data.get("price")
                time_req = data.get("time_req")
                description = data.get("description")
                category = data.get("category")
                address=data.get("address")
                pincode = data.get("pincode") 
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
                cache.delete_memoized(get_services)
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
@jwt_required()
@role_required(['admin'])
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
                cache.delete_memoized(get_services)
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
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500

@app.route("/api/delete_sev/<int:sev_id>", methods=["DELETE"])
@jwt_required()
@role_required(['admin'])
def admin_delete_sev(sev_id):
    try:
        sev_to_delete = Service.query.get(sev_id)
        if not sev_to_delete:
            return jsonify({"error": "Service not found"}), 404
        
        db.session.delete(sev_to_delete)
        db.session.commit()
        cache.delete_memoized(get_services)
        return jsonify({"message": "Service deleted successfully"}), 200
    
    except Exception as e:
        db.session.rollback()  
        return jsonify({"error": str(e)}), 500

@app.route("/api/professional/approve/<prof_email>", methods=["POST"])
@jwt_required()
@role_required(['admin'])
def admin_approve_prof(prof_email):
    professionals = Professional.query.get(prof_email)
    if professionals is None:
        return {"error": "Professional not found"}, 404
    professionals.approval ="approved"
    db.session.commit()
    cache.delete_memoized(get_professionals)
    return jsonify({"message": "Professional approval status updated successfully"}), 200

@app.route("/api/professional/reject/<prof_email>", methods=["POST"])
@jwt_required()
@role_required(['admin'])
def admin_reject_prof(prof_email):
    professionals = Professional.query.get(prof_email)
    if professionals is None:
        return {"error": "Professional not found"}, 404
    professionals.approval ="rejected"
    db.session.commit()
    cache.delete_memoized(get_professionals)
    return jsonify({"message": "Professional approval status updated successfully"}), 200

@app.route("/api/professional/block/<prof_email>", methods=["POST"])
@jwt_required()
@role_required(['admin'])
def admin_block_prof(prof_email):
    professionals = Professional.query.get(prof_email)
    if professionals is None:
        return {"error": "Professional not found"}, 404
    professionals.blocked = not professionals.blocked
    db.session.commit()
    cache.delete_memoized(get_professionals)
    return jsonify({"message": "Professional approval status updated successfully"}), 200

@app.route("/api/professional/delete/<cust_email>", methods=["DELETE"])
@jwt_required()
@role_required(['admin'])
def admin_delete_prof(cust_email):
    professionals = Professional.query.get(cust_email)
    if professionals is None:
        return {"error": "Professional not found"}, 404
    db.session.delete(professionals)
    db.session.commit()
    cache.delete_memoized(get_professionals)
    cache.delete_memoized(get_service_requests)
    return jsonify({"message": "Professional deleted successfully"}), 200

@app.route("/api/customer/block/<cust_email>", methods=["POST"])
@jwt_required()
@role_required(['admin']) 
def admin_block_cust(cust_email):
    customers = Customer.query.get(cust_email)
    if customers is None:
        return {"error": "Customer not found"}, 404 
    customers.blocked = not customers.blocked
    db.session.commit()
    cache.delete_memoized(get_customers)
    return jsonify({"message": "Customer approval status updated successfully"}), 200    

@app.route("/api/customer/delete/<cust_email>", methods=["DELETE"])
@jwt_required()
@role_required(['admin'])
def admin_delete_cust(cust_email):
    customers = Customer.query.get(cust_email)
    if customers is None:
        return {"error": "Customer not found"}, 404
    db.session.delete(customers)
    db.session.commit()
    cache.delete_memoized(get_customers)
    cache.delete_memoized(get_service_requests)
    return jsonify({"message": "Customer deleted successfully"}), 200

@app.route("/api/admin_summary", methods=["GET"])
@jwt_required()
@role_required(['admin'])
def api_admin_summary():
    cache.delete_memoized(get_service_requests)
    profs = Professional.query.all()
    custs = Customer.query.all()
    reqs = Sevrequest.query.all()
    sevs = Service.query.all()
    print(reqs)
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
    
@app.route("/api/admin_search", methods=["POST"])
def admin_search():
    data = request.get_json() 
    query = data.get("query", "").strip()
    results = Professional.query.filter(
        or_(
            Professional.prof_email.ilike(f"%{query}%"),
            Professional.service_type.ilike(f"%{query}%"),
            Professional.description.ilike(f"%{query}%"),
            Professional.experience.ilike(f"%{query}%"),
            Professional.address.ilike(f"%{query}%"),
            Professional.pincode.ilike(f"%{query}%"),
           Professional.rating.ilike(f"%{query}%"),)).all()
    if results:
        result_list = [{
            "prof_email": result.prof_email,
            "description": result.description,
            "service_type": result.service_type,
            "experience": result.experience,
            "address": result.address,
            "pincode": result.pincode,
            "phone": result.phone,
            "rating": result.rating,
            "blocked": result.blocked,
            "approval": result.approval,
        } for result in results]
        return jsonify({"results": result_list}), 200
    return jsonify({"results": []}), 200

#=========================================CUSTOMER ============================================================================================
@app.route('/api/servicesforcust', methods=['GET'])
@jwt_required()
@role_required(['cust'])
def get_servicesforcust():
    try:
        category = request.args.get('category')
        if category:
            services = Service.query.filter_by(category=category).all()
        else:
            services = Service.query.all()
        services_list = [
            {   'sev_id': service.sev_id,
                'sev_name': service.sev_name,
                'description': service.description,
                'price': service.price,
                'time_req': service.time_req,
                'address': service.address,
                'category': service.category,
                'pincode' : service.pincode
            } for service in services
        ]
        return jsonify(services_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/update_customer/<cust_email>', methods=['PUT'])
@jwt_required()
@role_required(['cust'])
def update_customer(cust_email):
    try:
        data = request.json
        customer_to_update = Customer.query.filter_by(cust_email=cust_email).first()       
        if customer_to_update:
            customer_to_update.cust_email = data.get("cust_email", customer_to_update.cust_email)
            customer_to_update.phone = data.get("phone", customer_to_update.phone)
            customer_to_update.address = data.get("address", customer_to_update.address)
            customer_to_update.pincode = data.get("pincode", customer_to_update.pincode)            
            db.session.commit()
            cache.delete_memoized(get_customer_info, cust_email)                
            updated_customer_data = {
                "cust_email": customer_to_update.cust_email,
                "phone": customer_to_update.phone,
                "address": customer_to_update.address,
                "pincode": customer_to_update.pincode
            }        
            return jsonify({"message": "Customer updated successfully", "customer": updated_customer_data}), 200
        else:
            return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        db.session.rollback() 
        return jsonify({"error": str(e)}), 500

@app.route("/api/customer/<cust_email>", methods=["GET"])
@jwt_required()
@role_required(['cust'])
@cache.memoize(timeout=50)
def get_customer_info(cust_email):
    cust = Customer.query.get(cust_email)
    if not cust:
        return jsonify({"error": "Customer not found"}), 404
    cust_data = {
        "cust_email": cust.cust_email,
        "address": cust.address,
        "pincode": cust.pincode,
        "phone": cust.phone
    }
    return jsonify(cust_data), 200

@app.route('/api/create_sevrequest/<cust_email>', methods=['POST'])
@jwt_required()
@role_required(['cust'])
def create_service_request(cust_email):
    try:
        data = request.get_json()
        prof_email = data.get("prof_email")
        sev_id = data.get("sev_id")
        date_of_request = data.get("date_of_request")
        date_of_completion = data.get("date_of_completion")
        print(prof_email,sev_id,date_of_request,date_of_completion)
        print(type(date_of_request),type(date_of_completion))
        today = datetime.today()
        formatted_today = today.strftime("%Y-%m-%d")
        if date_of_request < formatted_today or date_of_completion < formatted_today:
            print(date_of_request,date_of_completion)
            return jsonify({
                "message": "Dates must be today or in the future"
            }), 400     
        new_request = Sevrequest(
            cust_email=cust_email,
            prof_email=prof_email,
            sev_id=sev_id,
            date_of_request=date_of_request,
            date_of_completion=date_of_completion,)
        db.session.add(new_request)
        db.session.commit()
        cache.delete_memoized(cust_service_requests, cust_email)
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
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 401
    
@app.route("/api/edit_sevreq/<int:sevreq_id>/<cust_email>", methods=["GET", "POST"])
@jwt_required()
@role_required(['cust'])
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
                "remarks": service_request.remarks}            
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
                cache.delete_memoized(cust_service_requests, cust_email)
                updated_service_data = {
                    "prof_email": sev_to_update.prof_email,
                    "cust_email": cust_email,
                    "date_of_request": sev_to_update.date_of_request,
                    "date_of_completion": sev_to_update.date_of_completion,
                    "sev_status": sev_to_update.sev_status,
                    "remarks": sev_to_update.remarks}
                return jsonify({"message": "Service updated successfully", "service_request": updated_service_data}), 200
            else:
                return jsonify({"error": "Service not found"}), 404
        except Exception as e:
            db.session.rollback()  
            return jsonify({"error": str(e)}), 500

@app.route("/api/delete_sevreq/<int:sevreq_id>", methods=["DELETE"])
@jwt_required()
@role_required(['cust'])
def delete_service_request(sevreq_id):
    try:
        sev_to_delete = Sevrequest.query.get(sevreq_id)
        if not sev_to_delete:
            return jsonify({"error": "Service request not found"}), 404   
        db.session.delete(sev_to_delete)
        db.session.commit()
        cache.delete_memoized(cust_service_requests, sev_to_delete.cust_email)
        return jsonify({"message": "Service request deleted successfully"}), 200   
    except Exception as e:
        db.session.rollback()  
        return jsonify({"error": str(e)}), 500

@app.route("/api/cust_service_requests/<cust_email>", methods=["GET"])
@jwt_required()
@role_required(['cust'])
@cache.memoize(timeout=50)
def cust_service_requests(cust_email):
    try:
        service_requests = Sevrequest.query.filter_by(cust_email=cust_email).all()
        service_requests_list = [
            {   'sevreq_id': service_request.sevreq_id,
                'prof_email': service_request.prof_email,
                'cust_email': service_request.cust_email,
                'sev_id': service_request.sev_id,
                'date_of_request': service_request.date_of_request,
                'date_of_completion': service_request.date_of_completion,
                'remarks': service_request.remarks,
                'sev_status': service_request.sev_status,
                'rating': service_request.rating,
            } for service_request in service_requests
        ]
        return jsonify(service_requests_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/rate_sevreq/<sevreq_id>", methods=["POST"])
@jwt_required()
@role_required(['cust'])
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
        cache.delete_memoized(cust_service_requests, sevreq.cust_email)
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
            return jsonify({"message": "Service rated successfully", "service_request": rate_sevreq_list}), 200
        except (decimal.InvalidOperation, TypeError):
            return jsonify({"error": "Invalid rating value"}), 400
    else:
        return jsonify({
            "error": "Service request must be closed to rate"
        }), 400

@app.route("/api/close_sevreq/<int:sevreq_id>", methods=["POST"])
@jwt_required()
@role_required(['cust'])
def close_service_request(sevreq_id):
    sevreq = Sevrequest.query.get(sevreq_id)
    if sevreq is None:
        return {"error": "Sevrequest not found"}, 404
    sevreq.sev_status = "closed"
    db.session.commit()
    cache.delete_memoized(cust_service_requests, sevreq.cust_email)
    return jsonify({"message": "Service request closed successfully"}), 200

@app.route("/api/cust_search", methods=["POST"])
@jwt_required()
@role_required(['cust'])
def cust_search():
    data = request.get_json()
    query = data.get("query", "").strip()
    sresults = Service.query.filter(
        or_(
            Service.sev_name.ilike(f"%{query}%"),
            Service.category.ilike(f"%{query}%"),
            Service.address.ilike(f"%{query}%"),
            Service.pincode.ilike(f"%{query}%") )).all()
    if sresults:
        result_list = [{"sev_id": result.sev_id,
                        "sev_name": result.sev_name,
                        "category": result.category,
                        "description": result.description,
                        "time_req": result.time_req,
                        "price": result.price,
                        "address": result.address,
                        "pincode": result.pincode} for result in sresults]
        return jsonify({"sresults": result_list}), 200
    return jsonify({"sresults": [], "message": "No sresults found"}), 200

@app.route("/api/cust_summary/<cust_email>", methods=["GET"])
@jwt_required()
@role_required(['cust'])
def cust_summary(cust_email):
    cache.delete_memoized(cust_service_requests)
    try:       
        requests = Sevrequest.query.filter_by(cust_email=cust_email).all()
        if not requests:
            return jsonify({"message": "No service requests found for this customer."}), 404        
        requests_json = [request.to_json() for request in requests]
        return jsonify({
            "email": cust_email,
            "requests": requests_json
        })
    except Exception as e:
        return jsonify({"error": "An error occurred while fetching data."}), 500
    
#=================================================PROFESSIONAL================================================================================

@app.route("/api/professional/<prof_email>", methods=["GET"])
@jwt_required()
@role_required(['prof'])
@cache.memoize(timeout=50)
def get_professional_info(prof_email):
    prof = Professional.query.get(prof_email)
    if not prof:
        return jsonify({"error": "Professional not found"}), 404
    prof_data = {
        "prof_email": prof.prof_email,
        "prof_password": prof.prof_password,
        "service_type": prof.service_type,
        "experience": prof.experience,
        "address": prof.address,
        "pincode": prof.pincode,
        "description": prof.description,
        "phone": prof.phone,
        "rating": prof.rating,
        "image": prof.image,
        "approval": prof.approval
    }
    return jsonify(prof_data), 200

@app.route("/api/prof_update/<prof_email>", methods=["GET", "POST"])
@jwt_required()
@role_required(['prof'])
def prof_update(prof_email):
    if request.method == "GET":
        prof = Professional.query.get(prof_email)
        if not prof:
            return jsonify({"error": "Professional not found"}), 404
        else:
            prof_data = { "prof_email": prof.prof_email,
                           "service_type": prof.service_type,
                           "experience": prof.experience,
                           "address": prof.address,
                           "pincode": prof.pincode,
                           "description": prof.description,
                           "rating": prof.rating }
        return jsonify(prof_data), 200  
     
    if request.method == "POST":
        data = request.get_json() 
        prof_email= data.get("prof_email")
        service_type = data.get("service_type")
        experience = data.get("experience")
        address = data.get("address")
        pincode = data.get("pincode")
        description = data.get("description")
        phone = data.get("phone")
        update_prof = Professional.query.get(prof_email)
        if not update_prof:
            return jsonify({"error": "Professional not found"}), 404       
        update_prof.prof_email = prof_email
        update_prof.service_type = service_type
        update_prof.experience = experience
        update_prof.address = address
        update_prof.pincode = pincode
        update_prof.description = description
        update_prof.phone = phone
        db.session.commit()
        cache.delete_memoized(get_professional_info, prof_email)
        updated_prof_data = { "prof_email": update_prof.prof_email,
                              "service_type": update_prof.service_type,
                              "experience": update_prof.experience,
                              "address": update_prof.address,
                              "pincode": update_prof.pincode,
                              "description": update_prof.description,
                              "phone": update_prof.phone}
        return jsonify({"message": "Professional profile updated successfully", "prof_data": updated_prof_data}), 200

@app.route("/api/prof_sevs_today/<prof_email>", methods=["GET"])
@jwt_required()
@role_required(['prof'])
@cache.memoize(timeout=50)
def prof_sevs_today(prof_email):
    try:
        prof= Professional.query.get(prof_email)
        sevreqs = Sevrequest.query.all()
        current_date = datetime.now().date()
        formatted_date = current_date.strftime("%Y-%m-%d")
        service_requests_today = [i for i in sevreqs if i.date_of_request== formatted_date and i.prof_email == prof.prof_email]
        requests_today= [ {   
              "sevreq_id":  requests_today.sevreq_id,
              "date_of_request":requests_today.date_of_request,
              "date_of_completion":requests_today.date_of_completion,
              "sev_status":requests_today.sev_status,
              "remarks":requests_today.remarks,
              "prof_email":requests_today.prof_email,
              "cust_email":requests_today.cust_email,
              "sev_id":requests_today.sev_id
          }for requests_today in service_requests_today]
        return jsonify(requests_today), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500  
  
@app.route("/api/prof_closed_sevs/<prof_email>", methods=["GET"])
@jwt_required()
@role_required(['prof'])
@cache.memoize(timeout=50)
def prof_closed_sevs(prof_email):
    try:
        prof = Professional.query.get(prof_email)
        sevreqs = Sevrequest.query.all()
        closed_service_requests = [i for i in sevreqs if i.sev_status == "closed" and i.prof_email == prof.prof_email]
        closed_requests= [{
              "sevreq_id":  closed_requests.sevreq_id,
              "date_of_request":closed_requests.date_of_request,
              "date_of_completion":closed_requests.date_of_completion,
              "sev_status":closed_requests.sev_status,
              "remarks":closed_requests.remarks,
              "prof_email":closed_requests.prof_email,
              "cust_email":closed_requests.cust_email,
              "sev_id":closed_requests.sev_id,
              "rating":closed_requests.rating
          }for closed_requests in closed_service_requests]
        return jsonify(closed_requests), 200   
    except Exception as e:
        return jsonify({"error": str(e)}), 500  
  
@app.route("/api/prof_pending_sevs/<prof_email>", methods=["GET"])
@cache.memoize(timeout=50)
@jwt_required()
@role_required(['prof'])
@cache.memoize(timeout=50)
def prof_pending_sevs(prof_email):
    try:
        prof = Professional.query.get(prof_email)
        sevreqs = Sevrequest.query.all()
        current_date = datetime.now().date()
        formatted_date = current_date.strftime("%Y-%m-%d")
        service_requests = [i for i in sevreqs if  i.sev_status in["requested", "accepted"] and i.date_of_completion>= formatted_date and i.prof_email == prof.prof_email]
        pending_requests= [{
              "sevreq_id":  service_request.sevreq_id,
              "date_of_request":service_request.date_of_request,
              "date_of_completion":service_request.date_of_completion,
              "sev_status":service_request.sev_status,
              "remarks":service_request.remarks,
              "prof_email":service_request.prof_email,
              "cust_email":service_request.cust_email,
              "sev_id":service_request.sev_id,
              "rating":service_request.rating
          }for service_request in service_requests]
        return jsonify(pending_requests), 200   
    except Exception as e:
        return jsonify({"error": str(e)}), 500  

@app.route("/api/prof_accept_sev/<int:sevreq_id>", methods=["POST"])
@jwt_required()
@role_required(['prof'])
def prof_accept_sev(sevreq_id):
    try:
        sevreq = Sevrequest.query.get(sevreq_id)
        sevreq.sev_status = "accepted"
        db.session.commit()
        cache.delete_memoized(prof_closed_sevs, sevreq.prof_email)
        cache.delete_memoized(prof_pending_sevs, sevreq.prof_email)
        cache.delete_memoized(prof_sevs_today, sevreq.prof_email)
        return jsonify({"message": "Service request accepted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/prof_reject_sev/<int:sevreq_id>", methods=["POST"])
@jwt_required()
@role_required(['prof'])
def prof_reject_sev(sevreq_id):
    try:
        sevreq = Sevrequest.query.get(sevreq_id)
        sevreq.sev_status = "rejected"
        db.session.commit()
        cache.delete_memoized(prof_closed_sevs, sevreq.prof_email)
        cache.delete_memoized(prof_pending_sevs, sevreq.prof_email)
        cache.delete_memoized(prof_sevs_today, sevreq.prof_email)
        return jsonify({"message": "Service request rejected"}), 200    
    except Exception as e:  
        return jsonify({"error": str(e)}), 500  
    
@app.route("/api/prof_close_sev/<int:sevreq_id>", methods=["POST"])
@jwt_required()
@role_required(['prof'])
def prof_close_sev(sevreq_id):
    try:
        sevreq = Sevrequest.query.get(sevreq_id)
        sevreq.sev_status = "closed"
        db.session.commit()
        cache.delete_memoized(prof_closed_sevs, sevreq.prof_email)
        cache.delete_memoized(prof_pending_sevs, sevreq.prof_email)
        cache.delete_memoized(prof_sevs_today, sevreq.prof_email)
        return jsonify({"message": "Service request closed"}), 200  
    except Exception as e:
        return jsonify({"error": str(e)}), 500  
    
@app.route("/api/prof_rating/<prof_email>", methods=["POST"])
@jwt_required()
@role_required(['prof'])
def prof_rating(prof_email):
    try:
        rating = 0
        count = 0
        prof = Professional.query.filter_by(prof_email=prof_email).first()
        if not prof:
            return jsonify(error="Professional not found"), 404
        for x in prof.prof_req:
            if x.sev_status == "closed":
                rating += x.rating
                count += 1
        average_rating = round(rating /count, 2) if prof.prof_req else 0
        prof.rating=average_rating
        db.session.commit()
        return jsonify(prof.rating), 200    
    except Exception as e:
        return jsonify({"error":str(e)}),500

@app.route('/api/reupload-document/<prof_email>', methods=['POST'])
def reupload_document(prof_email):
    professional = Professional.query.filter_by(prof_email=prof_email).first()
    if not professional:
        return jsonify({"error": "Professional not found"}), 404
    if professional.approval != "rejected":
        return jsonify({"error": "Document re-upload is only allowed if status is 'rejected'"}), 403

    document_file = request.files.get('document')
    if not document_file or not allowed_file(document_file.filename):
        return jsonify({"error": "Invalid document file"}), 400
    new_document_filename = prof_email.split("@")[0] + "_reupload." + document_file.filename.split(".")[-1]
    document_path = os.path.join(app.config['UPLOAD_FOLDER'], new_document_filename)
    document_file.save(document_path)
    professional.file = new_document_filename
    db.session.commit()
    return jsonify({"msg": "Document re-upload successful"}), 200

@app.route("/api/prof_summary/<prof_email>", methods=["GET"])
@jwt_required()
@role_required(['prof'])
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
        return jsonify({"error": "An error occurred while fetching data."}), 500

@app.route("/api/prof_search/<prof_email>", methods=["POST"])
@jwt_required()
@role_required(['prof'])
def prof_search(prof_email):
    data = request.get_json() 
    query = data.get("query", "").strip()
    results = Sevrequest.query.filter(
        Sevrequest.prof_email == prof_email,
        or_(
            Sevrequest.sev_status.ilike(f"%{query}%"),
            Sevrequest.rating.ilike(f"%{query}%") )).all()
    if results:
        result_list = [{
            "sevreq_id": result.sevreq_id,
            "cust_email": result.cust_email,
            "prof_email": result.prof_email,
            "sev_status": result.sev_status,
            "rating": result.rating,
            "remarks": result.remarks,
            "date_of_request": result.date_of_request,
            "date_of_completion": result.date_of_completion,
        } for result in results]
        return jsonify({"results": result_list}), 200
    return jsonify({"results": [], "message": "No results found"}), 200





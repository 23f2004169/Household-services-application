<template>
    <div class="container custbody">
        <header>
        <CustBar :email="email"/>
        <h2 class="white">Welcome Customer</h2>
        <p class="white">Your email: {{ email }}</p>
        <button @click.prevent="openUpdateCustForm(customer)"  class="white" style="background-color: rgb(63, 35, 18);">Edit your profile</button>
        </header>

      <h1 class="white">Category of Services</h1> 
        <div class="rating white">
            <span class="star white">★★★★</span>
        </div>      
        <div class="services">
            <div class="service-card" @click="navigateToCategory('Child_Elderly Care Services')">
                <img src="/static/childcare.jpeg" alt="Child_Elderly Care Services">
                <h3>Child_Elderly Care Services</h3>
            </div>
            <div class="service-card" @click="navigateToCategory('Lifestyle and Convenience Services') ">
                <div class="badge">Trending Now</div>
                <img src="/static/mealprep.jpeg" alt="Lifestyle and Convenience Services">
                <h3>Lifestyle and Convenience Services</h3>
            </div>

            <div class="service-card"  @click="navigateToCategory('Home Maintenance Services')">
                <img src="/static/specialized.jpeg" alt="Home Maintenance Services">
                <h3>Home Maintenance Services</h3>
            </div>

            <div class="service-card" @click="navigateToCategory('Cleaning and Organization Services')">
                <div class="badge">Trending Now</div>
                <img src="/static/homeorg.jpeg"  alt="Cleaning and Organization Services">
                <h3>Cleaning and Organization Service</h3>
            </div>
        </div>
      <br><br>
      <!-- Service Requests Table -->
      <section class="mb-5">
        <h3 class="white">HISTORY: Service Requests</h3>
        <table class="table table-striped table-hover">
          <thead class="thead-dark">
            <tr>
              <th>ID</th>
              <th>Assigned Professional</th>
              <th>Customer</th>
              <th>Requested Date</th>
              <th>Completion Date</th>
              <th>Service ID</th>
              <th>Status (R/A/C)</th>
              <th>Rating</th>
              <th>Remarks</th>
              <th></th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="( service_request, index) in service_requests" :key="index">
              <td>{{ service_request.sevreq_id }}</td>
              <td>{{ service_request.prof_email }}</td>
              <td>{{ service_request.cust_email }}</td>
              <td>{{ service_request.date_of_request }}</td>
              <td>{{ service_request.date_of_completion }}</td>
              <td>{{ service_request.sev_id }}</td>
              <td>{{ service_request.sev_status }}</td>
              <td>{{ service_request.rating }}</td>
              <td>{{ service_request.remarks }}</td>
              <td>
                <div class="d-flex">
                    <button v-if="service_request.sev_status === 'requested' || service_request.sev_status === 'accepted'"
                     @click.prevent="closeServiceRequest(service_request.sevreq_id)"class="btn btn-info btn-sm mr-5">Close</button>
        
                    <button v-else-if="service_request.sev_status === 'closed'"
                     @click.prevent="openRateServiceForm(service_request)" class="btn btn-violet btn-sm mr-5">Rate</button>
                </div>
                
              </td>
              <td>
                <div class="d-flex">
                <button @click.prevent="openEditServiceForm(service_request)" class="btn btn-warning btn-sm mr-5">Edit</button>
                <button @click.prevent="deleteService(service_request.sevreq_id)" class="btn btn-danger btn-sm mr-5">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- Edit Service Request Form Modal -->
      <div v-show="showEditServiceForm" class="modal fade show" style="display: block;" tabindex="-1">
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title">Edit Service</h5>
                      <button @click.prevent="showEditServiceForm = false" class="btn-close"></button>
                    </div>
                    <div class="modal-body">
                    <form @submit.prevent="editService(editedService.sevreq_id)">
                        <div class="mb-3">
                          <label class="form-label">Service Request ID:</label>
                          <input v-model="editedService.sevreq_id" type="text" class="form-control" required readonly/>
                        </div>
                        <div class="mb-3">  
                          <label class="form-label">Professional Email:</label>
                          <input v-model="editedService.prof_email" type="text" class="form-control" required />
                        </div>
                        <div class="mb-3">
                          <label class="form-label">Remarks:</label>
                          <textarea v-model="editedService.remarks" class="form-control" ></textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Status:</label>
                            <select v-model="editedService.sev_status" class="form-control" required >
                           <option value="" disabled>Select a category</option>
                           <option value="requested">Requested</option>
                           <option value="accepted">Accepted</option>
                           <option value="closed">Closed</option>
                           </select> 
                        </div>
                        
                        <div class="mb-3">
                          <label class="form-label">Date of request:</label>
                          <input v-model="editedService.date_of_request" type="text" class="form-control" required />
                        </div>

                        <div class="mb-3">
                          <label class="form-label">Date of Completion:</label>
                          <input v-model="editedService.date_of_completion" type="text" class="form-control" required />
                        </div>
                        
                        <div class="modal-footer">
                          <button type="submit" class="btn btn-primary">Save Changes</button>
                          <button @click.prevent="showEditServiceForm = false" class="btn btn-secondary">Cancel</button>
                        </div>
                      </form>
                  </div>
            </div>
        </div>
    </div>
    
    <!-- RATE Service Request Form Modal -->
    <div v-show="showRateServiceForm" class="modal fade show" style="display: block;" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Rate Service Request</h5>
                <button @click.prevent="showRateServiceForm = false" class="btn-close"></button>
            </div>
            <div class="modal-body">
                <form @submit.prevent="ratedService(rateService.sevreq_id)">
                    <div class="mb-3">
                        <label class="form-label">Service Request ID:</label>
                        <input v-model="rateService.sevreq_id" type="text" class="form-control" required readonly />
                    </div>
                    <!-- <div class="mb-3">
                        <label class="form-label">Rating:</label>
                        <input v-model.number="rateService.rating" type="number" class="form-control" min="1" max="5" placeholder="Rate between 1 and 5" required />
                    </div> -->
                    <div class="mb-3">
                     <label class="form-label">Rating:</label>
                     <div class="star-rating">
                         <input type="radio" id="star5" v-model="rateService.rating" :value="5" />
                         <label for="star5" title="5 stars">★</label>
                         
                         <input type="radio" id="star4" v-model="rateService.rating" :value="4" />
                         <label for="star4" title="4 stars">★</label>
                         
                         <input type="radio" id="star3" v-model="rateService.rating" :value="3" />
                         <label for="star3" title="3 stars">★</label>
                         
                         <input type="radio" id="star2" v-model="rateService.rating" :value="2" />
                         <label for="star2" title="2 stars">★</label>
                         
                         <input type="radio" id="star1" v-model="rateService.rating" :value="1" />
                         <label for="star1" title="1 star">★</label>
                     </div>
                    </div>

                    
                    <div class="mb-3">
                        <label class="form-label">Remarks (optional):</label>
                        <textarea v-model="rateService.remarks" class="form-control"></textarea>
                    </div>
                    <div class="modal-footer">
                        <button type="submit" class="btn btn-primary">Submit Rating</button>
                        <button @click.prevent="showRateServiceForm = false" class="btn btn-secondary">Cancel</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    </div>
     <!---Edit customer form-->
     <div v-show="showEditCustForm" class="modal fade show" style="display: block;" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Edit Customer</h5>
                    <button @click.prevent="showEditCustForm = false" class="btn-close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="updateCustomerProfile(updatecust.cust_email)">
                        <div class="mb-3">
                            <label class="form-label">Email:</label>
                            <input v-model="updatecust.cust_email" type="text" class="form-control" required readonly />
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Address:</label>
                            <input v-model="updatecust.address" type="text" class="form-control" required />
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Pincode:</label>
                            <input v-model="updatecust.pincode" type="text" class="form-control" required />
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Phone:</label>
                            <input v-model="updatecust.phone" type="text" class="form-control" required />
                        </div>
                        <div class="modal-footer">
                            <button type="submit" class="btn btn-primary">Save Changes</button> 
                            <button @click.prevent="showEditCustForm = false" class="btn btn-secondary">Cancel</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

    </div>
</template>

<script>
import CustBar from '../components/CustBar.vue';
import axios from 'axios';
export default {
  props: ['email'],
  name: 'CustDash',
components: { CustBar },
data() {
    return {
      cust_data: [],
      showEditCustForm: false,
      updatecust: {
        cust_email: '',
        address: '',
        phone: '',
        pincode: ''
      },
      service_requests: [],
      showEditServiceForm: false, 
      editedService: {
        sevreq_id: '',
        prof_email: '',
        date_of_request: '',
        date_of_completion: '',
        sev_status:'',
        remarks: '', } ,     
      showRateServiceForm: false,
      rateService: {
        sevreq_id: '',
        prof_email: '',
        cust_email: '',
        sev_status: '',
        remarks: '',
        rating: '',
        sev_id: ''
      },                      
    };
    },
created() {
    this.fetchServiceRequests();
    this.fetchCust();
},    
mounted() {
    console.log('CustDashboard received email:', this.email);
},
methods: {
    async fetchServiceRequests() {
        try {
          let your_jwt_token = localStorage.getItem('jwt');
          if (!your_jwt_token) {
            throw new Error('JWT token is missing');
          }
           const response = await axios.get(`http://127.0.0.1:8080/api/cust_service_requests/${this.email}`,{
      headers: {
        'Authorization': `Bearer ${your_jwt_token}` 
      },
      withCredentials: true
    });
           if (response.status === 200) {
             this.service_requests = response.data; 
             console.log("Service requests fetched successfully:", this.service_requests);
           } else {
             console.error("Failed to fetch service requests:", response.data.error);
           }
        } catch (error) {
           console.error('Error fetching service requests:', error.message);
        }
    },  
    openEditServiceForm(service) {
      this.showEditServiceForm = true; 
      this.editedService = { ...service }; 
    },
    openUpdateCustForm(cust){
      this.showEditCustForm = true;
    },
    async fetchCust() {
          try {
                let your_jwt_token = localStorage.getItem('jwt');
                if (!your_jwt_token) throw new Error('JWT token is missing');
                
                const response = await axios.get(`http://127.0.0.1:8080/api/customer/${this.email}`, {
                  headers: { 'Authorization': `Bearer ${your_jwt_token}` },
                  withCredentials: true
                });
                if (response.status === 200) {
                  this.cust_data = response.data;
                  console.log("Customer data fetched successfully:", this.cust_data);
                  this.updatecust = { ...this.cust_data }; 
                } else {
                  console.error("Failed to fetch customer:", response.data.error);
                }
           } catch (error) {
                 console.error('Error fetching customer:', error.message);
        }
},

async updateCustomerProfile() {
    try {
        let your_jwt_token = localStorage.getItem('jwt');
        if (!your_jwt_token) {
            throw new Error('JWT token is missing');
        }
        const response = await axios.put(`http://127.0.0.1:8080/api/update_customer/${this.email}`, {
            "cust_email": this.updatecust.cust_email,
            "address": this.updatecust.address,
            "pincode": this.updatecust.pincode,
            "phone": this.updatecust.phone
        }, {
            headers: {
                'Authorization': `Bearer ${your_jwt_token}`
            },
            withCredentials: true
        });
        
        if (response.status === 200) {
            console.log("Customer profile updated successfully:", response.data);
            this.fetchCust();
            this.showEditCustForm = false;
            const updatedCust = response.data.customer;
            const index = this.cust_data.findIndex(cust => cust.cust_email === this.email);
            if (index !== -1) {
                this.cust_data[index] = { ...updatedCust };
            }
            this.showEditCustForm = false;
            this.updatecust = { 
                cust_email: '',
                address: '',
                phone: '',
                pincode: ''
            };
            location.reload();
        } else {
            console.error("Failed to update customer profile:", response.data.error);
        }
    } catch (error) {
        console.error('Error updating customer profile:', error.message);
    }
},
    async editService(sevreq_id) {
      try { 
        let your_jwt_token = localStorage.getItem('jwt');
        if (!your_jwt_token) {
          throw new Error('JWT token is missing');
        }
        const response = await axios.post(`http://127.0.0.1:8080/api/edit_sevreq/${sevreq_id}/${this.email}`, {
          "sevreq_id": this.editedService.sevreq_id,
          "prof_email": this.editedService.prof_email,
          "date_of_request": this.editedService.date_of_request,
          "date_of_completion": this.editedService.date_of_completion,
          "sev_status": this.editedService.sev_status,
          "remarks": this.editedService.remarks,
          "cust_email": this.email
        },{
      headers: {
        'Authorization': `Bearer ${your_jwt_token}` 
      },
      withCredentials: true
    });
        if (response.status === 200) {
          console.log("Service request updated successfully:", response.data);
          this.fetchServiceRequests();
          this.showEditServiceForm = false;
           // Update the local services array with the updated service data from the backend
           const updatedService = response.data.service_requests;
           const index = this.service_requests.findIndex(service_request=> service_request.sevreq_id === sevreq_id);
           if (index !== -1) {
             // Replace the old service data with the updated one from the backend
             this.service_requests[index] = { ...updatedService_Request };
           }
           // Clear and close the edit form
           this.showEditServiceForm = false;
           this.editedService = { // Reset editedService
            sevreq_id: '',
            cust_email: '',
            prof_email: '',
            date_of_request: '',
            date_of_completion: '',
            sev_status:'',
            remarks: '', 
           };
           location.reload();
        } else {
          console.error("Failed to update service request:", response.data.error);
        }
      } catch (error) {
        console.error("Error updating service request:", error.message);
      }
    },
    async deleteService(sevreq_id) {
      if (confirm("Are you sure you want to delete this service request?")) {
        try {
          let your_jwt_token = localStorage.getItem('jwt');
          if (!your_jwt_token) {  
            throw new Error('JWT token is missing');
          }
          const response = await axios.delete(`http://127.0.0.1:8080/api/delete_sevreq/${sevreq_id}`,
          {
      headers: {
        'Authorization': `Bearer ${your_jwt_token}` 
      },
      withCredentials: true
    }
          );
          if (response.status === 200) {
            console.log("Service request deleted successfully:", response.data);
            this.service_requests = this.service_requests.filter(service_request => service_request.sevreq_id !== sevreq_id);
          } else {
            alert("Failed to delete service request: " + response.data.error);
          }
        } catch (error) {
          console.error("Error deleting service request:", error.message);
          alert("An error occurred while deleting the service request.");
        }
      }
    },
    navigateToCategory(category) {
      this.$router.push({ path: `/services/${category}`, query: { email: this.email } });
    },
    async closeServiceRequest(sevreq_id) {
      try {
        let your_jwt_token = localStorage.getItem('jwt');
      if (!sevreq_id) {
        console.error("Service request ID is undefined");
        return;
      }         
      const response = await axios.post(`http://127.0.0.1:8080/api/close_sevreq/${sevreq_id}`,{},{
      headers: {
        'Authorization': `Bearer ${your_jwt_token}` 
      },
      withCredentials: true
    });

      if (response.status === 200) {  // Check if the update was successful
        console.log("Service request closed successfully:", response.data);
        location.reload();

      } else {          
        console.error("Failed to close service request: " + response.data.error);
      }
    } catch (error) {
      console.error('Error closing service request:', error.message);
    } 
    },
    async openRateServiceForm(service) {
      this.showRateServiceForm= true; 
      this.rateService = { ...service }; 
    },
    async ratedService(sevreq_id) {
      try {
        let your_jwt_token = localStorage.getItem('jwt');
        const response = await axios.post(`http://127.0.0.1:8080/api/rate_sevreq/${sevreq_id}`,{
                    "sevreq_id": this.rateService.sevreq_id,
                    "prof_email": this.rateService.prof_email,
                    "cust_email": this.rateService.cust_email,
                    "rating": this.rateService.rating,
                    "sev_status": this.rateService.sev_status,
                    "remarks": this.rateService.remarks,
                    "sev_id": this.rateService.sev_id},{
      headers: {
        'Authorization': `Bearer ${your_jwt_token}` 
      },
      withCredentials: true
    });
        if (response.status === 200) {
          console.log("Service request rated successfully:", response.data);
           await this.fetchServiceRequests();
          this.showRateServiceForm = false;
          this.rateService={
            sevreq_id: '',
            sev_id: '',
            prof_email: '',
            cust_email: '',
            sev_status: '',
            remarks: '',
            rating: '',
          };
          location.reload();
        } else {
          console.error("Failed to rate service request: " + response.data.error);
        }
      } catch (error) {
        console.error("Error rating service request:", error.message);
      }
   }
  }
}
</script>

  <!-- IMPORTANT background color #3b0a03 rgb(205, 176, 132); -->
<style> 
  body{background-color:#282828;}
  .custbody {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 20px;
      text-align: center;
  }
  
  .container {
      max-width: 1200px;
      margin: 0 auto;
  }
  h1 {
      font-size: 36px;
      margin-bottom: 10px;
  }
  .services {
      display: flex;
      justify-content: space-around;
      margin-top: 20px;
  }
  .service-card {
      background-color: #fff;
      border-radius: 10px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      width: 200px;
      padding: 20px;
      text-align: center;
      position: relative;
  }
  .service-card img {
      width: 150px;
      height: 150px;
      margin-bottom: 10px;
  }
  .service-card h3 {
      font-size: 18px;
      margin: 10px 0;
  }
  .badge {
      background-color: #f39c12;
      color: white;
      font-size: 12px;
      padding: 5px 10px;
      border-radius: 20px;
      position: absolute;
      top: -10px;
      right: -10px;
  }
  .btn-violet {
  background-color: #8a2be2; /* Violet color */
  color: white;
  border: none;
}
.white{color:white}
.btn-violet:hover {
  background-color: #7a1bcf; /* Darker shade on hover */
}
.yellow{color:yellow}
.star-rating {direction: rtl;
                  display: inline-flex;
                color:white}

.star-rating input[type="radio"] {
    display: none;}
.star-rating label {
    font-size: 2rem;
    color: #d5c810;
    cursor: pointer;
    position: relative;
    padding: 0 1rem; /* Add padding to create space between stars */

}
.star-rating label::before {
    content: "\2605"; /* Unicode star character */
    position: absolute;
}
.star-rating input[type="radio"]:checked ~ label {
    color: #f5b301;
}
.star-rating label:hover,
.star-rating label:hover ~ label,
.star-rating input[type="radio"]:checked ~ label:hover,
.star-rating input[type="radio"]:checked ~ label:hover ~ label,
.star-rating input[type="radio"]:checked ~ label:hover ~ input[type="radio"]:checked ~ label {
    color: #f5b301;}

</style>
<template>
    <div class="container">
        <header>
        <CustBar :email="email"/>
        <h2>Welcome Customer</h2>
        <p>Your email: {{ email }}</p>
        </header>
        <h1>Cleaning Services</h1> 
        <div class="rating">
            <span class="star">★</span> 4.9 (3.4M bookings near you)
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
                <img src="/static/iron.jpeg" alt="Home Maintenance Services">
                <h3>Home Maintenance Services</h3>
            </div>

            <div class="service-card" @click="navigateToCategory('Cleaning and Organization Services')">
                <div class="badge">Trending Now</div>
                <img src="/static/homeorg.jpeg"  alt="Cleaning and Organization Services">
                <h3>Cleaning and Organization Service</h3>
            </div>
        </div>

      <!-- Service Requests Table -->
      <section class="mb-5">
        <h3>HISTORY: Service Requests</h3>
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
              <td>
                <div class="d-flex">
                    <button v-if="service_request.sev_status === 'requested' || service_request.sev_status === 'accepted'"
                     @click.prevent="closeServiceRequest(service_request.sevreq_id)"class="btn btn-info btn-sm mr-5">Close</button>
        
                    <button v-else-if="service_request.sev_status === 'closed'"
                     @click.prevent="rateServiceRequest(service_request.sevreq_id)" class="btn btn-violet btn-sm mr-5">Rate</button>
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
      <!-- Rate Service Modal -->
<div class="modal fade" id="rateModal" tabindex="-1" role="dialog" aria-labelledby="rateModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="rateModalLabel">Service Remarks</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <h5>Request ID: {{ selectedServiceRequest.sevreq_id }}</h5>
        <div class="form-group">
          <label>Service Name</label>
          <input type="text" class="form-control" v-model="selectedServiceRequest.service_name" readonly>
        </div>
        <div class="form-group">
          <label>Description</label>
          <input type="text" class="form-control" v-model="selectedServiceRequest.description" readonly>
        </div>
        <div class="form-group">
          <label>Professional ID</label>
          <input type="text" class="form-control" v-model="selectedServiceRequest.professional_id" readonly>
        </div>
        <div class="form-group">
          <label>Professional Name</label>
          <input type="text" class="form-control" v-model="selectedServiceRequest.professional_name" readonly>
        </div>
        <div class="form-group">
          <label>Service Rating:</label>
          <div>
            <span v-for="star in 5" :key="star" @click="setRating(star)" 
                  :class="{'text-warning': star <= rating, 'text-muted': star > rating}">
              &#9733;
            </span>
          </div>
        </div>
        <div class="form-group">
          <label>Remarks (if any):</label>
          <textarea class="form-control" v-model="remarks"></textarea>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" @click="submitRating">Submit</button>
      </div>
    </div>
  </div>
</div>
      <!-- Edit Service Form Modal -->
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
                            <select v-model="editedService.sev_status" type="text" class="form-control" required >
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
      service_requests: [],
      showEditServiceForm: false, 
      editedService: {
        sevreq_id: '',
        prof_email: '',
        date_of_request: '',
        date_of_completion: '',
        sev_status:'',
        remarks: '', 
      } ,     
      selectedServiceRequest: {},
      rating: 0,
      remarks: ""                       
    };
    },
  created() {
    this.fetchServiceRequests();},    
    mounted() {
    console.log('CustDashboard received email:', this.email); },
    methods: {
        async fetchServiceRequests() {
        try {
           const response = await axios.get('http://127.0.0.1:8080/api/service_requests');
           if (response.status === 200) {
             this.service_requests = response.data; 
           } else {
             console.error("Failed to fetch service requests:", response.data.error);
           }
        } catch (error) {
           console.error('Error fetching service requests:', error.message);
        }
    },
    openEditServiceForm(service) {
      this.showEditServiceForm = true; // Show the edit form
      this.editedService = { ...service }; // Populate the form with selected service data
    },
    async editService(sevreq_id) {
      try {
        const response = await axios.post(`http://127.0.0.1:8080/api/edit_sevreq/${sevreq_id}/${this.email}`, {
          "sevreq_id": this.editedService.sevreq_id,
          "prof_email": this.editedService.prof_email,
          "date_of_request": this.editedService.date_of_request,
          "date_of_completion": this.editedService.date_of_completion,
          "sev_status": this.editedService.sev_status,
          "remarks": this.editedService.remarks,
          "cust_email": this.email
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
          const response = await axios.delete(`http://127.0.0.1:8080/api/delete_sevreq/${sevreq_id}`);
          if (response.status === 200) {
            console.log("Service request deleted successfully:", response.data);
            this.service_requests = this.service_requests.filter(service_request => service_request.sevreq_id !== sevreq_id);
            alert("Service request deleted successfully");
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
      if (!sevreq_id) {
        console.error("Service request ID is undefined");
        return;
      }         
      const response = await axios.post(`http://127.0.0.1:8080/api/close_sevreq/${sevreq_id}`);

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
  async rateServiceRequest(sevreq_id) {
    this.selectedServiceRequest = service_request;
    this.rating = 0;
    this.remarks = "";
    $('#rateModal').modal('show'); // This line uses jQuery to show the modal
  },
  setRating(star) {
    this.rating = star;
  },
  submitRating() {
    // Submit the rating and remarks for the selected service request
    console.log("Service ID:", this.selectedServiceRequest.sevreq_id);
    console.log("Rating:", this.rating);
    console.log("Remarks:", this.remarks);
    
    // Add your code to save the rating and remarks here

    // Close the modal after submission
    $('#rateModal').modal('hide');
  }
  }
}
</script>

  
  <style>
  body {
      font-family: Arial, sans-serif;
      background-color: rgb(205, 176, 132);
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
  .rating {
      font-size: 18px;
      color: #666;
  }
  .rating .star {
      color: #f4c150;
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
      width: 60px;
      height: 60px;
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
.btn-violet:hover {
  background-color: #7a1bcf; /* Darker shade on hover */
}

</style>
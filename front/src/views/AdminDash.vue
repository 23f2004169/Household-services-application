<template>
  <div class="adminbody">
    <div class="container mt-0">
      <header class="d-flex justify-content-between align-items-center mb-4">
        <MenuBar />
      </header>
    </div>

    <main>
      <!-- Services Table -->
      <section class="mb-5">
        <h3 class="white">Services</h3>
        <button @click.prevent="showNewServiceForm = true" class="red ">
          <b>+ New Service</b>
        </button>
        <div>
          <table class="table table-striped table-hover">
            <thead class="thead-dark">
              <tr>
                <th>ID</th>
                <th>Service Name</th>
                <th>Base Price</th>
                <th>Service Category</th>
                <th>Time Required</th>
                <th>Description</th>
                <th>Address</th>
                <th>Pincode</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(service, index) in services" :key="index">
                <td>{{ service.sev_id }}</td>
                <td>{{ service.sev_name }}</td>
                <td>{{ service.price }}</td>
                <td>{{ service.category }}</td>
                <td>{{ service.time_req }}</td>
                <td>{{ service.description }}</td>
                <td>{{ service.address }}</td>
                <td>{{ service.pincode }}</td>
                <td>
                  <div class="d-flex">
                    <button @click.prevent="openEditServiceForm(service)"
                      class="btn btn-warning btn-sm mr-2">Edit</button>
                    <button @click.prevent="deleteService(service.sev_id)" class="btn btn-danger btn-sm">Delete</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Professionals Table -->
      <section class="mb-5">
        <h3 class="white">Professionals</h3>
        <table class="table table-striped table-hover">
          <thead class="thead-dark">
            <tr>
              <th>ID</th>
              <th>Description</th>
              <th>Experience (Yrs)</th>
              <th>Service Name</th>
              <th>Approval</th>
              <th>Blocked</th>
              <th>Profile doc</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(professional, index) in professionals" :key="index">
              <td>{{ professional.prof_email }}</td>
              <td>{{ professional.description }}</td>
              <td>{{ professional.experience }}</td>
              <td>{{ professional.service_type }}</td>
              <td>{{ professional.approval }}</td>
              <td>{{ professional.blocked }}</td>
              <td><button @click="viewDocument(professional.prof_email)" class="btn btn-primary btn-sm">View</button> </td>
              <td>
                <div class="d-flex">
                  <button  v-if="professional.approval === 'rejected' || professional.approval==='pending'" @click="approveProfessional(professional.prof_email)"
                    class="btn btn-success btn-sm">Approve</button>
                  <button v-else-if="professional.approval === 'approved'" @click="rejectProfessional(professional.prof_email)"
                    class="btn btn-danger btn-sm">Reject</button>
                  <button @click="blockProfessional(professional.prof_email)"
                    class="btn btn-dark btn-sm">Block/Unblock</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- Service Requests Table -->
      <section class="mb-5">
        <h3 class="white">Service Requests</h3>
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
            </tr>
          </tbody>
        </table>
      </section>
    </main>

    <!-- Edit Service Form Modal -->
    <div v-show="showEditServiceForm" class="modal fade show" style="display: block;" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Edit Service</h5>
            <button @click.prevent="showEditServiceForm = false" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="editService(editedService.sev_id)">

              <div class="mb-3">
                <label class="form-label">Service Name:</label>
                <input v-model="editedService.sev_name" type="text" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Description:</label>
                <textarea v-model="editedService.description" class="form-control" required></textarea>
              </div>

              <div class="mb-3">
                <label class="form-label">Base Price:</label>
                <input v-model="editedService.price" type="number" class="form-control" required />
              </div>

              <div class="mb-3">
                <label for="category" class="form-label">Category:</label>
                <select v-model="editedService.category" name="category" id="category" class="form-control" required>
                  <option value="" disabled>Select a category</option>
                  <option value="Home Maintenance Services">Home Maintenance Services</option>
                  <option value="Cleaning and Organization Services">Cleaning and Organization Services</option>
                  <option value="Child_Elderly Care Services">Child_Elderly Care Services</option>
                  <option value="Lifestyle and Convenience Services">Lifestyle and Convenience Services</option>
                </select>
              </div>

              <div class="mb-3">
                <label class="form-label">Time Required:</label>
                <input v-model="editedService.time_req" type="text" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Address:</label>
                <input v-model="editedService.address" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Pincode:</label>
                <input v-model="editedService.pincode" type="number" class="form-control" required />
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

    <!-- New Service Form Modal -->
    <div v-show="showNewServiceForm" class="modal fade show" style="display: block;" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal title">New Service</h5>
            <button @click.prevent="showNewServiceForm = false" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addNewService">
              <div class="mb-3">
                <label class="form-label">Service Name:</label>
                <input v-model="newService.sev_name" type="text" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Description:</label>
                <textarea v-model="newService.description" class="form-control" required></textarea>
              </div>

              <div class="mb-3">
                <label class="form-label">Base Price:</label>
                <input v-model="newService.price" type="number" class="form-control" required />
              </div>

              <div class="mb-3">
                <label for="category" class="form-label">Category:</label>
                <select v-model="newService.category" name="category" id="category" class="form-control" required>
                  <option value="" disabled>Select a category</option>
                  <option value="Home Maintenance Services">Home Maintenance Services</option>
                  <option value="Cleaning and Organization Services">Cleaning and Organization Services</option>
                  <option value="Child_Elderly Care Services">Child_Elderly Care Services</option>
                  <option value="Lifestyle and Convenience Services">Lifestyle and Convenience Services</option>
                </select>
              </div>

              <div class="mb-3">
                <label class="form-label">Time Required in minutes:</label>
                <input v-model="newService.time_req" type="text" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Address:</label>
                <input v-model="newService.address" type="text" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Pincode:</label>
                <input v-model="newService.pincode" type="number" class="form-control" required />
              </div>
              <div class="modal-footer">
                <button type="submit" class="btn btn-primary">Add Service</button>
                <button @click.prevent="showNewServiceForm = false" class="btn btn-secondary">Cancel</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import MenuBar from '../components/MenuBar.vue';
import axios from 'axios';

export default {
  name: 'AdminDash',
  data() {
    return {
      services: [],
      professionals: [],
      service_requests: [],
      showNewServiceForm: false, // Controls the visibility of the new service form modal
      showEditServiceForm: false, // Controls the visibility of the edit service form modal
      newService: {
        sev_name: '',
        description: '',
        price: '',
        time_req: '',
        address: '',
        category: '',
        pincode: ''
      },
      editedService: { // Holds the service being edited
        sev_id: '',
        sev_name: '',
        description: '',
        price: '',
        time_req: '',
        address: '',
        category: '',
        pincode: ''
      }
    };
  },
  components: { MenuBar },
  created() {
    this.fetchServices();
    this.fetchProfessionals();
    this.fetchServiceRequests();
  },
    methods: {
      async fetchServices() {
        try {
          let your_jwt_token = localStorage.getItem('jwt');
          if (!your_jwt_token) {
              throw new Error('JWT token is missing');
          }
          const response = await axios.get(`http://127.0.0.1:8080/api/services`, {
            headers: {
              Authorization: `Bearer ${ your_jwt_token }`
          },
        withCredentials: true
      });
      if(response.status === 200) {
        this.services = response.data; // Update the services array with the data from the backend
        console.log("Services fetched successfully:", response.data);
}     else {
         console.error("Failed to fetch services:", response.data.error);
}
      } 
      catch (error) {
  console.error('Error fetching services:', error.message);
}
    },
    async addNewService() {
  try { 
    let your_jwt_token = localStorage.getItem('jwt');
    if (!your_jwt_token) {
      throw new Error('JWT token is missing');
    }
    const response = await axios.post('http://127.0.0.1:8080/api/create_sev', {
      "sev_name": this.newService.sev_name,
      "description": this.newService.description,
      "price": this.newService.price,
      "time_req": this.newService.time_req,
      "category": this.newService.category,
      "address": this.newService.address,
      "pincode": this.newService.pincode
    }, {
      headers: {
        Authorization: `Bearer ${ your_jwt_token }`
      },
      withCredentials: true
    });

    // If the response is successful, add the new service to the list and close the modal
    if (response.status === 201) {
      console.log("Service added successfully:", response.data);
      await this.fetchServices();

      this.services.push({
        ...this.newService,
        id: response.data.service_id // Assuming the backend returns the new service's ID
      });

      // Clear the new service form
      this.newService = {
        sev_name: '',
        description: '',
        price: '',
        time_req: '',
        address: '',
        category: '',
        pincode: ''
      };

      // Close the modal
      this.showNewServiceForm = false;
      location.reload();

    } else {
      alert("Failed to add service: " + response.data.error);
    }
  } catch (error) {
    console.error('Error adding new service:', error.message);
    alert('An error occurred while adding the service.');
  }
},
openEditServiceForm(service) { 
  this.showEditServiceForm = true; // Show the edit form
  this.editedService = { ...service }; // Populate the form with selected service data
},
    async editService(sev_id) {
  if (!sev_id) {
    console.error("Service ID is undefined");
    return;
  }
  try { 
    let your_jwt_token = localStorage.getItem('jwt');
    if (!your_jwt_token) {
      throw new Error('JWT token is missing');
    }
    const response = await axios.post(`http://127.0.0.1:8080/api/edit_sev/${sev_id}`, {
      "sev_name": this.editedService.sev_name,
      "description": this.editedService.description,
      "price": this.editedService.price,
      "time_req": this.editedService.time_req,
      "category": this.editedService.category,
      "address": this.editedService.address,
      "pincode": this.editedService.pincode
    } , {
      headers: {
        Authorization: `Bearer ${ your_jwt_token }`
      },
      withCredentials: true
    });

    if (response.status === 200) { // Check if the update was successful
      console.log("Service updated successfully:", response.data);

      // Update the local services array with the updated service data from the backend
      const updatedService = response.data.service;

      const index = this.services.findIndex(service => service.sev_id === sev_id);
      if (index !== -1) {
        // Replace the old service data with the updated one from the backend
        this.services[index] = { ...updatedService };
      }

      // Clear and close the edit form
      this.showEditServiceForm = false;
      this.editedService = { // Reset editedService
        sev_id: '',
        sev_name: '',
        description: '',
        price: '',
        time_req: '',
        address: '',
        category: '',
        pincode: ''
      };
      location.reload();
    } else {
      alert("Failed to update service: " + response.data.error);
    }
  } catch (error) {
    console.error('Error updating service:', error.message);
    alert('An error occurred while updating the service.');
  }
},
    async deleteService(sev_id) {
  if (confirm("Are you sure you want to delete this service?")) {
    try {
      let your_jwt_token = localStorage.getItem('jwt');
      if (!your_jwt_token) {
        throw new Error('JWT token is missing');
      }
      const response = await axios.delete(`http://127.0.0.1:8080/api/delete_sev/${sev_id}`,
      {
        headers: {
          Authorization: `Bearer ${ your_jwt_token }`
        },
        withCredentials: true
      }
      );
      if (response.status === 200) {
        console.log("Service deleted successfully:", response.data);
        this.services = this.services.filter(service => service.sev_id !== sev_id);
      } else {
        alert("Failed to delete service: " + response.data.error);
      }
    } catch (error) {
      console.error("Error deleting service:", error.message);
      alert("An error occurred while deleting the service.");
    }
  }
},
    async fetchProfessionals() {
  try {
    let your_jwt_token = localStorage.getItem('jwt');
    if (!your_jwt_token) {
      throw new Error('JWT token is missing');
    }
    const response = await axios.get('http://127.0.0.1:8080/api/professionals', {
      headers: {
        'Authorization': `Bearer ${your_jwt_token}` 
      } ,
      withCredentials: true
    });

    if (response.status === 200) {
      this.professionals = response.data; // Update the services array with the data from the backend
    } else {
      console.error("Failed to fetch professionals:", response.data.error);
    }
  } catch (error) {
    console.error('Error fetching professionals:', error.message);
  }
},
  async approveProfessional(prof_email) {
  try {
    let your_jwt_token = localStorage.getItem('jwt');
    console.log(your_jwt_token);
    console.log("Professional email ", prof_email);
    const response = await axios.post(`http://127.0.0.1:8080/api/professional/approve/${prof_email}`,{},
    { 
      headers: {
        'Authorization': `Bearer ${your_jwt_token}` 
      },      
      withCredentials: true
    });
    if (response.status === 200) {  // Check if the update was successful
      console.log("Professional approved successfully:", response.data);
      location.reload();

    } else {
      console.error("Failed to approve professional: " + response.data.error);
    }
  } catch (error) {
    console.error('Error approving professional:', error.message);
  }
},
    async rejectProfessional(prof_email) {
  try {
    let your_jwt_token = localStorage.getItem('jwt');
    if (!your_jwt_token) {  
      throw new Error('JWT token is missing');
    }
    console.log("Professional email ", prof_email);
    const response = await axios.post(`http://127.0.0.1:8080/api/professional/reject/${prof_email}`,{},
    {
      headers: {
        'Authorization': `Bearer ${your_jwt_token}` 
      },
      withCredentials: true
    }
    );

    if (response.status === 200) {  // Check if the update was successful
      console.log("Professional rejected successfully:", response.data);
      location.reload();

    } else {
      console.error("Failed to reject professional: " + response.data.error);
    }
  } catch (error) {
    console.error('Error rejecting professional:', error.message);
  }
},
  async blockProfessional(prof_email) {
  try { 
    let your_jwt_token = localStorage.getItem('jwt');
    if (!your_jwt_token) {
      throw new Error('JWT token is missing');
    }
    console.log("Professional email ", prof_email);
    const response = await axios.post(`http://127.0.0.1:8080/api/professional/block/${prof_email}`,
    {},
    {
      headers: {
        'Authorization': `Bearer ${your_jwt_token}` 
      },
      withCredentials: true
    }
    );

    if (response.status === 200) {  // Check if the update was successful
      console.log("Professional blocked successfully:", response.data);
      location.reload();

    } else {
      console.error("Failed to block professional: " + response.data.error);
    }
  } catch (error) {
    console.error('Error blocking professional:', error.message);
  }
},
  async fetchServiceRequests() {
  try {
    let your_jwt_token = localStorage.getItem('jwt');
    if (!your_jwt_token) {
      throw new Error('JWT token is missing');
    }
    const response = await axios.get('http://127.0.0.1:8080/api/service_requests',
    {
      headers: {
        'Authorization': `Bearer ${your_jwt_token}` 
      },      
      withCredentials: true
    }
    );
    if (response.status === 200) {
      this.service_requests = response.data; // Update the services array with the data from the backend
      console.log("Service requests fetched successfully:", response.data);
    } else {
      console.error("Failed to fetch service requests:", response.data.error);
    }
  } catch (error) {
    console.error('Error fetching service requests:', error.message);
  }
},
viewDocument(prof_email) {
      // Open document in new tab
      const documentUrl = `http://127.0.0.1:8080/api/view-document/${prof_email}`;
      window.open(documentUrl, '_blank');
    }
}
}
</script>

<style>
.adminbody {
  font-family: Arial, sans-serif;
  background-color: #282828;
  margin: 0;
  padding: 20px;
  text-align: center;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;

}

table {
  width: 90%;
  max-width: 1200px;
  border-collapse: collapse;
  margin: 20px auto;
  font-size: 1.1em;
}

table,
th,
td {
  border: 1px solid #ddd;
}

th,
td {
  padding: 8px;
  text-align: left;
}

.add-service-btn {
  margin-bottom: 10px;
}

.new-service-form {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  padding: 20px;
  background-color: #fff;
  border: 1px solid #ddd;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.form-actions {
  margin-top: 10px;
}

button {
  margin-right: 10px;
}

.red {
  background-color: rgb(63, 35, 18);
  color: white
}

.white {
  color: white
}
</style>
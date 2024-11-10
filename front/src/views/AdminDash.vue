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
    <div class="table-container">
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
              <th>Export</th>
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
                  <button  @click="approveProfessional(professional.prof_email)" class="btn btn-success btn-sm">Approve</button>
                  <button  @click="rejectProfessional(professional.prof_email)" class="btn btn-danger btn-sm">Reject</button>
                </div>
                <br>
                <div class="d-flex">
                  <button @click="blockProfessional(professional.prof_email)" class="btn btn-dark btn-sm">Block/Unblock</button>
                </div>
              </td>
              <td><button @click="exportProfessional(professional.prof_email)" class="btn btn-secondary btn-sm">Export</button></td>
            </tr>
          </tbody>
        </table>
      </div>

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
              <th>Service status</th>
              <th>Service ID</th>
              <th>Rating</th>
              <th>Status (R/A/C)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="( service_request, index) in service_requests" :key="index">
              <td>{{ service_request.sevreq_id }}</td>
              <td>{{ service_request.prof_email }}</td>
              <td>{{ service_request.cust_email }}</td>
              <td>{{ service_request.date_of_request }}</td>
              <td>{{ service_request.date_of_completion }}</td>
              <td>{{ service_request.sev_status }}</td>
              <td>{{ service_request.sev_id }}</td>
              <td>{{ service_request.rating }}</td>
              <td v-if ="service_request.sev_status === 'accepted'"><div class="btn btn-success">Accepted</div></td>
              <td v-else-if="service_request.sev_status === 'rejected'"><div class="btn btn-danger">Rejected</div></td>
              <td v-else-if="service_request.sev_status === 'requested'"><div class="btn btn-primary">Requested</div></td>
              <td v-else><div class="btn btn-warning">Closed</div></td>
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
    
    <!-- <div v-if="isDownloading" class="download-overlay">
      <div class="download-spinner">
        <span>Downloading...</span>
      </div>
    </div>
    <div> -->
    

    <div>
    <div v-if="isExporting || isDownloading" class="loading-overlay">
      <div class="loading-content">
        <div class="spinner"></div>
        <span>{{ isExporting ? 'Preparing CSV export...' : 'Downloading CSV...' }}</span>
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
  mounted() {
  //   console.log("AdminDash mounted");
  //   const source = new EventSource( "http://127.0.0.1:8080/stream");
  //       source.addEventListener('notifyadmin', event => {
  //         let data = JSON.parse(event.data);
  //         alert(<a href="http://127.0.0.1:8080/api/reports/"+ data.filename)</a>); 
  //         // # this.notifications.push(data);
  //         // start downloading data.message.link
  //         console.log("Received notification:", data);
  //       }, false);

  // },
//     console.log("AdminDash mounted");
    
//     const source = new EventSource("http://127.0.0.1:8080/stream");
    
//     source.onerror = (error) => {
//         console.error("EventSource failed:", error);
//         source.close();
//     };

//     source.addEventListener('notifyadmin', event => {
//         try {
//             const data = JSON.parse(event.data);
//             const sanitizedFilename = encodeURIComponent(data.filename);
//             const reportUrl = `http://127.0.0.1:8080/api/reports/${sanitizedFilename}`;
            
//             this.downloadDocument(reportUrl, data.filename);
//             console.log("Received notification:", data);
//         } catch (error) {
//             console.error("Error processing notification:", error);
//         }
//     }, false);
// },

console.log("AdminDash mounted");
    
    const source = new EventSource("http://127.0.0.1:8080/stream");
    
    source.onerror = (error) => {
        console.error("EventSource failed:", error);
        source.close();
    };

    source.addEventListener('notifyadmin', event => {
        try {
            const data = JSON.parse(event.data);
            const sanitizedFilename = encodeURIComponent(data.filename);
            const reportUrl = `http://127.0.0.1:8080/api/reports/${sanitizedFilename}`;
            
            // Show confirmation with options
            // console.log("beofre")
            // if (confirm(`New report available: ${data.filename}\nClick OK to download, Cancel to view in browser`)) {
                // this.downloadDocument(reportUrl, data.filename);
            // } else {
                // this.viewcsvDocument(reportUrl);
            // }

            this.downloadDocument(reportUrl, data.filename);

            console.log("Received notification:", data);
        } catch (error) {
            console.error("Error processing notification:", error);
        }
    }, false);
},
data() {
    return {
      services: [],
      professionals: [],
      service_requests: [],
      showNewServiceForm: false, // Controls the visibility
      showEditServiceForm: false, 
      newService: {
        sev_name: '',
        description: '',
        price: '',
        time_req: '',
        address: '',
        category: '',
        pincode: ''
      },
      editedService: { 
        sev_id: '',
        sev_name: '',
        description: '',
        price: '',
        time_req: '',
        address: '',
        category: '',
        pincode: ''
      },
      isDownloading: false,
      isExporting: false
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
        this.services = response.data; 
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

    if (response.status === 201) {
      console.log("Service added successfully:", response.data);
      await this.fetchServices();

      this.services.push({
        ...this.newService,
        id: response.data.service_id 
      });

      this.newService = {
        sev_name: '',
        description: '',
        price: '',
        time_req: '',
        address: '',
        category: '',
        pincode: ''
      };

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
  this.showEditServiceForm = true; 
  this.editedService = { ...service }; 
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

    if (response.status === 200) {
      console.log("Service updated successfully:", response.data);

      const updatedService = response.data.service;

      const index = this.services.findIndex(service => service.sev_id === sev_id);
      if (index !== -1) {
        this.services[index] = { ...updatedService };
      }

      this.showEditServiceForm = false;
      this.editedService = { 
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
      const documentUrl = `http://127.0.0.1:8080/api/view-document/${prof_email}`;
      window.open(documentUrl, '_blank');
    },
async exportProfessional(prof_email) {
        try {
            let your_jwt_token = localStorage.getItem('jwt');
            if (!your_jwt_token) {
                throw new Error('JWT token is missing');
            }
            const response = await axios.post(`http://127.0.0.1:8080/api/export-professional/${prof_email}`,
                {},
                { headers: {
                        'Authorization': `Bearer ${your_jwt_token}` 
                    },
                    withCredentials: true
                }
            );
            if (response.status === 202) {
                console.log("Export started successfully:", response.data);
            }
            alert('Export started. You will be notified once the export is done.');
        } catch (error) {
            console.error('Error triggering export:', error);
        }
    },
async downloadDocument(url, filename) {
      this.isDownloading = true;

      try {
        let your_token = localStorage.getItem('jwt');
        const response = await axios({
          url,
          method: 'GET',
          responseType: 'blob',
          headers: {
            'Authorization': `Bearer ${your_token}`
          },
          onDownloadProgress: (progressEvent) => {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            console.log(`Download Progress: ${percentCompleted}%`);
          }
        });

        // Create blob URL
        const blob = new Blob([response.data], { 
          type: response.headers['content-type'] 
        });
        const downloadUrl = window.URL.createObjectURL(blob);

        // Create download link and trigger download
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = filename;
        document.body.appendChild(link);
        link.click();

        // Cleanup
        document.body.removeChild(link);
        window.URL.revokeObjectURL(downloadUrl);

        this.showNotification(`Downloaded ${filename} successfully`, 'success');

      } catch (error) {
        console.error('Download error:', error);
        this.showNotification(
          `Failed to download ${filename}: ${error.message}`, 
          'error'
        );
      } finally {
        this.isDownloading = false;
      }
    },
showNotification(message, type = 'success') {
        alert(message);
    },
viewcsvDocument(url) {
        try {
            let jwt = localStorage.getItem('jwt');
            if (!jwt) {
                throw new Error('Please login to view the document');
            }

            // Open in new tab with JWT
            const newTab = window.open('about:blank', '_blank');
            newTab.document.write('Loading document...');
            
            // Create form for secure GET request
            const form = document.createElement('form');
            form.method = 'GET';
            form.action = url;
            form.target = '_blank';

            // Add authorization header as hidden input
            const authInput = document.createElement('input');
            authInput.type = 'hidden';
            authInput.name = 'Authorization';
            authInput.value = `Bearer ${jwt}`;
            form.appendChild(authInput);

            // Submit form
            document.body.appendChild(form);
            form.submit();
            document.body.removeChild(form);

        } catch (error) {
            console.error('Error viewing document:', error);
            this.showNotification('Failed to view document: ' + error.message);
        }
},


    
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
  color: white,
}
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.table-container {
            background-color: #282828;
            border-radius: 8px;
            padding: 20px;
  }
  /* Custom text color for table content */
  .table th, .table td {
      border-color: #444444; /* Border color for contrast */
  }
  .table thead th {
      color: #ffffff; /* Header text color */
      background-color: #333333; /* Header background color 
  }
  .table-striped tbody tr:nth-of-type(odd) {
      background-color: #333333; /* Alternate row background color */
  }
  .table-striped tbody tr:nth-of-type(even) {
      background-color: #282828; /* Alternate row background color */
  }
  .table-striped tbody tr:hover {
      background-color: #444444; /* Hovered row background color */
  }
  .table-bordered td, .table-bordered th {
      border-color: #444444; /* Border color for contrast */
  }
  .table-bordered thead td, .table-bordered thead th {
      border-color: #444444; /* Border color for contrast */
  }
  .table-bordered thead td, .table-bordered thead th {
      border-color: #444444; /* Border color for contrast */
  }
  .table-bordered thead th {
      color: #ffffff; /* Header text color */
  }
  .download-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.download-spinner {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
                
</style>
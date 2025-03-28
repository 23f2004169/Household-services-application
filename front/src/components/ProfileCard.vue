<template>
    <div class="profile-card">
      <img :src="'http://127.0.0.1:8080/api/view-image/' + prof_data.prof_email" alt="Profile Picture" class="profile-pic" />
      <p class="service">Service: {{ prof_data.service_type }}</p>
      <p class="email">Email: {{ prof_data.prof_email }}</p>
      <p class="experience">Experience: {{ prof_data.experience }}</p>
      <p class="address">Address: {{ prof_data.address }}</p>
      <p class="pincode">Pincode: {{ prof_data.pincode }}</p>
      <p class="description">Description: {{ prof_data.description }}</p>
      <p class="phone" >Phone: {{ prof_data.phone }}</p>
      <button @click="viewDocument(prof_data.prof_email)" class="btn btn-primary btn-sm">View</button> 
      <button @click.prevent="openUpdateProfessionalForm(prof_data)" class="btn btn-warning btn-sm mr-2">Edit Profile</button>
      <div>
      <button v-if="prof_data.approval === 'rejected'" @click="reuploadDocument(prof_data.prof_email)" class="btn btn-dark btn-sm">Reupload Document</button>
      </div>
      <input type="file" ref="documentInput" accept=".pdf" @change="handleFileUpload" style="display:none" />
    </div>

<!-- ------Edit Professional Profile Modal------ -->
  <div v-show="showEditProfessionalForm" class="modal fade show" style="display: block;" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Edit Professional Profile</h5>
          <button @click.prevent="showEditProfessionalForm = false" class="btn-close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="updateProfessionalProfile(updateprof.prof_email)">
            <div class="mb-3">
              <label class="form-label">Email:</label>
              <input v-model="updateprof.prof_email" type="email" class="form-control" required readonly/>
            </div>           
            <div class="row g-3 mt-2">
            <div class="col-12">
              <label class="form-label">Service Type:</label>
              <select v-model="updateprof.service_type" class="form-select form-select-sm" required>
                <option v-for="service in services" :key="service.sev_id" :value="service.sev_name" :selected="service.sev_name === updateprof.service_type">
                  {{ service.sev_name }}
                </option>
              </select>
            </div>
            </div>            
            <div class="mb-3">
              <label class="form-label">Experience (Years):</label>
              <input v-model="updateprof.experience" type="number" class="form-control" required />
            </div>            
            <div class="mb-3">
              <label class="form-label">Address:</label>
              <input v-model="updateprof.address" type="text" class="form-control" required />
            </div>           
            <div class="mb-3">
              <label class="form-label">Pincode:</label>
              <input v-model="updateprof.pincode" type="text" class="form-control" required />
            </div>            
            <div class="mb-3">
              <label class="form-label">Description:</label>
              <textarea v-model="updateprof.description" class="form-control" required></textarea>
            </div>           
            <div class="mb-3">
              <label class="form-label">Phone:</label>
              <input v-model="updateprof.phone" type="text" class="form-control" required />
            </div>
            <div class="modal-footer">
              <button type="submit" class="btn btn-primary">Save Changes</button>
              <button @click.prevent="showEditProfessionalForm = false" class="btn btn-secondary">Cancel</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
    
</template>


<script>
import axios from 'axios'; 
export default {
  name: 'ProfileCard',
  props: ['email'],
  data() {
    return {
      prof_data: [], 
      showEditProfessionalForm: false, 
      updateprof: { 
        prof_email: "",
        service_type: "",
        experience: "",
        address: "",
        pincode: "",
        description: "",
        phone: ""
      },
      services: []
      }
    },
  created() {
    this.fetchProf();
    this.fetchServices();
  },
  methods: {
    openUpdateProfessionalForm(prof) {
      this.showEditProfessionalForm= true;
      this.updateprof= { ...prof }; // Populate with current prof data
    },
  async updateProfessionalProfile(prof_email) {
      try {
        let your_jwt_token = localStorage.getItem('jwt');
      if (!your_jwt_token) {
        throw new Error('JWT token is missing');
      }
      const response = await axios.post(`http://127.0.0.1:8080/api/prof_update/${this.email}`, {
          "prof_email": this.updateprof.prof_email,
          "service_type": this.updateprof.service_type,
          "experience": this.updateprof.experience,
          "address": this.updateprof.address,
          "pincode": this.updateprof.pincode,
          "description": this.updateprof.description,
          "phone": this.updateprof.phone
        }, {
          headers: {
            'Authorization': `Bearer ${your_jwt_token}`
          },
          withCredentials: true
        });

        if (response.status === 200) {
          console.log("Professional profile updated successfully:", response.data);
          this.fetchProf();

          this.showEditProfessionalForm = false;
          this.updateprof = { 
            prof_email: "",
            prof_password: "",
            service_type: "",
            experience: "",
            address: "",
            pincode: "",
            description: "",
            phone: ""
          };
        } else {
          alert("Failed to update service: " + response.data.error);
        }
      } catch (error) {
        console.error('Error updating service:', error.message);
        alert('An error occurred while updating the service.');
      }
    },    
  async fetchProf() {
      try {
        let your_jwt_token = localStorage.getItem('jwt');
        if (!your_jwt_token) {
          throw new Error('JWT token is missing');
        }
        const response = await axios.get(`http://127.0.0.1:8080/api/professional/${this.email}`, {
          headers: {
            'Authorization': `Bearer ${your_jwt_token}`
          },
          withCredentials: true
        });
        if (response.status === 200) {
          this.prof_data = response.data; 
        } else {
          console.error("Failed to fetch professionals:", response.data.error);
        }
      } catch (error) {
        console.error('Error fetching professionals:', error.message);
      }
    },
  async fetchServices() {
      try {
        let your_jwt_token = localStorage.getItem('jwt');
        const response = await axios.get('http://127.0.0.1:8080/api/reg_servicenames',
          {
            headers: {
              'Authorization': `Bearer ${your_jwt_token}`
            },
            withCredentials: true
          }
        );
        this.services = response.data; 
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },
  viewDocument(prof_email) {
      const documentUrl = `http://127.0.0.1:8080/api/view-document/${prof_email}`;
      window.open(documentUrl, '_blank');
    },
  async reuploadDocument(prof_email) {
    try {
        let your_jwt_token = localStorage.getItem('jwt');
        if (!your_jwt_token) {
          throw new Error('JWT token is missing');
        }
        this.$refs.documentInput.click();
    } catch (error) {
        console.error('Error triggering file upload:', error.message);
        alert('An error occurred while triggering the file upload.');
      }
   },
  async handleFileUpload(event) {
     const file = event.target.files[0];  
     if (!file) {
       return;
     }
     const formData = new FormData();
     formData.append('document', file);
     try {
       let your_jwt_token = localStorage.getItem('jwt');
       if (!your_jwt_token) {
         throw new Error('JWT token is missing');
       }   
       const response = await axios.post(`http://127.0.0.1:8080/api/reupload-document/${this.email}`, formData, {
         headers: {
           'Authorization': `Bearer ${your_jwt_token}`,
           'Content-Type': 'multipart/form-data'
         },
         withCredentials: true
       });    
       if (response.status === 200) {
         alert('Document reuploaded successfully.');
       } else {
         alert('Failed to reupload document: ' + response.data.error);
       }
     } catch (error) {
       console.error('Error uploading document:', error.message);
       alert('An error occurred while uploading the document.');
     }
  }
  }
}
</script>
  
  
<style scoped>
  .profile-card {
    background-color: #f8f9fa;
    width: 250px;
    border: 1px solid #ccc;
    border-radius: 8px;
    padding: 16px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  } 
  .profile-pic {
    border-radius: 100%;
    margin-bottom: 12px;
    width: 100px;
    height: 100px;
  }
  .name {
    font-size: 1.5em;
    margin: 0;
  }  
  .service {
    color: #777;
    margin: 8px 0;
  } 
  .email {
    color: #555;
    margin-bottom: 16px;
  }  
  .phone ,.service{
    background-color:#55799f;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
  }  
  .phone:hover {
    background-color: #55799f;
  }
 
</style>


  
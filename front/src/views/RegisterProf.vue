<template>
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card text-white shadow-lg" style="background-color: #282828; max-width: 600px;">
      <div class="card-header text-center" style="background-color: rgb(63, 35, 18);">
        <h2 class="mb-0">Professional Registration</h2>
      </div>
      <div class="card-body">
        <div class="text-end mb-3">
          <a href="/" class="btn btn-danger">Go Home</a>
        </div>
        <form @submit.prevent="register_prof">
          <div class="row g-3">
            <div class="col-md-6">
              <label for="emailID" class="form-label">Email ID:</label>
              <input type="email" class="form-control form-control-sm" placeholder="Email" required v-model="emailID" />
            </div>
            <div class="col-md-6">
              <label for="password" class="form-label">Password:</label>
              <input type="password" class="form-control form-control-sm" placeholder="Password" required v-model="pwd" />
            </div>
          </div>
          <div class="row g-3 mt-2">
            <div class="col-12">
              <label for="description" class="form-label">Description:</label>
              <textarea class="form-control form-control-sm" rows="1" placeholder="Expertise description" required v-model="description"></textarea>
            </div>
          </div>
          <div class="row g-3 mt-2">
            <div class="col-12">
              <label for="service_type" class="form-label">Service Type:</label>
              <select v-model="service_type" class="form-select form-select-sm" required>
                <option v-for="service in services" :key="service.id" :value="service.sev_name">
                  {{ service.sev_name }}
                </option>
              </select>
            </div>
          </div>
          <div class="row g-3 mt-2">
            <div class="col-md-6">
              <label for="experience" class="form-label">Experience:</label>
              <input type="text" class="form-control form-control-sm" placeholder="Years" required v-model="experience" />
            </div>
            <div class="col-md-6">
              <label for="phone" class="form-label">Phone:</label>
              <input type="text" class="form-control form-control-sm" placeholder="Phone" required v-model="phone" />
            </div>
          </div>
          <div class="row g-3 mt-2">
            <div class="col-md-6">
              <label for="address" class="form-label">Address:</label>
              <input type="text" class="form-control form-control-sm" placeholder="Address" required v-model="address" />
            </div>
            <div class="col-md-6">
              <label for="pincode" class="form-label">Pincode:</label>
              <input type="text" class="form-control form-control-sm" placeholder="Pincode" required v-model="pincode" />
            </div>
          </div>
          <div class="row g-3 mt-2">
            <div class="col-md-6">
              <label for="image" class="form-label">Profile Picture:</label>
              <input type="file" class="form-control form-control-sm" @change="handleImageUpload" accept="image/*" required />
            </div>
            <div class="col-md-6">
              <label for="file" class="form-label">Profile Document:</label>
              <input type="file" class="form-control form-control-sm" @change="handleFileUpload" accept=".pdf" required />
            </div>
          </div>
          <div class="d-grid gap-2 mt-3">
            <button type="submit" class="btn btn-primary btn-sm">Submit</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

  
<script>
import axios from 'axios';
export default {
  name: 'RegisterProf',
  data() {
    return {
        emailID: "",
        pwd: "",
        service_type: "",
        description:"",
        experience: "",
        file:null,
        address: "",
        pincode: "",
        phone: "",
        image: null,
        imageFile: null,
        documentFile: null,
        services: [],
    };
  },
  created() {
    this.fetchServices();
  },
  methods: {
    async register_prof(){
    try {
      const formData = new FormData();

        formData.append('prof_email', this.emailID);
        formData.append('prof_password', this.pwd);
        formData.append('service_type', this.service_type);
        formData.append('description', this.description);
        formData.append('experience', this.experience);
        formData.append('address', this.address);
        formData.append('pincode', this.pincode);
        formData.append('phone', this.phone);
        formData.append('image', this.imageFile);
        formData.append('file', this.documentFile);

      const response = await axios.post('http://127.0.0.1:8080/api/prof_reg', formData ,
        {
          headers: {'Content-Type': 'multipart/form-data' }
        });
        if (response.status === 201) {
          this.$router.push('/login');
          console.log("Professional registered successfully:");
        } else {
          alert(response.data.error);
        }
      } catch (error) {
        alert('An error occurred: ' + error.message);
      }
    },
    handleImageUpload(event) {
      this.imageFile = event.target.files[0];
    },
    handleFileUpload(event) {
      this.documentFile = event.target.files[0];
    },
    async fetchServices() {
      try {
        const response = await axios.get('http://127.0.0.1:8080/api/reg_servicenames',
        );
        this.services = response.data; 
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },

  }
  };
</script>


      
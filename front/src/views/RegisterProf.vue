<!-- <template>
    <div class="container text-white" style="background-color: #282828">
      <div class="top-right">
      <a href="/"><button class="btn btn-danger">Go Home</button></a>
      </div>
      <h1 style="text-align:center">Register as New Professional</h1>
      <br>
      <br>
      <form @submit.prevent="register_prof" style="text-align: center">
  
        <div class="mb-3 mt-3">
            <label for="emailID" class="form-label">Enter Email ID:</label>
            <input type="email" class="form-control" placeholder="Email" required=true v-model="emailID" />
        </div>
  
        <div class="mb-3">    
            <label for="password" class="form-label">Enter Password:</label>
            <input type="password" class="form-control" placeholder="Enter password" required=true v-model="pwd" />
        </div>
        <div class="mb-3">    
            <label for="description" class="form-label">description:</label>
            <input type="description" class="form-control" placeholder="description" required=true v-model="description" />
        </div>
        <div class="mb-3">
              <label class="form-label">Service Type:</label>
              <select  v-model="service_type" class="form-control" placeholder="service_type"  required>
                <option value="" disabled>Select a service type</option>
                <option value="Home Maintenance Services">Home Maintenance Services</option>
                <option value="Cleaning and Organization Services">Cleaning and Organization Services</option>
                <option value="Child_Elderly Care Services">Child_Elderly Care Services</option>
                <option value="Lifestyle and Convenience Services">Lifestyle and Convenience Services</option>
              </select>
            </div>
        
        <div class="mb-3">    
            <label for="experience" class="form-label">experience:</label>
            <input type="experience" class="form-control" placeholder="experience" required=true v-model="experience" />
        </div>
        
        <div class="mb-3">    
            <label for="address" class="form-label">address:</label>
            <input type="address" class="form-control" placeholder="address" required=true v-model="address" />
        </div>
        <div class="mb-3">    
            <label for="pincode" class="form-label">pincode:</label>
            <input type="pincode" class="form-control" placeholder="pincode" required=true v-model="pincode" />
        </div>

        <div class="mb-3">
            <label for="phone" class="form-label">Phone:</label>
            <input type="phone" class="form-control" placeholder="phone" required=true v-model="phone" />
        </div>
        <div class="mb-3">
            <label for="image" class="form-label">Upload Profile Picture:</label>
            <input type="file" class="form-control" @change="handleImageUpload" accept="image/*" required />
        </div>

        <div class="mb-3">
            <label for="file" class="form-label"> Upload Profile Document:</label>
            <input type="file" class="form-control" @change="handleFileUpload" accept=".pdf" required/>
        </div>
      
        <input type="submit"  class="btn btn-primary"/>
  
      </form>
  
    </div>
</template> -->

<template>
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card text-white shadow-lg" style="background-color: #282828; max-width: 600px;">
      <div class="card-header text-center" style="background-color: rgb(63, 35, 18);">
        <h2 class="mb-0">Register as Professional</h2>
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
              <label class="form-label">Service Type:</label>
              <select v-model="service_type" class="form-select form-select-sm" required>
                <option value="" disabled>Select service type</option>
                <option value="Home Maintenance Services">Home Maintenance</option>
                <option value="Cleaning and Organization Services">Cleaning & Organization</option>
                <option value="Child & Elderly Care Services">Child & Elderly Care</option>
                <option value="Lifestyle and Convenience Services">Lifestyle & Convenience</option>
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
        documentFile: null
    };
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
          headers: {
            'Content-Type': 'multipart/form-data'

          }
        });

        console.log(this.emailID, this.pwd, this.address, this.pincode,this.documentFile, this.imageFile);

        if (response.status === 201) {
          this.$router.push('/login');
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
    }
  }
  };
</script>


      
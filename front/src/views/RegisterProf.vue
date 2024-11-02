<template>
    <!-- <div>
      <center><img src="../assets/logo.png" height="120" width="120" /></center>
    </div> 
     v-on:submit.prevent="register()" -- when u click submit trying to prevent default behaviour of form ie rendering html template-->
    <br>

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
      
        <input type="submit"  class="btn btn-primary"/>
  
      </form>
      <br>
      <br>
  
    
  
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
        // file: null,
        address: "",
        pincode: ""
    };
  },
  methods: {
    async register_prof(){
    try {const response = await axios.post('http://127.0.0.1:8080/api/prof_reg', 
        {
        "prof_email": this.emailID,
        "prof_password": this.pwd,
        "service_type": this.service_type,
        "description":this.description,
        "experience":this.experience,
        "address": this.address,
        "pincode": this.pincode
        },
        {
          headers: {
            'Content-Type': 'application/json'  
          }
        });

        console.log(this.emailID, this.pwd, this.address, this.pincode);

        if (response.status === 201) {
          this.$router.push('/login');
        } else {
          alert(response.data.error);
        }
      } catch (error) {
        alert('An error occurred: ' + error.message);
      }
    }
  }
};
</script>


      
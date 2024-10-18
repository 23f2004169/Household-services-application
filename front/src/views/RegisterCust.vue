<template>
  <br>
  <div class="container p-5 my-5 bg-dark text-white">
    <h1 style="text-align:center">Register a New User Account</h1>
    <br>
    <br>
    <form @submit.prevent="register" style="text-align: center">  <!-- Changed login to register -->

      <div class="mb-3 mt-3">
        <label for="emailID" class="form-label">Enter Email ID:</label>
        <input type="email" class="form-control" placeholder="Enter email" required v-model="emailID" />
      </div>

      <div class="mb-3">
        <label for="pwd" class="form-label">Enter Password:</label>
        <input type="password" class="form-control" placeholder="Enter password" required v-model="pwd" />
      </div>
      
      <div class="mb-3">
        <label for="address" class="form-label">Enter address:</label>
        <input type="text" class="form-control" placeholder="address" required v-model="address" />
      </div>

      <div class="mb-3">
        <label for="pincode" class="form-label">Enter pincode:</label>
        <input type="text" class="form-control" placeholder="pincode" required v-model="pincode" />
      </div>

      <input type="submit" class="btn btn-primary" />

    </form>
    
    <a href="/register_prof"><button class="btn btn-secondary btn-custom">REGISTER AS PROFESSIONAL?</button></a>

    <br>
    <br>

  </div>
</template>

  
<script>
import axios from 'axios';

export default {
  name: 'RegisterCust',
  data() {
    return {
      emailID: "",
      pwd: "",
      address: "",
      pincode: ""
    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('http://127.0.0.1:8080/api/cust_reg', 
        {
          "cust_email": this.emailID,   // Make sure the field names match the backend expectation
          "cust_password": this.pwd,
          "address": this.address,
          "pincode": this.pincode
        },
        {
          headers: {
            'Content-Type': 'application/json'  // Ensure JSON data is correctly recognized
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

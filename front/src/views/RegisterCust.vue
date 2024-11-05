<template>
  <div class="container text-white" style="background-color: #282828">
    <h1 style="text-align:center;">Register a New User Account</h1>

    <div class="top-right ">
       <a href="/"><button class="btn btn-danger  ">Go Home</button></a>
    </div>

    <form @submit.prevent="register" style="text-align: center">  

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

      <div class="mb-3">
        <label for="phone" class="form-label">Phone:</label>
        <input type="phone" class="form-control" placeholder="Enter phone" required  v-model="phone"/>
      </div>

      <input type="submit" class="btn btn-primary" />

    </form>
      <div class="top-left">
       <a href="/register_prof"><button class="btn btn-secondary btn-custom top-left" >REGISTER AS PROFESSIONAL?</button></a>
      </div>
  </div>
</template>

<style>
.top-left {
    position: absolute;
    top: 10px; /* Adjust as needed */
    left: 10px; /* Adjust as needed */
}
.btn-custom {
            padding: 15px 30px; /* Increase padding for a larger button */
            font-size: 1.25rem; /* Increase font size */
            background-color: #8e631e; /* Change background color to a more visible green */
            color: white; /* Ensure text is white for contrast */
            border: none; /* Remove border */
            border-radius: 5px; /* Add border radius for rounded corners */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Add shadow for depth */
            transition: background-color 0.3s ease; /* Smooth transition for hover effect */
        }

        .btn-custom:hover {
            background-color: #218838; /* Darker green on hover */
        }
</style>

<script>
import axios from 'axios';

export default {
  name: 'RegisterCust',
  data() {
    return {
      emailID: "",
      pwd: "",
      address: "",
      pincode: "",
      phone: ""
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
          "pincode": this.pincode,
          "phone": this.phone
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

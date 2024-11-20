<template>
  <div class="container text-white" style="background-color: #282828">
    <h1 style="text-align:center;">Register a New User Account</h1>

    <div class="top-right ">
       <a href="/"><button class="btn btn-danger">Go Home</button></a>
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
          "cust_email": this.emailID,   
          "cust_password": this.pwd,
          "address": this.address,
          "pincode": this.pincode,
          "phone": this.phone
        },
        {
          headers: {
            'Content-Type': 'application/json'  
          }
        });
        if (response.status === 201) {
          this.$router.push('/login');
          console.log("Customer Registration successful");
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


<style>
.top-left {
    position: absolute;
    top: 10px; 
    left: 10px; 
}
.btn-custom {
            padding: 15px 30px; 
            font-size: 1.25rem; 
            background-color: #8e631e; 
            color: white; 
            border: none;
            border-radius: 5px; 
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease; }
.btn-custom:hover {
            background-color: #218838;}
</style>
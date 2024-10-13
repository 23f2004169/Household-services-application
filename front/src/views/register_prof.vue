<template>
    <!-- <div>
      <center><img src="../assets/logo.png" height="120" width="120" /></center>
    </div> 
     v-on:submit.prevent="register()" -- when u click submit trying to prevent default behaviour of form ie rendering html template-->
    <br>

    <div class="container p-5 my-5 bg-dark text-white">
      
      <h1 style="text-align:center">Register as New Professional</h1>
      <br>
      <br>
      <form style="text-align: center">
  
        <div class="mb-3 mt-3">
            <label for="emailID" class="form-label">Enter Email ID:</label>
            <input type="email" class="form-control" placeholder="Email" required=true v-model="emailID" />
        </div>

        <div class="mb-3">
            <label for="name" class="form-label">Enter Full Name of the User:</label>
            <input type="text" class="form-control" placeholder="name" required=true v-model="name" />
        </div>
  
        <div class="mb-3">    
            <label for="password" class="form-label">Enter Password:</label>
            <input type="password" class="form-control" placeholder="Enter password" required=true v-model="pwd" />
        </div>
        <div class="mb-3">    
            <label for="description" class="form-label">description:</label>
            <input type="description" class="form-control" placeholder="description" required=true v-model="pwd" />
        </div>
        <div class="mb-3">    
            <label for="service_type" class="form-label">service_type:</label>
            <input type="service_type" class="form-control" placeholder="service_type" required=true v-model="pwd" />
        </div>
        <div class="mb-3">    
            <label for="experience" class="form-label">experience:</label>
            <input type="experience" class="form-control" placeholder="experience" required=true v-model="pwd" />
        </div>
        <div class="mb-3">    
            <label for="date_created" class="form-label">date_created:</label>
            <input type="date_created" class="form-control" placeholder="date_created" required=true v-model="pwd" />
        </div>
        <div class="mb-3">    
            <label for="address" class="form-label">address:</label>
            <input type="address" class="form-control" placeholder="address" required=true v-model="pwd" />
        </div>
        <div class="mb-3">    
            <label for="pincode" class="form-label">pincode:</label>
            <input type="pincode" class="form-control" placeholder="pincode" required=true v-model="pwd" />
        </div>
      
        <input type="submit" @click='register_prof' center class="btn btn-primary"/>
  
      </form>
      <br>
      <br>
  
    
  
    </div>
</template>
  
<script>
export default {
  name: 'register_prof',
  data() {
    return {
        emailID: "",
        name: "",
        pwd: "",
        service_type: '',
        description:'',
        experience: '',
        date_created:'',
        file: null,
        address: '',
        pinCode: ''
    };
  },
  methods: {
      register_prof(){
          this.$router.push({ path: '/admin_dashboard' });
    }
  }
};
</script> 
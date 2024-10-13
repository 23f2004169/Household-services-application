<template>
    <!-- <div>
      <center><img src="../assets/logo.png" height="120" width="120" /></center>
    </div> 
     v-on:submit.prevent="register()" -- when u click submit trying to prevent default behaviour of form ie rendering html template-->
    <br>

    <div class="container p-5 my-5 bg-dark text-white">
      
      <h1 style="text-align:center">Register a New User Account</h1>
      <br>
      <br>
      <form style="text-align: center">
  
        <div class="mb-3 mt-3">
            <label for="emailID" class="form-label">Enter Email ID:</label>
            <input type="email" class="form-control" placeholder="Enter email" required=true v-model="emailID" />
        </div>

        <div class="mb-3">
            <label for="name" class="form-label">Enter Full Name of the User:</label>
            <input type="text" class="form-control" placeholder="Enter Name" required=true v-model="name" />
        </div>
  
        <div class="mb-3">    
            <label for="pwd" class="form-label">Enter Password:</label>
            <input type="password" class="form-control" placeholder="Enter password" required=true v-model="pwd" />
        </div>
        <div class="mb-3">    
            <label for="address" class="form-label">Enter address:</label>
            <input type="address" class="form-control" placeholder="address" required=true v-model="pwd" />
        </div>
        <div class="mb-3">    
            <label for="pincode" class="form-label">Enter pincode:</label>
            <input type="pincode" class="form-control" placeholder="pincode" required=true v-model="pwd" />
        </div>
        <input type="submit" @click='register' center class="btn btn-primary"/>
  
      </form>
      <a href="/register_prof"><button class="btn btn-secondary btn-custom" >REGISTER AS PROFESSIONAL?</button></a>

      <br>
      <br>
  
    
  
    </div>
</template>
  
<script>
export default {
  name: 'register',
  data() {
    return {
      emailID: "",
      name: "",
      pwd: "",
      address:"",
      pincode:""
    };
  },
  methods: {
      register(){
          this.$router.push({ path: '/admin_dashboard' });
    }
  }
};
</script> 
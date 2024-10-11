<template>

    <div class="container-fluid">
      <nav class="navbar navbar-expand-sm bg-dark navbar-dark">
        <div class="container-fluid">
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link" v-on:click="register()">Register</a>
            </li>
          <li class="nav-item">
              <a class="nav-link active">Create an Account: Enter Details</a>
            </li>
          </ul>
        </div>
      </nav>
    </div>

    <!-- <div>
      <center><img src="../assets/logo.png" height="120" width="120" /></center>
    </div> -->
    <br>

    <div class="container p-5 my-5 bg-dark text-white">
      
      <h1 style="text-align:center">Register a New User Account</h1>
      <br>
      <br>
      <form v-on:submit.prevent="registerUser()" style="text-align: center">
  
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
      
        <input type="submit" center class="btn btn-primary"/>
  
      </form>
      <br>
      <br>
  
    
  
    </div>
</template>
  
<script>


  export default {
    name: 'register',
  
    data() {
      return{
        emailID: "",
        name: "",
        pwd: "",       
      
    };
  },
    
    methods: {
      register(){
          this.$router.push({ path: '/register' });
    },
    }
}
</script>
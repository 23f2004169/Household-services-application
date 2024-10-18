<template>
  <div class="container mt-5">
    <div class="top-right">
      <a href="/"><button class="btn btn-danger">Go Homeeeee</button></a>
    </div>
    <h1>Login page</h1>
    
    <form @submit.prevent="login">
      <label for="email" class="form-label white">Enter email:</label>
      <input v-model="email" type="text" name="email" id="email" class="form-control" required>
      <label for="password" class="form-label white">Enter password:</label>
      <input v-model="password" type="password" name="password" id="password" class="form-control" required>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>  
  </div> 
</template>

<style>
.top-right {
  position: absolute;
  top: 10px;
  right: 10px;
}
body {
  padding-top: 20px;
  background-color: rgb(205, 176, 132);
}
</style>

<script>
import axios from 'axios';
export default {
  name: 'LoginView',
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    async login() {
      try {
        // Make the login request
        const response = await axios.post('http://127.0.0.1:8080/api/admin_login', {
          "email": this.email,
          "password": this.password
        });

        if (response.status === 200) {
          this.$router.push('/admin_dashboard');
        } 
        else {
          alert(response.data.error);
        }
      } catch (error) {
        alert('An error occurred: ' + error.message);
      }
    }
  }
}
</script>

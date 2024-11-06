<template>
  <div class="container mt-5">
    <div class="top-right">
      <a href="/"><button class="btn btn-danger">Go Home</button></a>
    </div>
    <h1 style="color:white">Login page</h1>
    
    <form @submit.prevent="login">
      <label for="email" class="form-label white">Enter email:</label>
      <input v-model="email" type="text" name="email" id="email" class="form-control" required>
      <label for="password" class="form-label white">Enter password:</label>
      <input v-model="password" type="password" name="password" id="password" class="form-control" required>
      <label for="role" class="form-label white">Select Role:</label>
      <select v-model="role" name="role" id="role" class="form-control" required>
      <option value="" disabled>Select a role</option>
      <option value="admin">Admin</option>
      <option value="cust">Customer</option>
      <option value="prof">Professional</option>
      </select>                
      <button type="submit" style="background-color: rgb(63, 35, 18);">Submit</button>
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
      role: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post(`http://127.0.0.1:8080/api/login`, {
          email: this.email,
          password: this.password,
          role: this.role
        , 
          withCredentials: true  
        });

        if (response.status === 200) {
          localStorage.setItem('jwt', response.data.access_token);
          localStorage.setItem('role', this.role);

          if (this.role === 'admin') {
            this.$router.push('/admin_dashboard');
          } else if (this.role === 'cust') {
            this.$router.push({ path: '/cust_dashboard', query: { email: this.email } });
          } else if (this.role === 'prof') {
            this.$router.push({ path: '/prof_dashboard', query: { email: this.email } });
          } else {
            alert('Invalid role');
          }
        } else {
          alert(response.data.error);
        }
      } catch (error) {
        if (error.response && error.response.status === 403) {
          alert(error.response.data.error);
        } else {
          alert('An error occurred: ' + error.message);
        }
      }
    }
  }
}
</script>

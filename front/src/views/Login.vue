<template>
    <div class="container mt-5">
        <div class="top-right">
            <a href="/"><button class="btn btn-danger">Go Home</button></a>
        </div>
    <h1 >Admin login page</h1>
    
    <form method="post">
        <label for="admin_name" class="form-label white">Enter Admin name</label>
        <input type="text" name="admin_name" id="admin_name" class="form-control">
        <label for="admin_password" class="form-label white">Enter Admin password:</label>
        <input type="text" name="admin_password" id="admin_password" class="form-control">
        <button v-on:click="login" type="submit" class="btn btn-primary">Submit</button>
    
    </form>  
    </div> 
</template>
<style>.top-right {position: absolute;top: 10px;right: 10px;}
         body {padding-top: 20px;background-color:rgb(205, 176, 132);}
</style>
<script>
export default {
  name: 'Login',
  data() {
    return {
      emailID: "",
      name: "",
      pwd: ""
    };
  },
  methods: {
      login(){
          this.$router.push({ path: '/admin_dashboard' });
    }
  }
};
</script>
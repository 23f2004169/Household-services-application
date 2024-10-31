<template>
    <div class="container mt-0">
      <header class="d-flex justify-content-between align-items-center mb-4">
        <MenuBar/>
      </header>
    </div>
     <div style="margin-top: 5%; margin-left: 5%; margin-right: 5%;">
        <h1 class="white">Search based on Influencer name</h1>
        <form method="post" class="card p-5" style="margin-top: 5%; margin-left: 5%; margin-right: 5%;">
            <label class="form-label" for="inf_name">Enter the Influencer name:</label>
            <input class="form-control" type="text" name="inf_name" id="inf_name" required>
            <button class="btn btn-primary" type="submit" style="width: 10%;">Search</button>
        </form>
    </div>
</template>

<style>
   body {padding-top: 70px;background-color:#282828;}
   .white{color:white}
    h1, h2 {margin-top: 20px;}
    table {margin-top: 20px;}.form-container {margin-top: 30px;}.navbar-brand {font-weight: bold;}.navbar, .offcanvas-header, .offcanvas-body {background-color: #f0f2ec;}
    .navbar-brand, .nav-link, .offcanvas-title {color: #020b17;}
    .nav-link.active {font-weight: bold;color: #e98e0f !important;}.btn-primary, .btn-outline-success {margin-top: 10px;}
</style>


<script>
  import axios from 'axios';
  import MenuBar from '../components/MenuBar.vue';
  
  export default {
    name: "AdminSearch",
    components: { MenuBar },
  };
</script>
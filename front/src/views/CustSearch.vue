<template>
<div class="container mt-0">
      <header class="d-flex justify-content-between align-items-center mb-4">
        <CustBar  :email="email" />
      </header>
</div>
<div>
    <CustSearchBar @updateResults="setResults" />
    <div v-if="profResults.length > 0" class="card-deck mt-4">
      <div v-for="result in profResults":key="result.prof_email" class="card mb-4" style="width: 18rem;">
        <div class="card-body">
          <h5 class="card-title">{{ result.prof_email }}</h5>
          <p class="card-text">Service type:{{ result.service_type }}</p>
          <p class="card-text">Experience:{{ result.experience }}</p>
          <p class="card-text">Description:{{ result.description }}</p>
          <div class="d-flex">
                <button class="btn btn-dark btn-sm">View profile</button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="serviceResults.length > 0" class="card-deck mt-4">
      <div v-for="result in serviceResults" :key="result.sev_id" class="card mb-4" style="width: 18rem;">
        <div class="card-body">
          <h5 class="card-title">Service:{{ result.sev_name }}</h5>
          <p class="card-text">Description:{{ result.description }}</p>
          <p class="card-text">Base Price:{{ result.price }}</p>
          <p class="card-text">Service Category:{{ result.category }}</p>
          <div class="d-flex">
                <button class="btn btn-dark btn-sm">View service</button>
          </div>
        </div>
      </div>
    </div>
    <div  v-else-if="searchPerformed" class="no-results-message mt-4">
      <p class="text-white">No results found for your search.</p>
    </div>
  </div> 
</template>


<script>
import CustSearchBar from "../components/CustSearchBar.vue";
import axios from 'axios';
import CustBar from '../components/CustBar.vue';

export default {
  name: "CustSearch",
  components: {
    CustSearchBar,CustBar
  },
  props: {
      email: {type: String, required: true,},
        },
  data() {
    return {
      searchPerformed: false,
      searchResults: [],
      profResults: [], 
      serviceResults: [],
    };
  },
  methods: {
   // Method to set professional search results
   setResults(results) {
      if (results && results.length > 0) {
        // Check if results have "prof_email" key (professional results)
        if (results[0].prof_email) 
          this.profResults = results;
          this.serviceResults = []; // Clear service results if profResults are used
        }
        // Check if results have "sev_id" key (service results)
        else if (results[0].sev_id) {
          this.serviceResults = results;
          this.profResults = []; // Clear professional results if serviceResults are used
        }
        else {
          this.searchPerformed = true; 
        }
      },
      performSearch() {
        this.searchPerformed = true; // Set to true when search button is clicked
      },
    },
};
</script>

<style scoped>
.card-deck {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}
.card {
  margin: 10px;
}
   body {padding-top: 70px;background-color:#282828;}
   .white{color:white}
    h1, h2 {margin-top: 20px;}
    table {margin-top: 20px;}.form-container {margin-top: 30px;}.navbar-brand {font-weight: bold;}.navbar, .offcanvas-header, .offcanvas-body {background-color: #f0f2ec;}
    .navbar-brand, .nav-link, .offcanvas-title {color: #020b17;}
    .nav-link.active {font-weight: bold;color: #e98e0f !important;}.btn-primary, .btn-outline-success {margin-top: 10px;}
</style>



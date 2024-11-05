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
    setResults(results) {
      this.searchPerformed = false;
      this.searchResults = [];
      this.profResults = [];
      this.serviceResults = [];
  
      if (results && results.length > 0) {
        console.log(results);
        
        if (results[0].prof_email) {
          this.profResults = results;
          this.serviceResults = []; 
        }
        else if (results[0].sev_id) {
          this.serviceResults = results;
          this.profResults = []; 
        }
      } else {
        this.searchPerformed = true; 
      }
      
      this.searchPerformed = true;
    },
    
    executeSearch() {
      this.searchPerformed = false;
  
      if (this.searchType === "professional") {
        this.submitSearch();
      } else if (this.searchType === "service") {
        this.searchServices();
      }
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
  
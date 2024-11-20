<template>
      <div class="container mt-0">
        <header class="d-flex justify-content-between align-items-center mb-4">
          <ProfBar :email="email"/>
        </header>
      </div>
    <div>
      <ProfSearchBar @updateResults="setResults" @searchPerformed="performSearch" :email="email"/>
      <div v-if="searchResults.length > 0" class="card-deck mt-4">
        <div
          v-for="result in searchResults"
          :key="result.prof_email"
          class="card mb-4"
          style="width: 18rem;">
          <div class="card-body">
            <h5 class="card-title">Service Request ID:{{ result.sevreq_id }}</h5>
            <p class="card-text">Customer:{{ result.cust_email }}</p>
            <p class="card-text">Status:{{ result.sev_status }}</p>
            <p class="card-text">Rating:{{ result.rating }}</p>
            <p class="card-text">Remarks:{{ result.remarks }}</p>
            <p class="card-text">Date of request:{{ result.date_of_request }}</p>
            <p class="card-text">Date of completion:{{ result.date_of_completion }}</p>
          </div>
        </div>
      </div>
  
      <div v-else-if="searchPerformed" class="no-results-message mt-4">
        <p class="text-white">No results found for your search.</p>
      </div>
    </div>
</template>
  
<script>
  import ProfSearchBar from "../components/ProfSearchBar.vue";
  import ProfBar from '../components/ProfBar.vue';
    
  export default {
    name:  "ProfSearch",
    components: {ProfSearchBar,ProfBar},
    data() {
      return {
        searchResults: [],
        searchPerformed: false
      };
    },
    props: {
          email: {type: String, required: true,},
            },
    methods: {
      setResults(results) {
        this.searchResults = results;
        this.searchPerformed = true; 
      },
      performSearch() {
        this.searchPerformed = true; 
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
  
  
  
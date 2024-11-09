<template>
    <div class="container mt-0">
      <header class="d-flex justify-content-between align-items-center mb-4">
        <MenuBar/>
      </header>
    </div>
  <div>
    <SearchBar @updateResults="setResults" @searchPerformed="performSearch"/>
    <div v-if="searchResults.length > 0" class="card-deck mt-4">
      <div
        v-for="result in searchResults"
        :key="result.prof_email"
        class="card mb-4"
        style="width: 18rem;">
        <div class="card-body">
          <h5 class="card-title">{{ result.prof_email }}</h5>
          <p class="card-text">Service:{{ result.service_type }}</p>
          <p class="card-text">Experience:{{ result.experience }}</p>
          <p class="card-text">Description:{{ result.description }}</p>
          <p class="card-text">Rating:{{ result.rating }}</p>
          <p class="card-text">Mobile no:{{ result.phone }}</p>
          <div class="d-flex">
                <button @click="blockProfessional(result.prof_email)" class="btn btn-dark btn-sm">Block/Unblock</button>
                <button @click="viewDocument(result.prof_email)" class="btn btn-primary btn-sm">Review Profile</button> 

          </div>
        </div>
      </div>
    </div>
    <div v-else-if="searchPerformed" class="no-results-message mt-4">
      <p class="text-white">No results found for your search.</p>
    </div>
  </div>
</template>
<!-- v-if="result.service_type" -->

<script>
import SearchBar from "../components/SearchBar.vue";
import axios from 'axios';
import MenuBar from '../components/MenuBar.vue';

export default {
  name: "AdminSearch",
  components: {
    SearchBar,
    MenuBar
  },
  data() {
    return {
      searchResults: [],
      searchPerformed: false
    };
  },
  methods: {
    setResults(results) {
      this.searchResults = results;
      this.searchPerformed = true;
    },
    performSearch() {
      this.searchPerformed = true;
    },
    async blockProfessional(prof_email) {
      try {
        let your_jwt_token = localStorage.getItem("jwt");
        if (!your_jwt_token) {
          throw new Error("JWT token is missing");
        }

        const response = await axios.post(
          `http://127.0.0.1:8080/api/professional/block/${prof_email}`,
          {},
          {
            headers: {
              Authorization: `Bearer ${your_jwt_token}`,
            },
            withCredentials: true,
          }
        );

        if (response.status === 200) {
          console.log("Professional blocked successfully:", response.data);
        } else {
          console.error("Failed to block professional: " + response.data.error);
        }
      } catch (error) {
        console.error("Error blocking professional:", error.message);
      }
    },
    
viewDocument(prof_email) {
      // Open document in new tab
      const documentUrl = `http://127.0.0.1:8080/api/view-document/${prof_email}`;
      window.open(documentUrl, '_blank');
    }
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



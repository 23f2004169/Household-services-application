<template>
  <div class="message mb-2 text-white">
            <h5 v-if="searchType === 'service'">Search for services </h5>
            <h5 v-else>Search for professionals</h5>
        </div>
  <div class="container my-3">
    <div class="search-bar">
      <div class="input-group">
        <select v-model="searchType" class="search-type-dropdown">
          <option value="professional">Professional</option>
          <option value="service">Service</option>
        </select>
        
        <input type="text" class="form-control search-input" placeholder="Search for Services or Professionals" v-model="searchQuery"/>
        <div class="input-group-append">
          <button class="btn search-button" @click="executeSearch">
            Search
          </button>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "CustSearchBar",
  data() {
    return {
      searchQuery: "",
      searchType: "service",
      results: [],
      sresults: [],
    };
  },
  emits: ['updateResults', 'searchPerformed'],  
  methods: {
    async searchServices() {
      try {
        let your_jwt_token = localStorage.getItem("jwt");
        if (!your_jwt_token) {
          throw new Error("JWT token is missing");
        }
        const response = await axios.post("http://127.0.0.1:8080/api/cust_search", {
            query: this.searchQuery,
            sev_id: this.sresults.sev_id,
            sev_name: this.sresults.sev_name,
            description: this.sresults.description,
            category: this.sresults.category,
            time_req: this.sresults.time_req,
            price: this.sresults.price,
            address: this.sresults.address,
            pincode: this.sresults.pincode,
        },
        {
          headers: {
            Authorization: `Bearer ${your_jwt_token}`,
          },  
          withCredentials: true,
        });
        if (response.status === 200) {
          const data = response.data.sresults;
          this.$emit("updateResults", data); // pass results to the parent component
          this.sresults = data; 
        } else {
          alert("Failed to fetch services: " + response.data.error);
        }
      } catch (error) {
        console.error("Error fetching services:", error.message);
        alert("An error occurred while fetching services.");
      }
    },
    async submitSearch() {
      try {
        let your_jwt_token = localStorage.getItem("jwt");
        if (!your_jwt_token) {
          throw new Error("JWT token is missing");
        }
        const response = await axios.post("http://127.0.0.1:8080/api/admin_search", {
          query: this.searchQuery,
          prof_email: this.results.prof_email,
          description: this.results.description,
          service_type: this.results.service_type,
          experience: this.results.experience,
          address: this.results.address,
          pincode: this.results.pincode,
          blocked: this.results.blocked,
          approval: this.results.approval,
          rating: this.results.rating,
          phone: this.results.phone
        },
        {
          headers: {
            Authorization: `Bearer ${your_jwt_token}`,
          },  
          withCredentials: true,
        });
        
        if (response.status === 200) {
          const data = response.data.results;
          this.$emit("updateResults", data); 
          this.results = data; 
        } else {
          alert("Failed to fetch services: " + response.data.error);
        }
      } catch (error) {
        console.error("Error fetching services:", error.message);
        alert("An error occurred while fetching services.");
      }
    },
    executeSearch() {
    if (this.searchType === "professional") {
      this.submitSearch();
    } else {
      this.searchServices();
    }
  },
 }
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;}
.search-bar {
  width: 100%;
  max-width: 600px;
  border-radius: 50px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;}
.search-bar:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);}
.search-input {
  border: none;
  padding: 15px 20px;
  border-radius: 50px 0 0 50px;
  font-size: 1rem;
  transition: all 0.3s ease;}
.search-input:focus {
  outline: none;
  box-shadow: none;}
.search-button {
  background-color:rgb(63, 35, 18);
  color: white;
  border: none;
  padding: 15px 25px;
  border-radius: 0 50px 50px 0;
  font-size: 1rem;
  font-weight: bold;
  transition: background-color 0.3s ease;}
.search-button:hover {
  background-color:#282828;}
</style>


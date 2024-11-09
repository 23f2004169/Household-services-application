<template>
  <div><p class="text-white">Search for service requests based on their status(closed,accepted,rejected,requested) and rating(1-5)</p></div>
    <div class="container my-3">
      <div class="search-bar">
        <div class="input-group">
          <input
            type="text"
            class="form-control search-input"
            placeholder="Search for Service Requests"
            v-model="searchQuery"
          />
          <div class="input-group-append">
            <button class="btn search-button" @click="submitSearch">
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
    name: "ProfSearchBar",
    data() {
      return {
        searchQuery: "",
        results: [],
      };
    },
    emits: ['updateResults', 'searchPerformed'],  
    props: {
      email: {  
        type: String,
        required: true,
      },
    },
    methods: {
      async submitSearch() {
        try {
          let your_jwt_token = localStorage.getItem('jwt');
          if (!your_jwt_token) {
            throw new Error('JWT token is missing');
          }
          const response = await axios.post(`http://127.0.0.1:8080/api/prof_search/${this.email}`, {
            query: this.searchQuery,
            sevreq_id: this.results.sevreq_id,
            cust_email: this.results.cust_email,
            prof_email: this.results.prof_email,
            sev_status: this.results.sev_status,
            rating: this.results.rating,
            remarks: this.results.remarks,
            date_of_request: this.results.date_of_request,
            date_of_completion: this.results.date_of_completion
          }, {
            headers: {
              'Authorization': `Bearer ${your_jwt_token}`
            },
            withCredentials: true
          });
          
          if (response.status === 200) {
            const data = response.data.results;
            this.$emit("updateResults", data); // Pass results to parent component
            this.results = data; // Update local results if needed
          } else {
            alert("Failed to fetch services: " + response.data.error);
          }
        } catch (error) {
          console.error("Error fetching services:", error.message);
          alert("An error occurred while fetching services.");
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    display: flex;
    justify-content: center;
  }
  
  .search-bar {
    width: 100%;
    max-width: 600px;
    border-radius: 50px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s ease;
  }
  
  .search-bar:hover {
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
  }
  
  .search-input {
    border: none;
    padding: 15px 20px;
    border-radius: 50px 0 0 50px;
    font-size: 1rem;
    transition: all 0.3s ease;
  }
  
  .search-input:focus {
    outline: none;
    box-shadow: none;
  }
  
  .search-button {
    background-color:rgb(63, 35, 18);
    color: white;
    border: none;
    padding: 15px 25px;
    border-radius: 0 50px 50px 0;
    font-size: 1rem;
    font-weight: bold;
    transition: background-color 0.3s ease;
  }
  
  .search-button:hover {
    background-color:#282828;
  }
  </style>
  
  
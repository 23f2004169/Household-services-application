<template>
  <div class="container mt-0">
        <header class="d-flex justify-content-between align-items-center mb-4">
          <CustBar  :email="email" />
        </header>
  </div>
  <div>
    <CustSearchBar @updateResults="setResults" />

      <div v-if="profResults.length > 0" class="services">
        <div v-for="result in profResults":key="result.prof_email" class="service-card" style="width: 18rem;">
          <div class="card-body">
            <h5 class="card-title">{{ result.prof_email }}</h5>
            <img :src="'http://127.0.0.1:8080/api/view-image/' + result.prof_email" alt="Profile Picture" class="pic" />
            <p class="card-text">Service type:{{ result.service_type }}</p>
            <p class="card-text">Experience:{{ result.experience }}</p>
            <p class="card-text">Description:{{ result.description }}</p>
            <p class="card-text">Rating:{{ result.rating }}</p>
            <p class="card-text">Mobile no:{{ result.phone }}</p>
            <div class="d-flex">
              <button @click.prevent="showNewServiceRequestForm = true"  class="red">
              + New Service Request
            </button>   
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="serviceResults.length > 0" class="services">
        <div v-for="result in serviceResults" :key="result.sev_id" class="service-card" style="width: 18rem;">
          <div class="card-body">
            <h5 class="card-title">Service:{{ result.sev_name }}</h5>
            <img :src="getImageUrl(result.sev_name)" alt="Service image" class="pic">
            <p class="card-text">{{ result.description }}</p>
            <p class="card-text">Base Price:{{ result.price }}</p>
            <p class="card-text">Service Category:{{ result.category }}</p>
            <p class="card-text">Duration:{{ result.time_req }} minutes</p>
            <p class="card-text">Address:{{ result.address }}</p>
            <p class="card-text">Pincode:{{ result.pincode }}</p>
            <div class="d-flex">
              <button @click.prevent="showNewServiceRequestForm = true"  class="red">
              + New Service Request
            </button>            
          </div>
          </div>
        </div>
      </div>

      <div  v-else-if="searchPerformed" class="no-results-message mt-4">
        <p class="text-white">No results found for your search.</p>
      </div>
</div>

 
    <!-- New Service Request Form Modal -->
<div v-show="showNewServiceRequestForm" class="modal fade show" style="display: block;" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">New Service Request</h5>
        <button @click.prevent="showNewServiceRequestForm = false" class="btn-close"></button>
      </div>
      <div class="modal-body">
        <form @submit.prevent="addNewServiceRequest">
          <div class="mb-3">
            <label class="form-label">Customer Email:</label>
            <input v-model="newServiceRequest.cust_email" type="email" class="form-control" required readonly />
          </div>
          <div class="mb-3">
            <label for="service" class="form-label">Service:</label>
            <select v-model="newServiceRequest.sev_id" name="service" id="service" class="form-control" required  >
              <option value="">Select a Service</option>
              <option v-for="service in services" :key="service.sev_id" :value="service.sev_id" >
                {{ service.sev_name }}
              </option>
            </select>
          </div>

          <div class="mb-3">
          <label class="form-label">Professional Email:</label>
          <select v-model="newServiceRequest.prof_email" name="professional" id="prof_email" class="form-control" required >
            <option value="">Select a Professional</option>
            <option v-for="professional in filteredProfessionals" :key="professional.prof_email" :value="professional.prof_email">
              {{ professional.prof_email }}
            </option>
          </select>
          </div>
    
          <div class="mb-3">
            <label class="form-label">Date of Request:</label>
            <datepicker 
              v-model="newServiceRequest.date_of_request" 
              :format="formatDateOnly"
              class="form-control" 
              required />
          </div>
          
          <div class="mb-3">
            <label class="form-label">Date of Completion:</label>
            <datepicker 
              v-model="newServiceRequest.date_of_completion" 
              :format="formatDateOnly"
              class="form-control" 
              required />
          </div>

          <div class="modal-footer">
            <button type="submit" class="btn btn-primary">Request Service</button>
            <button @click.prevent="showNewServiceRequestForm = false" class="btn btn-secondary">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>

  </template>
  
  
  <script>
  import CustSearchBar from "../components/CustSearchBar.vue";
  // import Datepicker from 'vue3-datepicker';
  import axios from 'axios';
  import CustBar from '../components/CustBar.vue';
  
  export default {
    name: "CustSearch",
    components: {CustSearchBar,CustBar},
    props: {email: {type: String, required: true,}, },
    data() {
      return {
        searchPerformed: false,
        searchResults: [],
        profResults: [], 
        serviceResults: [],
        showNewServiceRequestForm: false,
      newServiceRequest: {
        cust_email: this.email,
        prof_email: '',
        sev_id: '',
        date_of_request: null,
        date_of_completion: null,
      },
      requests: [],
      services: [],
      professionals: [],
      };
    },
    async created() {
    await this.fetchServices();
    await this.fetchProfessionals();
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
    async addNewServiceRequest() {
  try {
    let your_jwt_token = localStorage.getItem('jwt');
    if (!your_jwt_token) {
      throw new Error('JWT token is missing');
    }

    const formattedRequestDate = this.formatDateOnly(this.newServiceRequest.date_of_request);
    const formattedCompletionDate = this.formatDateOnly(this.newServiceRequest.date_of_completion);

    const response = await axios.post(
      `http://127.0.0.1:8080/api/create_sevrequest/${this.email}`, 
      { 
        "cust_email": this.email,
        "prof_email": this.newServiceRequest.prof_email,
        "sev_id": this.newServiceRequest.sev_id,
        "date_of_request": formattedRequestDate,
        "date_of_completion": formattedCompletionDate,
      }, 
      {
        headers: {
          'Authorization': `Bearer ${your_jwt_token}` 
        },
        withCredentials: true
      }
    );

    if (response.status === 201) {
      console.log("Service request created successfully:", response.data);
      await this.fetchServices();

      this.requests.push({
        ...this.newServiceRequest,
        id: response.data.sevreq_id 
      });

      this.newServiceRequest = {
        cust_email: '',
        prof_email: '',
        sev_id: '',
        date_of_request: null,
        date_of_completion: null,
      };

      this.showNewServiceRequestForm = false;
    } else {
      alert("Failed to create service request: " + response.data.error);
    }
  } catch (error) {
    console.error('Error creating service request:', error);
    alert('An error occurred while creating the service request.');
  }
}, 
formatDateOnly(date) {
  if (!date) return '';
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
    },
    async fetchServices() {
    try {
      let your_jwt_token = localStorage.getItem('jwt');
      if (!your_jwt_token) {
        throw new Error('JWT token is missing');
      }
      const response = await axios.get(`http://127.0.0.1:8080/api/servicesforcust`, {
      params: {
        category: this.category,
        email: this.email 
      },
      headers: {
        'Authorization': `Bearer ${your_jwt_token}`
      },
      withCredentials: true
    });
      this.services = response.data;
    } catch (error) {
      console.error("Error fetching services:", error);
    }
  },
    async fetchProfessionals() {
      try {
        let your_jwt_token = localStorage.getItem('jwt');
        if (!your_jwt_token) {
          throw new Error('JWT token is missing');
        }
        const response = await axios.get(`http://127.0.0.1:8080/api/professionals`, {
        headers: {
          'Authorization': `Bearer ${your_jwt_token}`
        },
        withCredentials: true
      });
        this.professionals = response.data;
      } catch (error) {
        console.error("Error fetching professionals:", error);
      }
    },
    executeSearch() {
      this.searchPerformed = false;
  
      if (this.searchType === "professional") {
        this.submitSearch();
      } else if (this.searchType === "service") {
        this.searchServices();
      }
    },
    getImageUrl(id) {
      return `/static/${id}.jpeg`;
    },    

},
  computed: {
    filteredProfessionals() {
      if (!this.newServiceRequest.sev_id) {
        return []; 
      }
      const selectedService = this.services.find(
        service => service.sev_id === this.newServiceRequest.sev_id
      );

      if (!selectedService) return [];
      const filtered = this.professionals.filter(
      professional => professional.service_type == selectedService.sev_name
    );
    return filtered;
      
    }
  },
  
  watch: {
    // Reset professional email when service changes
    'newServiceRequest.sev_id'() {
      this.newServiceRequest.prof_email = '';
    }
  }
};
</script>
  
<style scoped>
.modal.show {
  display: block;
}
  .container {
    max-width: 1200px;
    margin: 0 auto;
    text-align: center;
  }
  .services {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    justify-content: center;
    margin-top: 20px;
  }
  .service-card {
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    width: 300px;
    padding: 20px;
    text-align: center;
    position: relative;
  }
  .service-card img {
    width: 120px;
    height: 100px;
    margin-bottom: 10px;
  }
  .pic {
    border-radius: 100%;
    margin-bottom: 12px;
    width: 120px;
    height: 100px;
  }

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
  
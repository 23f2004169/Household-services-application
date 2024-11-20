<template>
    <div class="container">
      <header>
        <CustBar :email="email"/>
      </header>
      <h1 class="text-white">Services for {{ category }}</h1>
      <div v-if="services && services.length > 0">
        <div class="services">
          <div class="service-card" v-for="service in services" :key="service.sev_id">
            <img :src="getImageUrl(service.sev_name)" alt="Service image" class="pic">
            <h3>{{ service.sev_name }}</h3>
            <p>{{ service.description }}</p>
            <p>Price: Rs.{{ service.price }}</p>
            <p>Time Required: {{ service.time_req }}</p>
            <p>Address: {{ service.address }}</p>
            <p>Category: {{ service.category }}</p>
            <button @click.prevent="showNewServiceRequestForm = true"  class="red"> + New Service Request </button>
          </div>
        </div>
      </div>
      <p v-else>Loading services...</p>
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
            <select v-model="newServiceRequest.sev_id" name="service" id="service" class="form-control" required>
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
            <option v-for="professional in filteredProfessionals.filter(prof => prof.approval === 'approved')" :key="professional.prof_email" :value="professional.prof_email">
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
              required/>
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

<div v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
</div>

</template>
 
<script>
import CustBar from '../components/CustBar.vue';
import axios from 'axios';

export default {
components: { CustBar},
props: ['category', 'email'], 
data() {
    return {
      showNewServiceRequestForm: false,
      newServiceRequest: {
        cust_email: this.email,
        prof_email: '',
        sev_id: '',
        date_of_request: null,
        date_of_completion: null,
      },
      services: [] , 
      requests: [],
      professionals: [],
      errorMessage: '',
    };
  },
  async created() {
    await this.fetchServices();
    await this.fetchProfessionals();
  },
  methods: {
  async addNewServiceRequest() {
  try {
    let your_jwt_token = localStorage.getItem('jwt');
    if (!your_jwt_token) {
      throw new Error('JWT token is missing');
    }

    // ensure the dates are valid Date objects
    const requestDate = new Date(this.newServiceRequest.date_of_request);
    const completionDate = new Date(this.newServiceRequest.date_of_completion);
    // validate the dates before formatting
    if (isNaN(requestDate) || isNaN(completionDate)) {
      throw new Error("Invalid date format");
    }

    const formattedRequestDate = this.formatDateOnly(requestDate);
    const formattedCompletionDate = this.formatDateOnly(completionDate);

    const response = await axios.post(`http://127.0.0.1:8080/api/create_sevrequest/${this.email}`,
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
      location.reload();

      this.showNewServiceRequestForm = false;
    }
    else if (response.status === 400) {
      this.errorMessage = "Dates must be today or in the future: " + response.data.message;
    } else {
      this.errorMessage = "Failed to create service request: " + response.data.message;
    }
  } catch (error) {
    console.error('Error creating service request:', error);
    this.errorMessage = 'Make sure you entered the correct details while creating the service request.';
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
    // reset professional email when service changes
    'newServiceRequest.sev_id'() {
      this.newServiceRequest.prof_email = '';
    },
    // watch and ensure the values remain valid Date objects
    'newServiceRequest.date_of_request'(newValue) {
      if (!(newValue instanceof Date)) {
        this.newServiceRequest.date_of_request = new Date(newValue);
      }
    },
    'newServiceRequest.date_of_completion'(newValue) {
      if (!(newValue instanceof Date)) {
        this.newServiceRequest.date_of_completion = new Date(newValue);}
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
  .alert {
  color: red;
  padding: 10px;
  background-color: #f8d7da;
  border-radius: 5px;
  margin-top: 10px;
}
</style>
  
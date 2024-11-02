<template>
    <div class="container mt-5">
      <MenuBar />
      
      <h2 class="my-4 text-white">Customers</h2>
      <div class="row">
        <div v-for="customer in customers" :key="customer.id" class="col-md-4 mb-4">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ customer.cust_email }}</h5>
              <p><strong>Address:</strong> {{ customer.address }}</p>
              <p><strong>Pincode:</strong> {{ customer.pincode }}</p>
              <div class="d-flex">
                <button @click="blockCustomer(customer.cust_email)" class="btn btn-dark btn-sm">Block/Unblock</button>
            </div>
            </div>
          </div>
        </div>
      </div> 

      <h2 class="my-4 text-white">Professionals</h2>
      <div class="row">
        <div v-for="professional in professionals" :key="professional.id" class="col-md-4 mb-4">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ professional.prof_email}}</h5>
              <p><strong>Description:</strong> {{ professional.description }}</p>
              <p><strong>Experience:</strong> {{ professional.experience }} years</p>
              <p><strong>Service Type:</strong> {{ professional.service_type }}</p>
              <div class="d-flex">
                <button @click="blockProfessional(professional.prof_email)" class="btn btn-dark btn-sm">Block/Unblock</button>
            </div>
            </div>
          </div>
        </div>
      </div>

      <h2 class="my-4 text-white">Services</h2>
      <div class="row">
        <div v-for="service in services" :key="service.id" class="col-md-4 mb-4">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ service.sev_name }}</h5>
              <p class="card-text">{{ service.description }}</p>
              <p><strong>Price:</strong> {{ service.price }}</p>
              <p><strong>Category:</strong> {{ service.category }}</p>
              <p><strong>Duration:</strong> {{ service.time_req }} minutes</p>
            </div>
          </div>
        </div>
      </div>
  
      <h2 class="my-4 text-white">Service Requests</h2>
      <div class="row">
        <div v-for="request in service_requests" :key="request.id" class="col-md-4 mb-4">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">Request ID: {{ request.sevreq_id }}</h5>
              <p><strong>Requested by:</strong> {{ request.cust_email }}</p>
              <p><strong>Status:</strong> {{ request.status }}</p>
              <p><strong>Service provider:</strong> {{ request.prof_email}}</p>
            </div>
          </div>
        </div>
      </div>

    </div>
  </template>
  


<script>
import MenuBar from '../components/MenuBar.vue';
import axios from 'axios'; 

export default {
  name: 'ExtendedView',
  components: { MenuBar },
  data() {
    return {
      services: [], 
      professionals: [] ,
      customers: [],
      service_requests: [],
    }
  },
  created() {
    this.fetchServices();
    this.fetchServiceRequests();
    this.fetchProfessionals();
    this.fetchCustomers();
  },
  methods: {
    async fetchCustomers() {
      try {
        const response = await axios.get('http://127.0.0.1:8080/api/customers');
        if (response.status === 200) {
          this.customers = response.data; // Update the services array with the data from the backend
        } else {
          console.error("Failed to fetch customers:", response.data.error);
        }
      } catch (error) {
        console.error('Error fetching customers:', error.message);
      }
    },
    async fetchProfessionals() {
      try {
        const response = await axios.get('http://127.0.0.1:8080/api/professionals');
        if (response.status === 200) {
          this.professionals = response.data; // Update the services array with the data from the backend
        } else {
          console.error("Failed to fetch professionals:", response.data.error);
        }
      } catch (error) {
        console.error('Error fetching professionals:', error.message);
      }
    },
    async fetchServices() {
      try {
        const response = await axios.get('http://127.0.0.1:8080/api/services');
        if (response.status === 200) {
          this.services = response.data; // Update the services array with the data from the backend
        } else {
          console.error("Failed to fetch services:", response.data.error);
        }
      } catch (error) {
        console.error('Error fetching services:', error.message);
      }
    },
  async fetchServiceRequests() {
    try {
      const response = await axios.get('http://127.0.0.1:8080/api/service_requests');
      if (response.status === 200) {
        this.service_requests = response.data; // Update the services array with the data from the backend
      } else {
        console.error("Failed to fetch service requests:", response.data.error);
      }
    } catch (error) {
      console.error('Error fetching service requests:', error.message);
  }
  },
  async blockProfessional(prof_email) {
      try {
      if (!prof_email) {
        console.error("Professional email is undefined");
        return;
      }         
      const response = await axios.post(`http://127.0.0.1:8080/api/professional/block/${prof_email}`);

      if (response.status === 200) {  // Check if the update was successful
        console.log("Professional blocked successfully:", response.data);
        location.reload();

      } else {          
        console.error("Failed to block professional: " + response.data.error);
      }
    } catch (error) {
      console.error('Error blocking professional:', error.message);
    } 
  },
  async blockCustomer(cust_email) {
      try {
      if (!cust_email) {
        console.error("Customer email is undefined");
        return;
      }         
      const response = await axios.post(`http://127.0.0.1:8080/api/customer/block/${cust_email}`);

      if (response.status === 200) {  // Check if the update was successful             
        console.log("Customer blocked successfully:", response.data);
        location.reload();  

      } else {
        console.error("Failed to block customer: " + response.data.error);
      }
    } catch (error) {
      console.error('Error blocking customer:', error.message);
    }
  },
},
}

</script>


<style>
.card {
  border-radius: 8px;
}

.card-title {
  font-size: 1.25rem;
}
</style>

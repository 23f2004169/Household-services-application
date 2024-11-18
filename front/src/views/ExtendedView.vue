<template>
    <div class="container mt-5">
      <MenuBar />
      <h2 class="my-4 text-white">Professionals</h2>
      <div class="row">
        <div v-for="professional in professionals" :key="professional.id" class="col-md-4 mb-4">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">Email id:{{ professional.prof_email}}</h5>
                <!-- <img id="image"src="http://127.0.0.1:8080/api/view-image/{{ professional.prof_email }}"   alt="Profile Picture" class="profile-pic" @error="handleImageError" /> -->
                <img :src="'http://127.0.0.1:8080/api/view-image/' + professional.prof_email" alt="Profile Picture" class="pic" />
                <p><strong>Description:</strong> {{ professional.description }}</p>
              <p><strong>Experience:</strong> {{ professional.experience }} years</p>
              <p><strong>Date of Registration:</strong> {{ professional.date_created}}</p>
              <p><strong>Service Type:</strong> {{ professional.service_type }}</p>
              <p><strong>Mobile no:</strong> {{ professional.phone }}</p>
              <p><strong>Address:</strong> {{ professional.address }}</p>
              <p><strong>Pincode:</strong> {{ professional.pincode }}</p>
              <p><strong>Rating:</strong> {{ professional.rating }}</p>
              <p><strong>Approval Status:</strong> {{ professional.approval }}</p>
              <p><strong>Block Status:</strong> {{ professional.blocked }}</p>
              <div class="d-flex">
                <button @click="blockProfessional(professional.prof_email)" class="btn btn-dark btn-sm">Block/Unblock</button>
                <button @click="viewDocument(professional.prof_email)" class="btn btn-primary btn-sm">View</button> 
                <button @click="deleteProfessional(professional.prof_email)" class="btn btn-danger btn-sm">Delete user</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <h2 class="my-4 text-white">Customers</h2>
      <div class="row">
        <div v-for="customer in customers" :key="customer.id" class="col-md-4 mb-4">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">Email id:{{ customer.cust_email }}</h5>
              <p><strong>Address:</strong> {{ customer.address }}</p>
              <p><strong>Pincode:</strong> {{ customer.pincode }}</p>
              <p><strong>Mobile no:</strong> {{ customer.phone }}</p>
              <p><strong>Block status:</strong>{{customer.blocked }}</p>
              <div class="d-flex">
                <button @click="blockCustomer(customer.cust_email)" class="btn btn-dark btn-sm">Block/Unblock</button>
                <button @click="deleteCustomer(customer.cust_email)" class="btn btn-danger btn-sm">Delete User</button>
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
              <h5 class="card-title">Name:{{ service.sev_name }}</h5>
               <p><strong>Service id:</strong>{{service.sev_id}}</p>
               <img :src="getImageUrl(service.sev_name)" alt="Service image" class="pic">
              <p class="card-text">{{ service.description }}</p>
              <p><strong>Price:</strong> {{ service.price }}</p>
              <p><strong>Category:</strong> {{ service.category }}</p>
              <p><strong>Duration:</strong> {{ service.time_req }} minutes</p>
              <p><strong>Address:</strong> {{ service.address }}</p>
              <p><strong>Pincode:</strong> {{ service.pincode }}</p>
              <div class="d-flex">
                    <button @click.prevent="deleteService(service.sev_id)" class="btn btn-danger btn-sm">Delete</button>
              </div>
            </div>
          </div>
        </div>
      </div>
 
      <h2 class="my-4 text-white">Service Requests</h2>
      <div class="row">
        <div v-for="request in service_requests" :key="request.id" class="col-md-4 mb-4">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">Request id: {{ request.sevreq_id }}</h5>
              <p><strong>Requested by:</strong> {{ request.cust_email }}</p>
              <p><strong>Status:</strong> {{ request.status }}</p>
              <p><strong>Service provider:</strong> {{ request.prof_email}}</p>
              <p><strong>Remarks:</strong> {{ request.remarks }}</p>
              <p><strong>Rating:</strong> {{ request.rating }}</p>
              <p><strong>Service ID:</strong> {{ request.sev_id }}</p>
              <p><strong>Date of Request:</strong> {{ request.date_of_request }}</p>
              <p><strong>Date of Completion:</strong> {{ request.date_of_completion }}</p>
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
        let your_jwt_token = localStorage.getItem('jwt');
        const response = await axios.get('http://127.0.0.1:8080/api/customers',
        {
          headers: {
            'Authorization': `Bearer ${your_jwt_token}`
          },
          withCredentials: true
        }
        );
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
        let your_jwt_token = localStorage.getItem('jwt');
        const response = await axios.get('http://127.0.0.1:8080/api/professionals',
        {
          headers: {
            'Authorization': `Bearer ${your_jwt_token}`
          },
          withCredentials: true
        }
        );
        if (response.status === 200) {
          this.professionals = response.data; // Update the services array with the data from the backend
          console.log(this.professionals);
        } else {
          console.error("Failed to fetch professionals:", response.data.error);
        }
      } catch (error) {
        console.error('Error fetching professionals:', error.message);
      }
    },
    async fetchServices() {
      try {
        let your_jwt_token = localStorage.getItem('jwt');
        const response = await axios.get('http://127.0.0.1:8080/api/services',
        {
          headers: {
            'Authorization': `Bearer ${your_jwt_token}`
          },
          withCredentials: true
        }
        );
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
      let your_jwt_token = localStorage.getItem('jwt');
      const response = await axios.get('http://127.0.0.1:8080/api/service_requests',
      {
        headers: {
          'Authorization': `Bearer ${your_jwt_token}`
        },
        withCredentials: true
      }
      );
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
      let your_jwt_token = localStorage.getItem('jwt');
      if (!your_jwt_token) {    
        throw new Error('JWT token is missing');
      }
      console.log("Professional email ", prof_email);       
      const response = await axios.post(`http://127.0.0.1:8080/api/professional/block/${prof_email}`,
      {},
      {
        headers: {
          'Authorization': `Bearer ${your_jwt_token}` 
        },
        withCredentials: true
      }
      );

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
  async deleteProfessional(prof_email) {
    try {
      const your_jwt_token = localStorage.getItem('jwt');
      if (!your_jwt_token) {
        throw new Error('JWT token is missing');
      }
      const response = await axios.delete(`http://127.0.0.1:8080/api/professional/delete/${prof_email}`, {
        headers: {
          'Authorization': `Bearer ${your_jwt_token}`
        },
        withCredentials: true
      });

      if (response.status === 200) {
        console.log("Professional deleted successfully:", response.data);
        this.professionals = this.professionals.filter(professional => professional.prof_email !== prof_email);
      } else {
        console.error("Failed to delete professional: " + response.data.error);
      }
    } catch (error) {
      console.error('Error deleting professional:', error.message);
    }
  },
  async blockCustomer(cust_email) {
      try {
      let your_jwt_token = localStorage.getItem('jwt');
      if (!your_jwt_token) {
        throw new Error('JWT token is missing');
      }  
      console.log("Customer email ", cust_email);     
      const response = await axios.post(`http://127.0.0.1:8080/api/customer/block/${cust_email}`, {},
      {
        headers: {
          'Authorization': `Bearer ${your_jwt_token}` 
        },
        withCredentials: true
      });

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
  async deleteCustomer(cust_email){
    try {
      const your_jwt_token = localStorage.getItem('jwt');
      if (!your_jwt_token) {
        throw new Error('JWT token is missing');
      }
      const response = await axios.delete(`http://127.0.0.1:8080/api/customer/delete/${cust_email}`, {
        headers: {
          'Authorization': `Bearer ${your_jwt_token}`
        },
        withCredentials: true
      });

      if (response.status === 200) {
        console.log("Customer deleted successfully:", response.data);
        this.customers = this.customers.filter(customer => customer.cust_email !== cust_email);
      } else {
        console.error("Failed to delete professional: " + response.data.error);
      }
    } catch (error) {
      console.error('Error deleting professional:', error.message);
    }
  },
  async deleteService(sev_id) {
  if (confirm("Are you sure you want to delete this service?")) {
    try {
      let your_jwt_token = localStorage.getItem('jwt');
      if (!your_jwt_token) {
        throw new Error('JWT token is missing');
      }
      const response = await axios.delete(`http://127.0.0.1:8080/api/delete_sev/${sev_id}`,
      {
        headers: {
          Authorization: `Bearer ${ your_jwt_token }`
        },
        withCredentials: true
      }
      );
      if (response.status === 200) {
        console.log("Service deleted successfully:", response.data);
        this.services = this.services.filter(service => service.sev_id !== sev_id);
      } else {
        alert("Failed to delete service: " + response.data.error);
      }
    } catch (error) {
      console.error("Error deleting service:", error.message);
      alert("An error occurred while deleting the service.");
    }
  }
},
  viewDocument(prof_email) {
      // Open document in new tab
      const documentUrl = `http://127.0.0.1:8080/api/view-document/${prof_email}`;
      window.open(documentUrl, '_blank');
    },
    getImageUrl(id) {
      return `/static/${id}.jpeg`;
    }
},
}

</script>


<style>
.card {
  border-radius: 8px;
}
.pic {
    border-radius: 100%;
    margin-bottom: 12px;
    width: 100px;
    height: 100px;
  }
.card-title {
  font-size: 1.25rem;
}
</style>

<template>
  <header>
    <ProfBar :email="email"/>
  </header>
  <div>
    <button @click="toggleProfileCard" class="btn btn-primary">View your ProfileCard</button>
    <div v-if="isProfileCardVisible">
      <ProfileCard :email="email" />
    </div>
  </div>

   <section class="service-section mt-4">
    <h3 class="text-white">Service Requests TODAY</h3>

      <table class="table table-bordered">
        <thead>
          <tr>
            <th>ID</th>
            <th>Customer ID</th>
            <th>Request Date</th>
            <th>Completion Date</th>
            <th>Status</th>
            <th>Remarks</th>
            <th>Service ID</th>
            <th>Actions</th>
          </tr>
        </thead>
      
        <tbody>
          <tr v-for="(service, index) in service_requests_today" :key="index">
            <td>{{ service.sevreq_id }}</td>
            <td>{{ service.cust_email }}</td>
            <td>{{ service.date_of_request }}</td>
            <td>{{ service.date_of_completion }}</td>
            <td>{{ service.sev_status }}</td>
            <td>{{ service.remarks }}</td>
            <td>{{ service.sev_id }}</td>
            <td >
              <button @click="acceptService(service.sevreq_id)" class="btn btn-success">Accept</button>
              <button @click="rejectService(service.sevreq_id)" class="btn btn-danger">Reject</button>
              <button @click="closeService(service.sevreq_id)" class="btn btn-warning">Close</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <section class="service-section mt-4">
    <h3 class="text-white">Closed Service Requests </h3>

      <table class="table table-bordered">
        <thead>
          <tr>
            <th>ID</th>
            <th>Customer ID</th>
            <th>Request Date</th>
            <th>Completion Date</th>
            <th>Status</th>
            <th>Remarks</th>
            <th>Service ID</th>
            <th>Rating</th>
          </tr>
        </thead>
      
        <tbody>
          <tr v-for="(service, index) in closed_service_requests" :key="index">
            <td>{{ service.sevreq_id }}</td>
            <td>{{ service.cust_email }}</td>
            <td>{{ service.date_of_request }}</td>
            <td>{{ service.date_of_completion }}</td>
            <td>{{ service.sev_status }}</td>
            <td>{{ service.remarks }}</td>
            <td>{{ service.sev_id }}</td>
            <td>{{ service.rating }}</td>
      
          </tr>
        </tbody>
      </table>
    </section>
</template>
    
<script>
import axios from 'axios';
import ProfBar from '../components/ProfBar.vue';
import ProfileCard from '../components/ProfileCard.vue';
      
export default {
    components: { ProfileCard,ProfBar},
    name: 'ProfDash',
    data() {
        return {
          isProfileCardVisible: false ,
            service_requests_today: [],
            closed_service_requests: [],
          };
        },
    props: ['email'],
    created() {
    this.fetchTodayServiceRequests();
    this.fetchClosedServices();  },  
    mounted() {
    console.log('ProfDashboard received email:', this.email); },
    methods: {  toggleProfileCard() {
      this.isProfileCardVisible = !this.isProfileCardVisible; 
    },
      async fetchTodayServiceRequests() {
        try {
           const response = await axios.get(`http://127.0.0.1:8080/api/prof_sevs_today/${this.email}`);
           if (response.status === 200) {
             this.service_requests_today = response.data; 
           } else {
             console.error("Failed to fetch service requests:", response.data.error);
           }
        } catch (error) {
           console.error('Error fetching service requests:', error.message);
        }
    },
    async fetchClosedServices() {
        try {
           const response = await axios.get(`http://127.0.0.1:8080/api/prof_closed_sevs/${this.email}`);
           console.log("Response:", response.data, "email:",this.email);
           if (response.status === 200) {
             this.closed_service_requests = response.data; 
           } else {
             console.error("Failed to fetch service requests:", response.data.error);
           }
        } catch (error) {
           console.error('Error fetching service requests:', error.message);}
    },
    async acceptService(sevreq_id) {
      try {
        const response = await axios.post(`http://127.0.0.1:8080/api/prof_accept_sev/${sevreq_id}`);
        if (response.status === 200) {
          console.log("Service request accepted successfully:", response.data);
          location.reload();

        } else {
          console.error("Failed to accept service request:", response.data.error);
        }
      } catch (error) {
        console.error('Error accepting service request:', error.message);
      }
    },
    async rejectService(sevreq_id) {
      try {
        const response = await axios.post(`http://127.0.0.1:8080/api/prof_reject_sev/${sevreq_id}`); 
        if (response.status === 200) {
          console.log("Service request rejected successfully:", response.data);
          location.reload();

        } else {
          console.error("Failed to reject service request:", response.data.error);
        }
      } catch (error) {
        console.error('Error rejecting service request:', error.message);
      }
        },
    async closeService(sevreq_id) {
      try {
        const response = await axios.post(`http://127.0.0.1:8080/api/prof_close_sev/${sevreq_id}`); 
        if (response.status === 200) {
          console.log("Service request closed successfully:", response.data);
          location.reload();

        } else {
          console.error("Failed to close service request:", response.data.error);
        }
      } catch (error) {
        console.error('Error closing service request:', error.message);
      }
        },
    }
    }
</script>

<style scoped>
.header {
  background-color: #f0f9ff;
  border-bottom: 2px solid #ddd;
}
.nav-link {
  margin-right: 15px;
  color: #555;
  font-weight: bold;
  text-decoration: none;
}
.nav-link:hover {
  color: #007bff;
  text-decoration: underline;
}

.container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem;
      }
      .table {
    color:red;
    width: 100%;
    margin-top: 1rem;
    box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
  }
  .table-bordered th, .table-bordered td {
    border: 1px solid #ccc;
    padding: 12px;
  }
  .service-section h3 {
    margin-bottom: 15px;
    color: #333;
  }
</style>


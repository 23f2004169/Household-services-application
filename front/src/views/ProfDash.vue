<template>

  <header  v-if="prof_data.approval === 'approved'">
    <ProfBar :email="email"/>
  </header>

  <h2 class="text-white">Welcome Professional</h2>
  <p class="text-white">Your email: {{ email }}</p>  
  <p class="text-white">Your rating: {{ rating }}</p>
  <div>
    <button @click="toggleProfileCard" style="background-color: rgb(63, 35, 18);">View your ProfileCard</button>
    <div v-if="isProfileCardVisible">
      <ProfileCard :email="email" />
    </div>
  </div>
  <br><br>

  <div>
  <div v-if="prof_data.approval === 'pending'" class="alert alert-warning text-center mt-4">
       <h4>Your account is under verification.</h4>
       <div class="d-flex justify-content-end mt-3">
  <router-link :to="{ path: '/login' }">
    <button class="btn btn-danger">Logout</button>
  </router-link>
</div>

  </div>

  <div v-else-if="prof_data.approval === 'rejected'" class="alert alert-danger text-center mt-4">
        <h4>Your profile has been rejected.</h4>
        <div class="d-flex justify-content-end mt-3">
  <router-link :to="{ path: '/login' }">
    <button class="btn btn-danger">Logout</button>
  </router-link>
</div>

  </div>

  <div v-else-if="prof_data.approval === 'approved'">

  <!-- Service Requests Today: -->
  <div>
  <div v-if="service_requests_today.length > 0">
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
    </div>
    <div v-else>
      <h3 class="text-white">Service Requests TODAY</h3>
      <p class="text-white">No service requests today</p>
    </div>
  </div>

  <br><br>
  <!-- Closed Service Requests : -->
  <div>
  <div v-if="closed_service_requests.length > 0">
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
    </div>
    <div v-else>
        <h3 class="text-white">Closed Service Requests</h3>
        <p class="text-white">No closed requests</p>
      </div>
  </div>
  
  <br><br>
  <!-- Pending Service Requests : -->
  <div>
    <div v-if="service_requests.length > 0">
      <section class="service-section mt-4">
      <h3 class="text-white">Pending Service Requests </h3>
  
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
              <th>Actions</th>
            </tr>
          </thead>
        
          <tbody>
            <tr v-for="(service_request, index) in service_requests"  :key="index">
              <td>{{ service_request.sevreq_id }}</td>
              <td>{{ service_request.cust_email }}</td>
              <td>{{ service_request.date_of_request }}</td>
              <td>{{ service_request.date_of_completion }}</td>
              <td>{{ service_request.sev_status }}</td>
              <td>{{ service_request.remarks }}</td>
              <td>{{ service_request.sev_id }}</td>
              <td>{{ service_request.rating }}</td>
              <td >
                <button @click="acceptService(service_request.sevreq_id)" class="btn btn-success">Accept</button>
                <button @click="rejectService(service_request.sevreq_id)" class="btn btn-danger">Reject</button>
                <button @click="closeService(service_request.sevreq_id)" class="btn btn-warning">Close</button>
              </td>
            </tr>
          </tbody>
        </table>
      </section>
  </div>
  <div v-else>
        <h3 class="text-white">Pending Service Requests</h3>
        <p class="text-white">No pending service requests </p>
  </div>
  </div>

  </div>  
</div>
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
          rating: null,
          isProfileCardVisible: false ,
            service_requests_today: [],
            closed_service_requests: [],
            service_requests: [],
            prof_data: [],
          };
        },
    props: ['email'],
    created() {
    this.fetchTodayServiceRequests();
    this.fetchClosedServices(); 
    this.fetchRating(); 
    this.fetchProf();
    this.fetchServiceRequests();

  },  
    mounted() {
    console.log('ProfDashboard received email:', this.email); },
    methods: {  toggleProfileCard() {
      this.isProfileCardVisible = !this.isProfileCardVisible; 
    },
    async fetchRating() {
      try {
        let your_jwt_token = localStorage.getItem('jwt');
        if (!your_jwt_token) {
          throw new Error('JWT token is missing');
        }
        const response = await axios.post(`http://127.0.0.1:8080/api/prof_rating/${this.email}`,{},
          {
            headers: {
              'Authorization': `Bearer ${your_jwt_token}`
            },
            withCredentials: true
          }
        );
        if (response.status === 200) {
          this.rating= response.data; 
          console.log("Professional rating updated successfully:", response.data);
        } else {
          console.error("Failed to update rating:", response.data.error);
        }
      } catch (error) {
        console.error("Error fetching rating:", error.message);
      }
    },
      async fetchTodayServiceRequests() {
        try {
           let your_jwt_token = localStorage.getItem('jwt');
           if (!your_jwt_token) {
             throw new Error('JWT token is missing');
           }
           const response = await axios.get(`http://127.0.0.1:8080/api/prof_sevs_today/${this.email}`,
             {
               headers: {
                 'Authorization': `Bearer ${your_jwt_token}`
               },
               withCredentials: true
             }
           );
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
           let your_jwt_token = localStorage.getItem('jwt');
           if (!your_jwt_token) {
             throw new Error('JWT token is missing');
           }
           const response = await axios.get(`http://127.0.0.1:8080/api/prof_closed_sevs/${this.email}`,
             {
               headers: {
                 'Authorization': `Bearer ${your_jwt_token}`
               },
               withCredentials: true
             }
           );
          //  console.log("Response:", response.data, "email:",this.email);
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
        let your_jwt_token = localStorage.getItem('jwt');
        if (!your_jwt_token) {
          throw new Error('JWT token is missing');
        }
        const response = await axios.post(`http://127.0.0.1:8080/api/prof_accept_sev/${sevreq_id}`,{},
          {
            headers: {
              'Authorization': `Bearer ${your_jwt_token}`
            },
            withCredentials: true
          }
        );
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
        let your_jwt_token = localStorage.getItem('jwt');
        if (!your_jwt_token) {  
          throw new Error('JWT token is missing');
        }
        const response = await axios.post(`http://127.0.0.1:8080/api/prof_reject_sev/${sevreq_id}`,{},
          {
            headers: {
              'Authorization': `Bearer ${your_jwt_token}`
            },
            withCredentials: true
          }
        ); 
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
        let your_jwt_token = localStorage.getItem('jwt');
        if (!your_jwt_token) {
          throw new Error('JWT token is missing');
        }
        const response = await axios.post(`http://127.0.0.1:8080/api/prof_close_sev/${sevreq_id}`,{},
          {
            headers: {
              'Authorization': `Bearer ${your_jwt_token}`
            },
            withCredentials: true
        }); 
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
        async fetchProf() {
      try {
        let your_jwt_token = localStorage.getItem('jwt');
        if (!your_jwt_token) {
          throw new Error('JWT token is missing');
        }
        const response = await axios.get(`http://127.0.0.1:8080/api/professional/${this.email}`, {
          headers: {
            'Authorization': `Bearer ${your_jwt_token}`
          },
          withCredentials: true
        });
        console.log(this.email,response.data);
        if (response.status === 200) {
          this.prof_data = response.data; // Update the services array with the data from the backend
        } else {
          console.error("Failed to fetch professionals:", response.data.error);
        }
      } catch (error) {
        console.error('Error fetching professionals:', error.message);
      }
    },
    async fetchServiceRequests(){
      try {
        let your_jwt_token = localStorage.getItem('jwt');
        if (!your_jwt_token) {
          throw new Error('JWT token is missing');
        }
        const response = await axios.get(`http://127.0.0.1:8080/api/prof_pending_sevs/${this.email} `, {
          headers: {
            'Authorization': `Bearer ${your_jwt_token}`
          },
          withCredentials: true
        });
        if (response.status === 200) {
          this.service_requests = response.data; // Update the services array with the data from the backend
          console.log("Service requests fetched successfully:", response.data);
        } else {
          console.error("Failed to fetch service requests:", response.data.error);
        }
      } catch (error) {
        console.error('Error fetching service requests:', error.message);
      }
    }
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


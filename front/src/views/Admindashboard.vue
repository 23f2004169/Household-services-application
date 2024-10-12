<template>
    <div class="admin-dashboard">
      <header>
        <h2>Welcome to Admin</h2>
        <nav>
          <router-link to="/">Home</router-link>
          <router-link to="/search">Search</router-link>
          <router-link to="/summary">Summary</router-link>
          <router-link to="/logout">Logout</router-link>
        </nav>
      </header>
  
      <main>
        <!-- Services Table -->
        <section class="services-section">
          <h3>Services</h3>
          <button @click="showNewServiceForm = true" class="add-service-btn">+ New Service</button>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Service Name</th>
                <th>Base Price</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(service, index) in services" :key="index">
                <td>{{ service.id }}</td>
                <td>{{ service.name }}</td>
                <td>{{ service.basePrice }}</td>
                <td>
                  <button @click="editService(service.id)">Edit</button>
                  <button @click="deleteService(service.id)">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </section>
  
        <!-- Professionals Table -->
        <section class="professionals-section">
          <h3>Professionals</h3>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Experience (Yrs)</th>
                <th>Service Name</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(professional, index) in professionals" :key="index">
                <td>{{ professional.id }}</td>
                <td>{{ professional.name }}</td>
                <td>{{ professional.experience }}</td>
                <td>{{ professional.serviceName }}</td>
                <td>
                  <button @click="approveProfessional(professional.id)">Approve</button>
                  <button @click="rejectProfessional(professional.id)">Reject</button>
                </td>
              </tr>
            </tbody>
          </table>
        </section>
  
        <!-- Service Requests Table -->
        <section class="requests-section">
          <h3>Service Requests</h3>
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Assigned Professional</th>
                <th>Requested Date</th>
                <th>Status (R/A/C)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(request, index) in requests" :key="index">
                <td>{{ request.id }}</td>
                <td>{{ request.professional }}</td>
                <td>{{ request.requestedDate }}</td>
                <td>{{ request.status }}</td>
              </tr>
            </tbody>
          </table>
        </section>
      </main>
  
      <!-- New Service Form Modal -->
      <div v-if="showNewServiceForm" class="new-service-form">
        <h3>New Service</h3>
        <form @submit.prevent="addNewService">
          <label>Service Name:</label>
          <input v-model="newService.name" type="text" required>
  
          <label>Description:</label>
          <textarea v-model="newService.description" required></textarea>
  
          <label>Base Price:</label>
          <input v-model="newService.basePrice" type="number" required>
  
          <div class="form-actions">
            <button type="submit">Add</button>
            <button @click="showNewServiceForm = false">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        services: [],          // List of services
        professionals: [],     // List of professionals
        requests: [],          // List of service requests
        showNewServiceForm: false, // Controls the visibility of the new service form modal
        newService: {
          name: '',
          description: '',
          basePrice: ''
        }
      };
    },
    methods: {
      addNewService() {
        // Logic to add a new service
        console.log("Adding new service", this.newService);
        this.services.push({ ...this.newService, id: this.services.length + 1 });
        this.showNewServiceForm = false;
      },
      editService(serviceId) {
        // Logic to edit a service
        console.log("Editing service with ID:", serviceId);
      },
      deleteService(serviceId) {
        // Logic to delete a service
        console.log("Deleting service with ID:", serviceId);
      },
      approveProfessional(professionalId) {
        // Logic to approve a professional
        console.log("Approving professional with ID:", professionalId);
      },
      rejectProfessional(professionalId) {
        // Logic to reject a professional
        console.log("Rejecting professional with ID:", professionalId);
      }
    }
  };
  </script>
  
  <style scoped>
  .admin-dashboard {
    padding: 20px;
  }
  
  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  nav a {
    margin-right: 10px;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }
  
  table, th, td {
    border: 1px solid #ddd;
  }
  
  th, td {
    padding: 8px;
    text-align: left;
  }
  
  .add-service-btn {
    margin-bottom: 10px;
  }
  
  .new-service-form {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    padding: 20px;
    background-color: #fff;
    border: 1px solid #ddd;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .form-actions {
    margin-top: 10px;
  }
  
  button {
    margin-right: 10px;
  }
  </style>
  
<template>
    <section class="service-section mt-4">
      <h3>{{ title }}</h3>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>ID</th>
            <th>Customer Name</th>
            <th>Contact Phone</th>
            <th>Location (Pin Code)</th>
            <th v-if="actionColumn">Action</th>
            <th v-if="ratingColumn">Date</th>
            <th v-if="ratingColumn">Rating</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(service, index) in services" :key="index">
            <td>{{ service.id }}</td>
            <td>{{ service.customerName }}</td>
            <td>{{ service.phone }}</td>
            <td>{{ service.location }}</td>
            <td v-if="actionColumn">
              <button @click="acceptService(service.id)" class="btn btn-success">Accept</button>
              <button @click="rejectService(service.id)" class="btn btn-danger">Reject</button>
            </td>
            <td v-if="ratingColumn">{{ service.date }}</td>
            <td v-if="ratingColumn">{{ service.rating }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  </template>
  
  <script>
  export default {
    name:'ServiceTable',
    props: {
      title: String,
      services: Array,
      actionColumn: Boolean,
      ratingColumn: Boolean
    },
    methods: {
      acceptService(id) {
        console.log("Service accepted:", id);
      },
      rejectService(id) {
        console.log("Service rejected:", id);
      }
    }
  };
  </script>
  
  <style scoped>
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
  
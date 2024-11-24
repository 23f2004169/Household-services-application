<template>
    <div class="container mt-0">
      <header class="d-flex justify-content-between align-items-center mb-4">
        <CustBar  :email="email"/>
      </header>
    </div>
    <div>
      <h2 style="color:white">Service Request Status Histogram</h2>
      <canvas id="professionalServiceRequestHistogram"></canvas>
    </div>
    <div>
      <h2 style="color:white">Service Request Ratings Histogram</h2>
      <canvas id="professionalServiceRequestRatingHistogram"></canvas>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import CustBar from '../components/CustBar.vue';
  import { Chart, BarController, BarElement, CategoryScale, LinearScale } from 'chart.js';
  Chart.register(BarController, BarElement, CategoryScale, LinearScale);
  
  export default {
    name: "CustSummary",
    components: { CustBar },
    props: {
      email: {type: String, required: true,},
        },
    data() {
      return {
        statusChart: null,
        ratingChart: null,
        statusCounts: {
          accepted: 0,
          rejected: 0,
          requested: 0,
          closed: 0,
        },
        ratingCounts: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 },
      };
    },
    
    methods: {
      async fetchData() {
        try {
          let your_jwt_token = localStorage.getItem('jwt');
          if (!your_jwt_token) {
            throw new Error('JWT token is missing');
          }
          const response = await axios.get(`http://127.0.0.1:8080/api/cust_summary/${this.email}`,
          {
            headers: {
              'Authorization': `Bearer ${your_jwt_token}`
            },
            withCredentials: true
          }
          );
          const data = response.data.requests;
  
          if (data && Array.isArray(data)) {
            data.forEach(item => {
              if (item.sev_status in this.statusCounts) {
                this.statusCounts[item.sev_status]++;
              }
              
              const rating = parseInt(item.rating);
              if (rating >= 1 && rating <= 5) {
                this.ratingCounts[rating]++;
              }
            });
  
            this.renderStatusChart();
            this.renderRatingChart();
          } else {
            console.error("Data format issue:", data);
          }
        } catch (error) {
          console.error("Error fetching data:", error);
        }
      },
      renderStatusChart() {
        const ctx = document.getElementById("professionalServiceRequestHistogram").getContext("2d");
        if (this.statusChart) {
          this.statusChart.destroy();
        }
        this.statusChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ["accepted", "rejected","requested", "closed"],
            datasets: [
              {
                label: "Service Request Status",
                data: Object.values(this.statusCounts),
                backgroundColor: ["#4caf50", "#f44336","#2196f3", "#ff9800"],
                borderWidth: 1,
              },
            ],
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                display: true,
                position: "top",
              },
            },
            scales: {
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: "Number of Requests",
                  color: "white",
                },
                ticks: {
                       color: "white", 
              },
              },
              x: {
                title: {
                  display: true,
                  text: "Status",
                  color: "white",
                },
                ticks: {
                       color: "white", 
              },
              },
            },
          },
        });
      },
  
      renderRatingChart() {
        const ctx = document.getElementById("professionalServiceRequestRatingHistogram").getContext("2d");
        if (this.ratingChart) {
          this.ratingChart.destroy();
        }
        this.ratingChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['1', '2', '3', '4', '5'],
            datasets: [
              {
                label: "Service Request Ratings",
                data: Object.values(this.ratingCounts),
                backgroundColor: ["#f44336", "#ff9800", "#ffeb3b", "#8bc34a", "#4caf50"],
                borderWidth: 1,
              },
            ],
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                display: true,
                position: "top",
              },
            },
            scales: {
              y: {
                beginAtZero: true,
                title: {
                  display: true,
                  text: "Number of Requests",
                  color: "white",
                },
                ticks: {
                       color: "white", 
              },
              },
              x: {
                title: {
                  display: true,
                  text: "Rating",
                  color: "white",
                },
                ticks: {
                       color: "white", 
              },
              },
            },
          },
        });
      },
    },
    
    mounted() {
      this.fetchData();
    },
  };
  </script>
  
  <style scoped>
  #professionalServiceRequestHistogram, #professionalServiceRequestRatingHistogram {
    max-width: 600px;
    margin: auto;
  } 
  </style>
  
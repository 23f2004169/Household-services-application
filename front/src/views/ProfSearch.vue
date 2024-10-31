<template>
    <div class="container mt-0">
          <header class="d-flex justify-content-between align-items-center mb-4">
            <ProfBar  :email="email" />
          </header>
    </div>
    </template>
    
    <script>
      import axios from 'axios';
      import ProfBar from '../components/ProfBar.vue';
      
      export default {
        name: "ProfSearch",
        components: { ProfBar },
        
        props: {
          email: {type: String, required: true,},
            },
      };
    </script>
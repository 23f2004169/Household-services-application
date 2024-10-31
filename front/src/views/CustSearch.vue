<template>
<div class="container mt-0">
      <header class="d-flex justify-content-between align-items-center mb-4">
        <CustBar  :email="email" />
      </header>
</div>
</template>

<script>
  import axios from 'axios';
  import CustBar from '../components/CustBar.vue';
  
  export default {
    name: "CustSearch",
    components: { CustBar },
    
    props: {
      email: {type: String, required: true,},
        },
  };
</script>
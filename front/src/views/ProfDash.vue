<template>
    <div>
        <ProfileCard />

        <main class="container mt-4">
            <ServiceTable 
              title="Today Services" 
              :services="todayServices" 
              :actionColumn="true"
              :ratingColumn="false"
            />
            <ServiceTable 
              title="Closed Services" 
              :services="closedServices" 
              :actionColumn="false"
              :ratingColumn="true"
            />
        </main>
    </div>
</template>
    
<script>
import ProfileCard from '../components/ProfileCard.vue';
import ProServices from '../components/ProServices.vue';
import ServiceTable from '../components/ServiceTable.vue';
      
export default {
    components: {
    ServiceTable,
    ProfileCard,
    ProServices
    },
    data() {
        return {
            todayServices: [
              { id: 1, customerName: 'John Doe', phone: '1234567890', location: '12345' },
              { id: 2, customerName: 'Jane Doe', phone: '0987654321', location: '67890' }
            ],
            closedServices: [
              { id: 1, customerName: 'Anna Smith', phone: '1112223333', location: '54321', date: '2024-10-12', rating: 4.5 },
              { id: 2, customerName: 'Mark Taylor', phone: '4445556666', location: '98765', date: '2024-10-11', rating: 5 }
            ]
          };
        }
      };
</script>
      
<style scoped>
      .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 1rem;
      }
</style>


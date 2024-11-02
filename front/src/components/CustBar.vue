<template>
    <nav class="navbar bg-body-tertiary fixed-top" style="background-color:  rgb(63, 35, 18);">
        <div class="container-fluid" style="background-color:  rgb(63, 35, 18);">
            <a class="navbar-brand" style="color:white">CUSTOMER DASHBOARD</a>
            <router-link :to="{ path: '/cust_dashboard', query: { email: email } }">
              <button style="background-color: rgb(63, 35, 18);">Home</button>
            </router-link> 
            
            <router-link :to="{ path: '/cust_search', query: { email: email } }">
              <button style="background-color: rgb(63, 35, 18);">Search</button>
            </router-link> 
            
            <router-link :to="{ path: '/cust_summary', query: { email: email } }">
              <button style="background-color: rgb(63, 35, 18);">Summary</button>
            </router-link> 
            
            <router-link :to="{ path: '/login' }">
              <button style="background-color: rgb(63, 35, 18);">Logout</button>
            </router-link>
        </div>
    </nav>
</template>

<style scoped>
 body {padding-top: 70px;background-color: rgb(63, 35, 18)!important; }
    .header {text-align: center;border: 2px solid rgb(205, 176, 132);padding: 8px;background-color:rgb(205, 176, 132) ;color: white;
        margin-bottom: 18px;margin-top: -50px;}
    .btn-container {text-align: center;margin-top: 50px;}
    .btn-custom {border: 4px solid  rgb(63, 35, 18);font-size: 30px;padding: 20px 40px;margin: 10px;
        border-radius: 50px;transition: background-color 0.3, color 0.3s; background-color:rgb(241, 144, 8)  }
    .btn-custom:hover {border: 2px solid   rgb(63, 35, 18);background-color:rgb(63, 35, 18)}
    .description-box {background-color:  rgb(63, 35, 18);color:rgb(229, 180, 101);padding: 10px;margin: 20px auto;border-radius: 10px;
            max-width: 700px;text-align: center;font-size: 1.2rem;margin-top: 100px; height: auto; }
    .image-container { display: flex; justify-content: space-between; align-items: center; margin-top: -150px; }
    .image-container img { max-width: 25%;height: auto;margin-top: -150px;}

h1, h2 {margin-top: 50px;}
table {margin-top: 20px;}.form-container {margin-top: 30px;}.navbar-brand {font-weight: bold;}.navbar {background-color: rgb(63, 35, 18);} .offcanvas-header, .offcanvas-body {background-color: rgb(63, 35, 18);}
.navbar-brand, .nav-link, .offcanvas-title {color: #020b17;}
.small-image { width: 60%; 
    height: 50%;}
.card-container {display: flex;
        flex-wrap: wrap; /* Allow cards to wrap to the next line */
        justify-content: space-between; /* Distribute space between cards */}
.card {width: 18rem;
        margin-bottom: 20px; /* Adjust spacing between rows */
        margin-right: 20px; /* Adjust spacing between columns */}
.card-body {
        text-align: center; /* Center align content */}
</style>


<script>
export default{
   name:'CustBar',
   props: ['email'],
   mounted() {
    console.log('CustBar received email:', this.email);
  }
}
</script>
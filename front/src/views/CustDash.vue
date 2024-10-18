<template>
<body>
    <div class="container">
        <header>
        <MenuBar/>
        <h2>Welcome Customer</h2>
      </header>

        <h1>Cleaning Services</h1>


        <div class="rating">
            <span class="star">★</span> 4.9 (3.4M bookings near you)
        </div>

        <div class="services">
            <!-- Full House Cleaning -->
            <div class="service-card">
                <img src="https://img.icons8.com/fluency/60/000000/home.png" alt="Full House Cleaning">
                <h3>Full House Cleaning</h3>
            </div>

            <!-- Kitchen Cleaning -->
            <div class="service-card">
                <div class="badge">Trending Now</div>
                <img src="https://img.icons8.com/fluency/60/000000/kitchen.png" alt="Kitchen Cleaning">
                <h3>Kitchen Cleaning</h3>
            </div>

            <!-- Sofa Cleaning -->
            <div class="service-card">
                <img src="https://img.icons8.com/fluency/60/000000/sofa.png" alt="Sofa Cleaning">
                <h3>Sofa Cleaning</h3>
            </div>

            <!-- Bathroom Cleaning -->
            <div class="service-card">
                <div class="badge">Trending Now</div>
                <img src="https://img.icons8.com/fluency/60/000000/bathroom.png" alt="Bathroom Cleaning">
                <h3>Bathroom Cleaning</h3>
            </div>
        </div>
    </div>
</body>
</template>

<script>
import MenuBar from '../components/MenuBar.vue';
  export default {
    name:'CustDash',
    components:{MenuBar}
  };
  </script>
  
  <style>
  body {
      font-family: Arial, sans-serif;
      background-color: #f0f4f8;
      margin: 0;
      padding: 20px;
      text-align: center;
  }
  .container {
      max-width: 1200px;
      margin: 0 auto;
  }
  h1 {
      font-size: 36px;
      margin-bottom: 10px;
  }
  .rating {
      font-size: 18px;
      color: #666;
  }
  .rating .star {
      color: #f4c150;
  }
  .services {
      display: flex;
      justify-content: space-around;
      margin-top: 20px;
  }
  .service-card {
      background-color: #fff;
      border-radius: 10px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      width: 200px;
      padding: 20px;
      text-align: center;
      position: relative;
  }
  .service-card img {
      width: 60px;
      height: 60px;
      margin-bottom: 10px;
  }
  .service-card h3 {
      font-size: 18px;
      margin: 10px 0;
  }
  .badge {
      background-color: #f39c12;
      color: white;
      font-size: 12px;
      padding: 5px 10px;
      border-radius: 20px;
      position: absolute;
      top: -10px;
      right: -10px;
  }
</style>
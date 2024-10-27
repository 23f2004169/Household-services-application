<!-- <template>
    <body class="body mt-2">
      <div class="container mt-2">
        <h1 class="text-center border border-light p-3 custom-header text-white mb-4">
          HOUSEHOLD SERVICES APPLICATION
        </h1>
        <div class="text-center mt-5">
          <a href="/login">
            <button class="btn btn-secondary btn-custom">LOGIN</button>
          </a>
          <a href="/register_cust">
            <button class="btn btn-secondary btn-custom">REGISTER</button>
          </a>
        </div>
        <div class="description-box mt-4">
          <h4>Your all-in-one platform connecting homeowners with skilled service professionals, where an admin manages a seamless experience for all.</h4>
          <h4>Whether you need repairs, cleaning, or maintenance, we've got every corner of your home covered!</h4>
        </div>
      </div>
    </body>
  </template>
  
  <style>
    body {
    padding-top: 0px;
    background-color: rgb(205, 176, 132) !important;
    }
    .custom-header {
      background-color: #3b0a03; /* Header background color */
    }
    .btn-custom {
      border: 4px solid #3b0a03; /* Button border color */
      font-size: 30px; /* Button font size */
      padding: 20px 40px; /* Button padding */
      margin: 10px; /* Button margin */
      border-radius: 50px; /* Button border radius */
      transition: background-color 0.3s, color 0.3s; /* Transition for hover effects */
      background-color: rgb(241, 144, 8); /* Button background color */
    }
    .btn-custom:hover {
      border: 2px solid #3b0a03; /* Button hover border */
      background-color: rgb(255, 97, 5); /* Button hover background */
      outline: white; /* Button hover outline */
      color: white; /* Button hover text color */
    }
    .description-box {
      background-color: #3b0a03; /* Description box background */
      color: white; /* Description box text color */
      padding: 10px; /* Description box padding */
      margin: 20px auto; /* Description box margin */
      border-radius: 10px; /* Description box border radius */
      max-width: 700px; /* Max width for the description box */
      text-align: center; /* Center text in the description box */
      font-size: 1.2rem; /* Font size for the description text */
      margin-top: 100px; /* Top margin for the description box */
      height: auto; /* Auto height for the description box */
    }
  </style>  -->
  
  <template>
    <body class="body mt-2">
      <div class="container">

      <!-- Header Section -->
      <header class="header">
        <h1 class="app-title">HOMEWHIZ HOUSEHOLD SERVICES APPLICATION</h1>
      </header>
  
      <!-- Logo and Buttons -->
      <div class="logo-section">
        <img src="/static/logo.jpeg" alt="Homewhiz Logo" class="logo" />
        <p class="info-text">30+ K Happy Users & Verified Experts in 20+ Categories</p>
        <h4 class="info-text">Our services include:</h4>

        
      
      </div>
      <!-- Information -->
      <div class="info-section">
        <div class="buttons">
          <a href="/login">
            <button class="btn btn-primary">LOGIN</button>
          </a>
          <p> New here?</p>
      
          <a href="/register_cust">
            <button class="btn btn-primary">REGISTER</button>
          </a>
          <!-- <div >
          <p>Whether you need repairs, cleaning, or maintenance, we've got every corner of your home covered!</p>

          <p>Your all-in-one platform connecting homeowners with skilled service professionals, where an admin manages a seamless experience for all.</p>
          <p>Whether you need repairs, cleaning, or maintenance, we've got every corner of your home covered!</p>
         </div>  -->
      </div>
      </div>

  
      <!-- Services Section -->
      <div class="services">
        <div class="service">
          <img src="/static/childcare.jpeg" alt="Childcare Services" />
          <p>Childcare services</p>
        </div>
        <div class="service">
          <img src="/static/mealprep.jpeg" alt="Mealprep Services" />
          <p>Mealprep service</p>
        </div>
        <div class="service">
          <img src="/static/handyman.jpeg" alt="Handyman Services" />
          <p>Handyman</p>
        </div>
        <div class="service">
          <img src="/static/iron.jpeg" alt="Plumbing Services" />
          <p>Plumbing</p>
        </div>
        <div class="service">
          <img src="/static/iron.jpeg" alt="Specialized Services" />
          <p>Specialized</p>
        </div>
        <div class="service">
          <img src="/static/homeorg.jpeg" alt="Home Organization Services" />
          <p>Home org</p>
        </div>
      </div>  
    
    
  </div>


    </body>
  </template>

<style scoped>

body {
    padding-top: 20px;
    background-color: rgb(205, 176, 132) !important;
    margin: 0;
  font-family: Arial, sans-serif;
}
.container {display: flex;
        flex-wrap: wrap; 
        justify-content: space-between;}

/* Header Section */
.header {
  flex-wrap: wrap;
  background-color: #3d1818;
  padding: 20px;
  text-align: center;
}

.app-title {
  color: #fff;
  font-size: 36px;
  margin: 0;
}

/* Logo Section */
.logo-section {
  flex-wrap: wrap;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 20px 0;
}

.logo {
  width: 300px;
  height: auto;
  margin-bottom: 20px;
}

.buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 50px;
}

.btn-primary {
  background-color: #3d1818;
  border: none;
  color: white;
  padding: 38px 40px;
  text-align: center;
  font-size: 30px;
  cursor: pointer;
  border-radius: 25px;
  width: 250px;
}

.btn-primary:hover {
  background-color: #e67e00;
}

/* Information Section */
.info-section {
  text-align: center;
  margin: 20px 0;
}

.info-text {
  font-size: 18px;
  color: black;
}

/* Services Section */
.services {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.service {
  text-align: center;
  margin: 10px;
}

.service img {
  width: 150px;
  height: auto;
}

.service p {
  font-size: 14px;
  color: black;
}
.description-box {
      background-color: #3b0a03; /* Description box background */
      color: white; /* Description box text color */
      padding: 10px; /* Description box padding */
      margin: 20px auto; /* Description box margin */
      border-radius: 10px; /* Description box border radius */
      max-width: 700px; /* Max width for the description box */
      text-align: center; /* Center text in the description box */
      font-size: 1.2rem; /* Font size for the description text */
      margin-top: 100px; /* Top margin for the description box */
      height: auto; /* Auto height for the description box */
    }
</style>


<script>
  export default {
    name: 'HomeView',
  }
</script>
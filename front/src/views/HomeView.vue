<script>
  export default {
    name: 'HomeView',
  }
</script>

<template>
    <div class="container">

      <header class="header">
        <h1 class="app-title text-white"><b>WELCOME TO HOMEWHIZ HOUSEHOLD SERVICES APPLICATION</b></h1>
      </header>

      <div class="horizontal-section">
        <div class="logo-section">
          <img src="/static/logo.jpeg" alt="Homewhiz Logo" class="logo" />      
        </div>

        <div class="info-section">
          <div class="buttons">
            <a href="/login">
              <button class="btn btn-primary text-white"><b>LOGIN</b></button>
            </a>
            <a href="/register_cust">
              <button class="btn btn-primary text-white"><b>REGISTER</b></button>
            </a>
          </div>
        </div>
      </div>

      <div class="services">
        <div class="service">
          <img src="/static/childcare.jpeg" alt="Childcare Services" />
          <p style="color:#fff">Childcare services</p>
        </div>
        <div class="service">
          <img src="/static/Meal prep service.jpeg" alt="Mealprep Services" />
          <p style="color:#fff">Mealprep service</p>
        </div>
        <div class="service">
          <img src="/static/handyman.jpeg" alt="Handyman Services" />
          <p style="color:#fff">Handyman</p>
        </div>
        <div class="service">
          <img src="/static/Car Washing.jpeg" alt="Plumbing Services" />
          <p style="color:#fff">Carwash</p>
        </div>
        <div class="service">
          <img src="/static/specialized.jpeg" alt="Specialized Services" />
          <p style="color:#fff">Specialized</p>
        </div>
        <div class="service">
          <img src="/static/Cleaning and Organizing Service.jpeg" alt="Home Organization Services" />
          <p style="color:#fff">Home org</p>
        </div>
      </div>  

    </div>
</template>

<style scoped>
.homebody {
  padding-top: 100px;
  background-color:rgb(63, 35, 18)!important;
  margin: 0;
  font-family: Arial, sans-serif;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  background-color:#282828;
}

.header {
  flex-wrap: wrap;
  background-color:rgb(63, 35, 18);
  padding: 15px;
  text-align: center;
}

.app-title {
  /* color: #fff; */
  font-size: 36px;
  margin: 0;
}

.horizontal-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 20px 0;
  width: 100%;
}

.logo-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 20px;
}

.logo {
  width: 400px;
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
  background-color:rgb(63, 35, 18);
  border: none;
  color: BLACK;
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

.info-section {
  text-align: center;
  margin: 20px;
}

.info-text {
  font-size: 20px;
  color: black;
  font-family: 'Georgia', serif; 
}

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
  width: 180px;
  height: 150px;
}

.service p {
  font-size: 14px;
  color: black;
}

.description-box {
  background-color:#282828;
  color: white;
  padding: 10px;
  margin: 20px auto;
  border-radius: 10px;
  max-width: 700px;
  text-align: center;
  font-size: 1.2rem;
  margin-top: 100px;
  height: auto;
}
</style>
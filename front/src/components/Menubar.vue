<template>
    <nav class="navbar bg-body-tertiary fixed-top" style="background-color: rgb(63, 35, 18);">
        <div class="container-fluid" style="background-color:rgb(63, 35, 18);">
            <a class="navbar-brand " style="color:white">ADMIN DASHBOARD</a>
            <a href="/admin_dashboard"><button style="background-color:  rgb(63, 35, 18)">Home</button></a>
            <a href="/admin_search"><button style="background-color:  rgb(63, 35, 18);">Search</button></a>
            <a href="/admin_summary"><button style="background-color:  rgb(63, 35, 18);">Summary</button></a>
            <button @click="logout" style="background-color:  rgb(63, 35, 18);">Logout</button>

            <button style="background-color:white" class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon" style="color:white"></span>
            </button>
            <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasNavbar" aria-labelledby="offcanvasNavbarlabel">
                <div class="offcanvas-header">
                    <h5 class="offcanvas-title" id="offcanvasNavbarLabel" style="color:white">ALL DETAILS </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close" style="color:white"></button>
                </div>
                <div class="offcanvas-body">
                    <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
                        <li class="nav-item">
                            <a class="nav-link active" aria-current="page" href="/admin_dashboard" style="color:white">Home</a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link active" aria-current="page" href="/extended_view" style="color:white">Extended VIEW</a>
                        </li>
                        
                            <button @click="logout" class="btn btn-danger">Logout</button>
                        
                    </ul>
                </div>
            </div>
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
   name:'MenuBar',
   methods: {
    logout() {
    try {
        const jwt = localStorage.getItem('jwt_token');       
        localStorage.removeItem('jwt_token');        
        localStorage.clear();
        sessionStorage.clear();
        this.$router.push('/login');
        console.log('Logged out successfully');
    } catch (error) {
        console.error('Error during logout:', error);
        this.$router.push('/login');}
      }
   }


}
</script>
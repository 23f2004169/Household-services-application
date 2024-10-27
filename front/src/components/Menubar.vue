<template>
    <nav class="navbar bg-body-tertiary fixed-top" style="background-color: #3b0a03;">
        <div class="container-fluid" style="background-color: #3b0a03;">
            <a class="navbar-brand " style="color:white">ADMIN DASHBOARD</a>
            <a href="/admin_dashboard"><button style="background-color:rgb(205, 176, 132);">Home</button></a>
            <a href="/admin_search"><button style="background-color: #3b0a03;">Search</button></a>
            <a href="/admin_summary"><button style="background-color: #3b0a03;">Summary</button></a>
            <a href="/"><button style="background-color: #3b0a03;">Logout</button></a>

            <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasNavbar" aria-labelledby="offcanvasNavbarlabel">
                <div class="offcanvas-header">
                    <h5 class="offcanvas-title" id="offcanvasNavbarLabel">ALL DETAILS </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                </div>
                <div class="offcanvas-body">
                    <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
                        <li class="nav-item">
                            <a class="nav-link active" aria-current="page" href="/admin_dashboard">Home</a>
                        </li>
                        <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">VIEW ALL</a>
                            <ul class="dropdown-menu">
                                <li><a class="dropdown-item" href="/campaigns">Campaigns</a></li>
                                <li><a class="dropdown-item" href="/sponsors">Sponsors</a></li>
                                <li><a class="dropdown-item" href="/influencers">Influencers</a></li>
                                <li><a class="dropdown-item" href="/adrequests">Ad requests</a></li>
                            </ul>
                        </li>
                        
                        <li class="nav-item">
                            <a href="/
                            login"><button class="btn btn-danger">Logout</button></a>
                        </li>
                        
                    </ul>
                </div>
            </div>
        </div>
    </nav>
</template>

<style scoped>
 body {padding-top: 70px;background-color: #3b0a03 !important; }
    .header {text-align: center;border: 2px solid rgb(205, 176, 132);padding: 8px;background-color:rgb(205, 176, 132) ;color: white;
        margin-bottom: 18px;margin-top: -50px;}
    .btn-container {text-align: center;margin-top: 50px;}
    .btn-custom {border: 4px solid  #3b0a03;font-size: 30px;padding: 20px 40px;margin: 10px;
        border-radius: 50px;transition: background-color 0.3, color 0.3s; background-color:rgb(241, 144, 8)  }
    .btn-custom:hover {border: 2px solid  #3b0a03;background-color:rgb(255, 97, 5)}
    .description-box {background-color: #3b0a03;color:rgb(229, 180, 101);padding: 10px;margin: 20px auto;border-radius: 10px;
            max-width: 700px;text-align: center;font-size: 1.2rem;margin-top: 100px; height: auto; }
    .image-container { display: flex; justify-content: space-between; align-items: center; margin-top: -150px; }
    .image-container img { max-width: 25%;height: auto;margin-top: -150px;}

h1, h2 {margin-top: 50px;}
table {margin-top: 20px;}.form-container {margin-top: 30px;}.navbar-brand {font-weight: bold;}.navbar {background-color:#3b0a03;} .offcanvas-header, .offcanvas-body {background-color:#3b0a03;}
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
   name:'MenuBar'

}
</script>
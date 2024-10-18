<template>  
 <body>
    <div class="btn-container">

    <h1 class="header"> HOUSEHOLD SERVICES APPLICATION</h1>
    <div class="btn-container">
        <a href="/login"><button class="btn btn-secondary btn-custom">LOGIN </button></a>
        <a href="/register_cust"><button class="btn btn-secondary btn-custom" >REGISTER </button></a>
        
    </div>
    <div class="description-box">
        <h4>Your all-in-one platform connecting homeowners with skilled service professionals, where an admin manages a seamless experience for all. </h4>
            <h4>Whether you need repairs, cleaning, or maintenance, we've got every corner of your home covered!        </h4>
    </div>
    </div>
</body>
</template>

 <style>
    body {padding-top: 70px;background-color: rgb(205, 176, 132);}
    .header {text-align: center;border: 2px solid rgb(205, 176, 132);padding: 8px;background-color: #3b0a03;color: white;
        margin-bottom: 18px;margin-top: -50px;}
    .btn-container {text-align: center;margin-top: 50px;}
    .btn-custom {border: 4px solid  #3b0a03;font-size: 30px;padding: 20px 40px;margin: 10px;
        border-radius: 50px;transition: background-color 0.3, color 0.3s; background-color:rgb(241, 144, 8)  }
    .btn-custom:hover {border: 2px solid  #3b0a03;background-color:rgb(255, 97, 5);outline:white;color: white;}
    .description-box {background-color: #3b0a03;color:white;padding: 10px;margin: 20px auto;border-radius: 10px;
            max-width: 700px;text-align: center;font-size: 1.2rem;margin-top: 100px; height: auto; }
    .image-container { display: flex; justify-content: space-between; align-items: center; margin-top: -150px; }
    .image-container img { max-width: 25%;height: auto;margin-top: -150px;}

</style> 


<script>

export default {
    name: 'HomeView',
}
</script>


<template>
    <header class="header d-flex justify-content-between align-items-center px-4 py-3">
      <h1 class="text-primary">Welcome to Professional</h1>
      <nav class="nav-links">
        <a href="#" class="nav-link">Home</a>
        <a href="#" class="nav-link">Search</a>
        <a href="#" class="nav-link">Summary</a>
        <a href="#" class="nav-link">Logout</a>
      </nav>
    </header>
  </template>
  
  <style>
  .header {
    background-color: #f0f9ff;
    border-bottom: 2px solid #ddd;
  }
  .nav-link {
    margin-right: 15px;
    color: #555;
    font-weight: bold;
    text-decoration: none;
  }
  .nav-link:hover {
    color: #007bff;
    text-decoration: underline;
  }
  </style>
<script>
  export default {
    name:'ProfServices',
  };
  </script>
<script setup>
const products = [
  {
    id: 1,
    name: 'T-Shirt',
    description: 'Comfortable cotton T-shirt',
    price: 19.99,
    image: 'https://via.placeholder.com/150'
  },
  {
    id: 2,
    name: 'Jeans',
    description: 'Classic blue jeans',
    price: 39.99,
    image: 'https://via.placeholder.com/150'
  }
  // Add more products here
]

async function helloWorld()
{
  const response = await fetch("http://127.0.0.1:5000");
  const hello = await response.json();
  console.log(hello);
}
helloWorld();
function addToCart(product) {
  // Add logic to add product to cart
  console.log("Product added to cart:", product);
}
</script>


<template>
  <div class="home">
    <h1>Welcome to Our Clothes Shopping Website</h1>
    <p>Check out our latest collection!</p>
    <div class="products">
      <!-- Example product cards -->
      <div v-for="product in products" :key="product.id" class="product-card">
        <img :src="product.image" :alt="product.name">
        <div class="product-details">
          <h2>{{ product.name }}</h2>
          <p>{{ product.description }}</p>
          <p>Price: ${{ product.price }}</p>
          <button @click="addToCart(product)">Add to Cart</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home {
  text-align: center;
}

.products {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.product-card {
  margin: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 300px;
}

.product-card img {
  width: 100%;
  border-radius: 5px;
}

.product-details {
  margin-top: 10px;
}
</style>
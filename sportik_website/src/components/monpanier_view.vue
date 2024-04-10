<template>
  <div class="my-cart">
    <h2>My Cart</h2>
    <div v-if="cartItems.length === 0">
      <p>Your cart is empty.</p>
    </div>
    <div v-else>
      <ul>
        <li v-for="(item, index) in cartItems" :key="index">
          <img :src="item.image" alt="Product Image" style="width: 50px; height: 50px; margin-right: 10px;">
          <div>
            <span>{{ item.name }}</span><br>
            <span>Price: ${{ item.price }}</span><br>
            <span>Quantity: {{ item.quantity }}</span>
          </div>
          <button @click="removeFromCart(index)">Remove</button>
        </li>
      </ul>
      <button @click="pay" v-if="cartItems.length > 0">Pay</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      cartItems: [ // Initialize cart items array with fake data
        { name: 'Adidas Shoes', price: 99.99, image: 'https://via.placeholder.com/150', quantity: 1 },
        { name: 'Adidas T-shirt', price: 29.99, image: 'https://via.placeholder.com/150', quantity: 2 },
        { name: 'Adidas Cap', price: 19.99, image: 'https://via.placeholder.com/150', quantity: 1 }
      ]
    };
  },
  methods: {
    removeFromCart(index) {
      this.cartItems.splice(index, 1); // Remove item from cart
    },
    pay() {
      // Logic for payment (e.g., redirect to payment page)
      alert('Redirecting to payment page...');
    }
  }
};
</script>

<style>
.my-cart {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 5px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

button {
  margin-left: auto;
  padding: 5px 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>

<template>
  <div class="product-container">
    <!-- Product Image -->
    <img :src="product.imageUrl" :alt="product.title" class="product-image">

    <!-- Product Title -->
    <h2 class="product-title">{{ product.title }}</h2>

    <!-- Product Description -->
    <p class="product-description">{{ product.description }}</p>

    <!-- Product Price -->
    <p class="product-price">{{ product.price }}</p>

    <!-- Add to Cart Button -->
    <button class="add-to-cart-btn" @click="addToCart">Add to Cart</button>
  </div>
</template>

<script>
export default {
  props: {
    product: {
      type: Object,
      required: true
    }
  },
  methods: {
    addToCart() {
      // You can emit an event to notify the parent component that the item is added to the cart
      this.$emit('add-to-cart', this.product);
    }
  }
};
</script>

<style scoped>
/* Style for the product container */
.product-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

/* Style for the product image */
.product-image {
  width: 100%;
  max-height: 400px;
  object-fit: cover;
  margin-bottom: 20px;
}

/* Style for the product title */
.product-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
}

/* Style for the product description */
.product-description {
  margin-bottom: 20px;
}

/* Style for the product price */
.product-price {
  font-size: 20px;
  font-weight: bold;
  color: green;
  margin-bottom: 20px;
}

/* Style for the add to cart button */
.add-to-cart-btn {
  padding: 10px 20px;
  background-color: blue;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}
</style>

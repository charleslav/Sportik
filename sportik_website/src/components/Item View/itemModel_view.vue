<template>
  <div v-if="item" class="item-view">
    <div class="item-left">
      <img :alt="item.name" :src="selectedColorImage">

    </div>
    <div class="item-right">
      <h2>{{ item.product_name }}</h2>
      <p>{{ item.description }}</p>
      <p class="price">Price: ${{ item.price }}</p>
      <!-- Color variations -->
      <div class="variation-options">
        <label for="color">Color:</label>
        <div class="color-buttons">
          <button v-for="color in item.colors" :key="color.id" :style="{ backgroundColor: color.name }"
                  @click="selectedColor = color.id"></button>
        </div>
      </div>
      <!-- Size variations -->
      <div class="variation-options">
        <label for="size">Size:</label>
        <div class="size-buttons">
          <button v-for="size in item.sizes" :key="size" @click="selectedSize = size">{{ size }}</button>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    Loading..
  </div>

  <!-- Reviews
  <div class="reviews-container">
    <div class="reviews">
      <h3>Reviews</h3>
      <ul v-if="item.reviews.length > 0">
        <li v-for="(review, index) in item.reviews" :key="index" class="review-item">
          <p>{{ review.text }}</p>
          <p>Rating: {{ review.rating }}/5</p>
          <p>By: {{ review.user }}</p>
        </li>
      </ul>
      <p v-else>No reviews yet.</p>
    </div>

    <div class="leave-review">
      <h3>Leave a Review</h3>
      <form @submit.prevent="submitReview">
        <label for="review-text">Your Review:</label>
        <textarea id="review-text" v-model="newReview.text" rows="4" required></textarea>

        <label for="review-rating">Rating:</label>
        <select id="review-rating" v-model="newReview.rating" required>
          <option value="5">5 - Excellent</option>
          <option value="4">4 - Good</option>
          <option value="3">3 - Average</option>
          <option value="2">2 - Poor</option>
          <option value="1">1 - Very Poor</option>
        </select>



        <button type="submit">Submit Review</button>
      </form>
    </div>
  </div>-->
</template>

<script setup>
import { computed, ref } from 'vue'


const props = defineProps(["itemId"])
const item = ref({})
fetch(`http://127.0.0.1:5000/product/${props.itemId}`, {
  method:"get",
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }

}).then( (response) => {
  return response.json()
}).then( (data) => {
  if (data.status === 200){
    item.value = data.productData;
    console.log(data.productData)
  }
}).catch((error) => {
  console.log(error)
})



/*const item = ref({
  name: 'Example Item',
  description: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
  price: 19.99,
  image: 'https://via.placeholder.com/150', // Replace with actual image URL
  colors: [
    { id: 1, name: 'Red', image: 'https://via.placeholder.com/150?text=Red' },
    { id: 2, name: 'Blue', image: 'https://via.placeholder.com/150?text=Blue' },
    { id: 3, name: 'Green', image: 'https://via.placeholder.com/150?text=Green' }

  ],
  sizes: ['Small', 'Medium', 'Large'], // Example sizes
  reviews: [
    { text: 'Great item!', rating: 5, user: 'John Doe' },
    { text: 'Could be better', rating: 3, user: 'Jane Smith' }
  ]
})*/
const selectedColor = ref(null)
const selectedSize = ref(null)

const selectedColorImage = computed(() => {
  if (selectedColor.value) {
    const selectedColorObj = item.value.colors.find(color => color.id === selectedColor.value)
    return selectedColorObj ? selectedColorObj.image : item.value.image
  }
  return item.value.image
})

/*const newReview = ref({
  text: '',
  rating: 5,
  user: ''
})
*/
/*const submitReview = () => {

  if (newReview.value.text) {
    item.value.reviews.push({
      text: newReview.value.text,
      rating: newReview.value.rating,
      user: newReview.value.user
    })

    newReview.value.text = ''
    newReview.value.rating = 5
    newReview.value.user = ''
  } else {

    alert('Please fill out all fields.')
  }
}*/
</script>

<style scoped>
.reviews-container {
  text-align: center;
  margin-top: 20px;
  max-width: 600px; /* Set the maximum width for the review section */
  margin: 0 auto; /* Center the review section horizontally */
  margin-bottom: 20px; /* Add space at the end */
}

.item-view {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 20px;
  margin-bottom: 20px;
}

.item-left {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.item-right {
  flex: 1;
  float: right;
  margin-left: 20px;
}

.price {
  font-weight: bold;
}

.variation-options {
  margin-top: 10px;
}

.color-buttons button {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 5px;
  border: none;
  cursor: pointer;
}

.size-buttons button {
  padding: 5px 10px;
  margin-right: 5px;
  border: none;
  cursor: pointer;
}

.reviews {
  margin-top: 20px;
}

.review-item {
  border-bottom: 1px solid #ccc;
  padding-bottom: 10px;
  margin-bottom: 10px;
}

.review-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
  margin-bottom: 0;
}

.leave-review {
  margin-top: 20px;
}

.leave-review form {
  text-align: left;
}

.leave-review label {
  display: block;
  margin-bottom: 5px;
}

.leave-review textarea,
.leave-review select,
.leave-review input {
  width: 100%;
  padding: 5px;
  margin-bottom: 10px;
}

.leave-review button {
  padding: 8px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.leave-review button:hover {
  background-color: #0056b3;
}
</style>

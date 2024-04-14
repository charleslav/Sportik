<template>
  <div class="contact">
    <h2>Contact Us</h2>
    <p>If you have any questions or inquiries, feel free to contact us using the form below:</p>
    <form @submit.prevent="submitForm" v-if="!submitted">
      <div class="form-group">
        <label for="name">Your Name:</label>
        <input type="text" id="name" v-model="name" required>
      </div>
      <div class="form-group">
        <label for="email">Your Email:</label>
        <input type="email" id="email" v-model="email" required>
      </div>
      <div class="form-group">
        <label for="message">Your Message:</label>
        <textarea id="message" v-model="message" required></textarea>
      </div>
      <button type="submit">Submit</button>
    </form>
    <p v-else>Contact form submitted successfully! We'll get back to you shortly.</p>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const name = ref('');
const email = ref('');
const message = ref('');
const submitted = ref(false);

const submitForm = () => {
  // Here you can implement the logic to send the form data
  console.log('Form submitted:', { name: name.value, email: email.value, message: message.value });
  // Reset form fields after submission
  name.value = '';
  email.value = '';
  message.value = '';
  // Set submitted to true to display confirmation message
  submitted.value = true;
};
</script>

<style scoped>
.contact {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
}

p {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="email"],
textarea {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

textarea {
  height: 150px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background-color: #0056b3;
}
</style>

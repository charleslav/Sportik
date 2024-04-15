<script setup>

import Cookies from 'js-cookie'
import router from '@/router'

Cookies.remove("user_token")
alert("You are now logout")

router.push("/")
</script>

<template>
  <div>
  </div>
</template>


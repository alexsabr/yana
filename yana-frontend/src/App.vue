<template>
  <theheader></theheader>
  <router-view></router-view>
</template>

<script>
import theheader from './components/theHeader.vue'
export default {
  components: { theheader },
  data () { return {} }
}
</script>

<style scoped>

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>

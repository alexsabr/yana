<template>

  <h1>
    <button @click="triggerRefresh">
      CLICK TO TRIGGER REFRESH
    </button>
    <p id="info_text" v-if="scrap_status_message.length > 0">{{ scrap_status_message }}</p>
  </h1>

</template>

<script>
export default {
  data () {
    return {
      scrap_status_message: '',
      scrap_status_color: ''
    }
  },
  methods: {
    triggerRefresh () {
      const triggerPromise = fetch('localhost:8081/scrap')
      triggerPromise.then((response) => {
        if (response.status === 200) {
          this.scrapSuccessMessage()
        } else { this.scrapFailureMessage() }
      }).catch((e) => { this.scrapFailureMessage() })
    },
    scrapSuccessMessage () {
      this.scrap_status_message = 'Scrapping Successfully requested !'
      this.scrap_status_color = 'green'
    },
    scrapFailureMessage () {
      this.scrap_status_message = '/!\\ Failed to request scrapping /!\\ '
      this.scrap_status_color = 'red'
    }

  }

}
</script>

<style scoped>
.button {
  background-color: rgb(148, 29, 29);
  size: 2in 2in;
}

#info_text {
  color: v-bind(scrap_status_color);
}
</style>

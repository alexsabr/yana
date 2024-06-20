<template>

  <ul v-if="articles_to_display.length > 0" id="article_list">
    <li v-for="learticle in articles_to_display" v-bind:key=learticle.title>
    <h4> {{learticle["title"]}}</h4>
    <h5>{{learticle["journal"]["name"]}}</h5>
    <p>{{learticle["condensed_text"]}}</p>
    <ul>
    <li v-for="similararticle in learticle.linked_article" v-bind:key=similararticle.title>
      <br>
      <h4>{{similararticle["title"]}}</h4>
    <h5>{{similararticle["journal"]["name"]}}</h5>
    </li>
  </ul>
    </li>
  </ul>
  <p v-else>Here shortly the articles !</p>

  <button @click="fetchArticle()">Show some media !</button>
</template>

<script>

export default {
  data () {
    return {
      articles_to_display: []
    }
  },
  components: {
  },
  methods: {
    fetchArticle () {
      const datathis = this
      console.info('fetch article clicked !')
      fetch('http://localhost:8081/article').then(async response => {
        if (response.ok !== true) { return };
        // console.log(response.json())
        const theobject = await response.json()
        datathis.articles_to_display.push(theobject)
        console.info('appended an article !')
      })
    }
  },
  addArticle (oneArticle) {

  }
}
</script>

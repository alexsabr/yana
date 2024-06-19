import { createStore } from 'vuex'

export default createStore({
  state: {
    numberOfArticles: 0
  },
  getters: {
    NumberOfArticles (state) { return state.numberOfArticles }
  },
  mutations: {
    setNumberOfArticles (state, newnumber) {
      state.numberOfArticles = newnumber
    }
  },
  actions: {
    updateNumberOfArticles (context) {
      const numberPromise = fetch('http://localhost:8081/number')
      let newnumber = -42
      numberPromise.then((response) => {
        if (response.status !== 200) { console.log('error when fetching article') }
        const jsonprom = response.json()
        jsonprom.then((data) => {
          newnumber = data.number_article_available
        })
      })
      context.store.commit('setNumberOfArticles', newnumber)
    }
  },
  modules: {
  }
})

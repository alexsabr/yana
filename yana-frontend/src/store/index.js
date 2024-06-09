import { createStore } from 'vuex'

export default createStore({
  state: {
    numberOfArticles:0
  },
  getters: {
    NumberOfArticles(state,**){return state.numberOfArticles;}
  },
  mutations: {
    setNumberOfArticles(state,newnumber){
      state.numberOfArticles = newnumber;
    }
  },
  actions: {
    updateNumberOfArticles(context,){
      //TODO query backend for number of articles and update through setNumberofArticles
      const newnumber = 42;
      $store.commit(setNumberOfArticles,newnumber);
    }
  },
  modules: {
  }
})

import { createStore } from 'vuex'

export default createStore({
  state: {
    token: null,
    patient: null,
    groups: [],
    tests: {},
  },

  getters: {
    getToken: state => state.token,
    getPatient: state => state.patient,
    getGroups: state => state.groups,
    getTests: state => state.tests,
  },

  mutations: {
    setToken(state, token) {
      state.token = token
    },
    setPatient(state, patient) {
      state.patient = patient
    },
    setGroups(state, groups) {
      state.groups = groups
    },
    addTests(state, test) {
      state.tests[test.name] = test.data
    }
  },

  actions: {
    setToken({ commit }, token) {
      commit('setToken', token)
    },
    setPatient({ commit }, patient) {
      commit('setPatient', patient)
    },
    setGroups({ commit }, groups) {
      commit('setGroups', groups)
    },
    addTests({ commit }, test) {
      commit('addTests', test)
    }
  },
})

import { createStore } from 'vuex'

export default createStore({
  state: {
    token: null,
    patient: null,
    groups: [],
    tests: {},
    complete: {},
  },

  getters: {
    getToken: state => state.token,
    getPatient: state => state.patient,
    getGroups: state => state.groups,
    getTests: state => state.tests,
    getTestByName: state => name => state.tests[name],
    getComplete: state => state.complete,
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
    setTests(state, tests) {
      state.tests = tests
    },
    addTests(state, test) {
      state.tests[test.name] = test.data
    },
    delTest(state, name) {
      delete state.tests[name]
    },
    setComplete(state, complete) {
      state.complete = complete
    },
    addComplete(state, complete) {
      state.complete[complete.name] = complete.data
    },
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
    setTests({ commit }, tests) {
      commit('setTests', tests)
    },
    addTests({ commit }, test) {
      commit('addTests', test)
    },
    delTest({ commit }, name) {
      commit('delTest', name)
    },
    setComplete({ commit }, complete) {
      commit('setComplete', complete)
    },
    addComplete({ commit }, complete) {
      commit('addComplete', complete)
    },
  },
})

import { defineStore } from 'pinia'
import type { MainState, TestData, CompleteData } from '@/types/store'
import type { Patient, SelectOption } from '@/types/api'

export const useMainStore = defineStore('main', {
  state: (): MainState => ({
    token: null,
    patient: null,
    groups: [],
    tests: {},
    complete: {},
  }),
  getters: {
    getToken: (state: MainState): string | null => state.token,
    getPatient: (state: MainState): Patient | null => state.patient,
    getGroups: (state: MainState): SelectOption[] => state.groups,
    getTests: (state: MainState): Record<string, any> => state.tests,
    getTestByName: (state: MainState) => (name: string): any => state.tests[name],
    getComplete: (state: MainState): Record<string, any> => state.complete,
  },
  actions: {
    setToken(token: string | null): void {
      this.token = token
    },
    setPatient(patient: Patient | null): void {
      this.patient = patient
    },
    setGroups(groups: SelectOption[]): void {
      this.groups = groups
    },
    setTests(tests: Record<string, any>): void {
      this.tests = tests
    },
    addTests(test: TestData): void {
      this.tests[test.name] = test.data
    },
    delTest(name: string): void {
      delete this.tests[name]
    },
    setComplete(complete: Record<string, any>): void {
      this.complete = complete
    },
    addComplete(complete: CompleteData): void {
      this.complete[complete.name] = complete.data
    },
    delComplete(name: string): void {
      delete this.complete[name]
    },
  },
})
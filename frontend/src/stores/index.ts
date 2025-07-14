import { defineStore } from 'pinia'
import type { MainState, TestData, CompleteData } from '@/types/store'
import type { Patient, SelectOption } from '@/types/api'

export const useMainStore = defineStore('main', {
  state: (): MainState => ({
    patient: null,
    groups: [],
    tests: {},
    complete: {},
  }),
  getters: {
    getTestByName: (state: MainState) => (name: string): any => state.tests[name],
    groupOptions: (state: MainState) => {
      return state.groups.map(group => ({
        text: group.label,
        value: group.value,
      }))
    },
    getGroupNameById: (state: MainState) => (id?: number): string => {
      return state.groups.find(group => group.value === id)?.label || '未确定'
    }
  },
  actions: {
    async initGroups() {
      if (this.groups.length > 0) return
      try {
        const { getGroups } = await import('@/api/kawasaki')
        this.groups = await getGroups()
      } catch (error) {
        console.error('Failed to fetch groups:', error)
      }
    },
    setPatient(patient: Patient | null): void {
      this.patient = patient
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
  }
})

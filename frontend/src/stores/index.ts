import { defineStore } from 'pinia'
import type { MainState, TestData, CompleteData } from '@/types/store'
import type { Patient } from '@/types/api'

export const useMainStore = defineStore('main', {
  state: (): MainState => ({
    patient: null,
    groups: [],
    tests: {},
    originalTests: {}, // 保存从API获取的原始数据，用于比较变更
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
      // 同时保存原始数据的深拷贝
      this.originalTests = JSON.parse(JSON.stringify(tests))
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
    // 优化的变更检测算法 - 更高效的对象比较和更好的错误处理
    getChangedTests(): Record<string, { added: any[], updated: any[], unchanged: any[] }> {
      const changes: Record<string, { added: any[], updated: any[], unchanged: any[] }> = {}
      
      // 辅助函数：深度比较对象（忽略指定字段）
      const deepEqual = (obj1: any, obj2: any, ignoreFields: string[] = ['version', 'modified_at']): boolean => {
        if (obj1 === obj2) return true
        if (!obj1 || !obj2) return false
        if (typeof obj1 !== 'object' || typeof obj2 !== 'object') return obj1 === obj2
        
        const keys1 = Object.keys(obj1).filter(key => !ignoreFields.includes(key))
        const keys2 = Object.keys(obj2).filter(key => !ignoreFields.includes(key))
        
        if (keys1.length !== keys2.length) return false
        
        return keys1.every(key => {
          if (!keys2.includes(key)) return false
          return deepEqual(obj1[key], obj2[key], ignoreFields)
        })
      }
      
      for (const [testName, currentData] of Object.entries(this.tests)) {
        const originalData = this.originalTests[testName] || []
        const current = Array.isArray(currentData) ? currentData : []
        const original = Array.isArray(originalData) ? originalData : []
        
        changes[testName] = {
          added: [],
          updated: [],
          unchanged: []
        }
        
        // 为了提高性能，创建原始数据的ID映射
        const originalMap = new Map(original.map(item => [item.id, item]))
        
        // 检查当前数据中的每一项
        for (const item of current) {
          if (!item.id) {
            // 没有ID的为新增记录
            changes[testName].added.push(item)
          } else {
            const originalItem = originalMap.get(item.id)
            if (originalItem) {
              // 使用优化的深度比较
              if (!deepEqual(item, originalItem)) {
                changes[testName].updated.push(item)
              } else {
                changes[testName].unchanged.push(item)
              }
            } else {
              // 原始数据中没有找到，按更新处理
              changes[testName].updated.push(item)
            }
          }
        }
      }
      
      return changes
    }
  }
})

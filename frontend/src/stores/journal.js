import { privateStorageKey } from '@/utils/orderAccess'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useJournalStore = defineStore('journal', () => {
  const savedJournal = localStorage.getItem(privateStorageKey('journal_entries'))
  let initialData = null
  try { initialData = savedJournal ? JSON.parse(savedJournal) : null } catch {}

  const entries = ref(initialData?.entries || [])
  const streak = ref(initialData?.streak || 0)
  function loadProfile() {
    let data = null
    try { data = JSON.parse(localStorage.getItem(privateStorageKey('journal_entries')) || 'null') } catch {}
    entries.value = data?.entries || []; streak.value = data?.streak || 0
  }

  function persist() {
    localStorage.setItem(privateStorageKey('journal_entries'), JSON.stringify({
      entries: entries.value,
      streak: streak.value
    }))
  }

  function addEntry(newEntry) {
    const d = new Date(newEntry.date || Date.now())
    const dayNum = d.getDate()
    const monthStr = d.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
    const dayOfWeek = d.toLocaleDateString('en-US', { weekday: 'short' })

    const entry = {
      id: Date.now(),
      date: newEntry.date || new Date().toISOString().split('T')[0],
      dayNum,
      monthStr,
      dayOfWeek,
      title: newEntry.title || 'Daily Log',
      notes: newEntry.notes || '',
      tags: newEntry.tags || [],
      productImages: newEntry.productImages || [],
      extraCount: newEntry.extraCount || 0
    }

    entries.value.unshift(entry)
    streak.value += 1
    persist()
  }

  function deleteEntry(id) {
    entries.value = entries.value.filter(e => e.id !== id)
    persist()
  }

  const loggedDays = computed(() => {
    return entries.value.map(e => e.dayNum)
  })

  return {
    loadProfile,
    entries,
    streak,
    loggedDays,
    addEntry,
    deleteEntry
  }
})

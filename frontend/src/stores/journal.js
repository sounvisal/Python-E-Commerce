import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useJournalStore = defineStore('journal', () => {
  const savedJournal = localStorage.getItem('lumea_journal_entries')
  const initialData = savedJournal ? JSON.parse(savedJournal) : null

  const entries = ref(initialData?.entries || [
    {
      id: 1,
      date: '2025-06-25',
      dayNum: 25,
      monthStr: 'Jun 2025',
      dayOfWeek: 'Wed',
      title: 'Good Skin Day!',
      notes: 'My skin feels smoother and less oily today. The new toner really helps. No breakouts, and my skin looks brighter.',
      tags: ['Less Oil', 'Brighter', 'No Breakouts'],
      productImages: [
        '/images/prod-anua-toner.jpg',
        '/images/prod-sk2.jpg',
        '/images/prod-laneige.jpg'
      ],
      extraCount: 2
    },
    {
      id: 2,
      date: '2025-06-22',
      dayNum: 22,
      monthStr: 'Jun 2025',
      dayOfWeek: 'Sun',
      title: 'A Little Dryness',
      notes: 'Woke up with some dry spots on my cheeks. Might be from the weather. Used a hydrating mask tonight.',
      tags: ['Dryness', 'Used Mask', 'Weather'],
      productImages: [
        '/images/prod-anua-toner.jpg',
        '/images/cat-masks.jpg',
        '/images/prod-laneige.jpg'
      ],
      extraCount: 1
    },
    {
      id: 3,
      date: '2025-06-19',
      dayNum: 19,
      monthStr: 'Jun 2025',
      dayOfWeek: 'Thu',
      title: 'Breakout Healing',
      notes: 'A small breakout on my chin, but it\'s already calming down. Using a spot treatment and keeping my routine simple.',
      tags: ['Breakout', 'Healing', 'Simpler Routine'],
      productImages: [
        '/images/prod-ordinary.jpg',
        '/images/prod-sk2.jpg',
        '/images/prod-cerave-cleanser.jpg'
      ],
      extraCount: 1
    },
    {
      id: 4,
      date: '2025-06-15',
      dayNum: 15,
      monthStr: 'Jun 2025',
      dayOfWeek: 'Sun',
      title: 'Feeling Fresh',
      notes: 'Skin feels hydrated and plump today! Love how it looks after using the new moisturizer.',
      tags: ['Hydrated', 'Plump', 'Glowing'],
      productImages: [
        '/images/prod-anua-toner.jpg',
        '/images/prod-cosrx-snail.jpg',
        '/images/prod-cerave-cleanser.jpg'
      ],
      extraCount: 2
    }
  ])

  const streak = ref(initialData?.streak || 7)

  function persist() {
    localStorage.setItem('lumea_journal_entries', JSON.stringify({
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
      tags: newEntry.tags || ['Hydrated'],
      productImages: newEntry.productImages?.length ? newEntry.productImages : ['/images/prod-anua-toner.jpg', '/images/prod-laneige.jpg'],
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
    entries,
    streak,
    loggedDays,
    addEntry,
    deleteEntry
  }
})

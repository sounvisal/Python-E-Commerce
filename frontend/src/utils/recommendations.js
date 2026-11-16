// Rule-based suggestions from live product metadata; no fixed product IDs.
export function buildRoutine(catalog, answers, evening = false) {
  const concernWords = [...(answers.concerns || []), ...(answers.goals || [])].join(' ').toLowerCase()
  const groups = [['cleansers'], ['moisturizers']]
  const level = answers.routineLevel || ''
  if (/complete|advanced/i.test(level)) groups.splice(1, 0, ['toners'])
  if (!/minimal|basic|1-2/i.test(level)) groups.splice(1, 0, ['serums', 'treatments', 'toners'])
  if (!evening) groups.push(['sunscreens'])
  const names = { cleansers: 'Cleanse', moisturizers: 'Moisturize', serums: 'Treat', treatments: 'Treat', toners: 'Tone', sunscreens: 'Protect' }
  const words = concernWords.split(/[^a-z]+/).filter(w => w.length > 3)
  function score(p) {
    const types = p.skin_type || []
    const metadata = [...(p.skin_concern || []), p.description || '', p.name].join(' ').toLowerCase()
    return (types.includes(answers.skinType) ? 20 : 0) + words.filter(w => metadata.includes(w)).length * 3
  }
  const used = new Set()
  return groups.flatMap(categories => {
    const options = catalog.filter(p => !used.has(p.id) && p.stock > 0 && categories.includes(p.category) &&
      (!(p.skin_type || []).length || p.skin_type.includes(answers.skinType) || p.skin_type.includes('All Skin Types')))
    options.sort((a, b) => score(b) - score(a) || a.id - b.id)
    const selected = options[0]
    if (selected) used.add(selected.id)
    return selected ? [{ ...selected, stepName: names[selected.category], tagline: `Selected for ${answers.skinType || 'your profile'} using available catalog attributes` }] : []
  }).map((p, index) => ({ ...p, step: index + 1 }))
}

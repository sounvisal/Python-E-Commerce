/**
 * Luméa Atelier CSV Exporter Utility
 * Converts tabular dataset into downloadable UTF-8 CSV spreadsheet.
 * Complies with OWASP CSV/Formula Injection prevention guidelines.
 */

const FORMULA_PREFIXES = ['=', '+', '-', '@', '\t', '\r']

export function exportToCSV(filename, rows, headers) {
  if (!rows || !rows.length) {
    return false
  }

  const keys = headers ? headers.map(h => h.key) : Object.keys(rows[0])
  const headerLabels = headers ? headers.map(h => h.label) : keys

  const csvContent = [
    headerLabels.map(escapeCSVField).join(','),
    ...rows.map(row => keys.map(k => escapeCSVField(row[k])).join(','))
  ].join('\r\n')

  const blob = new Blob(['\uFEFF' + csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.setAttribute('download', `${filename}_${new Date().toISOString().slice(0, 10)}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
  return true
}

function escapeCSVField(val) {
  if (val === null || val === undefined) return '""'
  let str = String(val)
  if (typeof val === 'object') {
    try { str = JSON.stringify(val) } catch { str = String(val) }
  }

  // OWASP CSV / Formula Injection Mitigation:
  // If user-controlled text starts with an executable spreadsheet operator (=, +, -, @, \t, \r),
  // prepend a single quote (') so spreadsheet engines (Excel, Calc) treat it as pure literal text.
  if (FORMULA_PREFIXES.some(prefix => str.startsWith(prefix))) {
    str = `'${str}`
  }

  str = str.replace(/"/g, '""')
  return `"${str}"`
}

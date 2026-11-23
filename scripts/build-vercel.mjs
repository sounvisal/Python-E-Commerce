import { execFileSync } from 'node:child_process'
import { cp, rm } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import { existsSync } from 'node:fs'

process.env.VITE_HOSTED_DEPLOYMENT = 'true'

function ensureDeps(app) {
  const viteBin = fileURLToPath(new URL(`../${app}/node_modules/vite/bin/vite.js`, import.meta.url))
  if (!existsSync(viteBin)) {
    console.log(`[Vercel Build] Installing dependencies for ${app}...`)
    const npmCmd = process.platform === 'win32' ? 'npm.cmd' : 'npm'
    execFileSync(npmCmd, ['--prefix', app, 'ci', '--include=dev'], {
      cwd: fileURLToPath(new URL('../', import.meta.url)),
      stdio: 'inherit',
    })
  }
}

function build(app, outDir, base) {
  ensureDeps(app)
  execFileSync(process.execPath, [
    'node_modules/vite/bin/vite.js', 'build', '--outDir', outDir, '--emptyOutDir', '--base', base,
  ], {
    cwd: fileURLToPath(new URL(`../${app}/`, import.meta.url)),
    stdio: 'inherit',
  })
}

build('frontend', '../dist', '/')
build('admin', '../dist/atelier', '/atelier/')

// Uploads belong to the API. Do not publish copies from a local build.
await rm(new URL('../dist/images/uploads/', import.meta.url), { recursive: true, force: true })
await rm(new URL('../dist/atelier/images/uploads/', import.meta.url), { recursive: true, force: true })

// The two apps share root-relative /images URLs. Keep the storefront copy on overlap.
await cp(new URL('../dist/atelier/images/', import.meta.url), new URL('../dist/images/', import.meta.url), {
  recursive: true,
  force: false,
})

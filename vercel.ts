const backendOrigin = (process.env.RENDER_API_ORIGIN ?? '').trim().replace(/\/$/, '')

if (!/^https:\/\/[a-zA-Z0-9_.-]+(?::\d+)?$/i.test(backendOrigin)) {
  throw new Error('Set RENDER_API_ORIGIN to the HTTPS origin of your backend (e.g. https://your-service.onrender.com).')
}

export const config = {
  framework: null,
  installCommand: 'npm --prefix frontend ci --include=dev && npm --prefix admin ci --include=dev',
  buildCommand: 'node scripts/build-vercel.mjs',
  outputDirectory: 'dist',
  routes: [
    {
      src: '^/api(?:/.*)?$',
      headers: {
        'Cache-Control': 'no-store',
        'Vercel-CDN-Cache-Control': 'no-store',
        'x-vercel-enable-rewrite-caching': '0',
      },
      continue: true,
    },
    { src: '^(/api(?:/.*)?)$', dest: `${backendOrigin}$1` },
    { src: '^(/images/uploads/.*)$', dest: `${backendOrigin}$1` },
    { handle: 'filesystem' },
    { src: '^(/videos/.*)$', dest: `${backendOrigin}$1` },
    { src: '^/atelier(?:/[^.]*)?$', dest: '/atelier/index.html', methods: ['GET', 'HEAD'] },
    { src: '^/(?!atelier(?:/|$)|assets(?:/|$)|images(?:/|$)|videos(?:/|$))[^.]*$', dest: '/index.html', methods: ['GET', 'HEAD'] },
  ],
}

import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';
import fs from 'fs';

export default defineConfig({
  plugins: [sveltekit()],
  test: {
    include: ['src/**/*.{test,spec}.{js,ts}']
  },
  build: {
    sourcemap: true,
    outDir: './dist'
  },
  server: {
    port: 3000,
    fs: {
      allow: ['/app/static']
    },
    https: {
      key: fs.readFileSync('/home/vagrant/server-ssl/server-web-key.pem'),
      cert: fs.readFileSync('/home/vagrant/server-ssl/server-web-cert.pem'),
      //requestCert: true, ca: [ fs.readFileSync('/home/vagrant/server-ssl/ca-web-cert.pem') ] 
    },
    proxy: {
      // Redirect all HTTP traffic to HTTPS
      'http://*': 'https://localhost:3000',
    }
  }
});

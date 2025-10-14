// @ts-check
import { defineConfig } from 'astro/config';

import react from '@astrojs/react';

import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  integrations: [react()],

  i18n: {
    locales: ["en", "es", "fr", "de"],
    defaultLocale: "en",
    
    routing: {
      prefixDefaultLocale: true, // Ensures that your default locale is prefixed aswell
    },
  },

  vite: {
    plugins: [tailwindcss()]
  }
});
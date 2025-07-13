/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
  "./pages/**/*.{js,ts,jsx,tsx,mdx}",
  "./components/**/*.{js,ts,jsx,tsx,mdx}",
  "./app/**/*.{js,ts,jsx,tsx,mdx}",
],
theme: {
  extend: {
    colors: {
      background: 'var(--background)',
      foreground: 'var(--foreground)',
      customDarkBlue: '#4A58B5',
      customlightBlue: '#C0EDF0',
      customOrange: '#FC6453',
      customYellow: '#fcae66',
      customLightYellow: '#FFF2DE',

    },
    borderRadius: {
      lg: 'var(--radius)',
      md: 'calc(var(--radius) - 2px)',
      sm: 'calc(var(--radius) - 4px)'
    }
  }
},
plugins: [
  require("tailwindcss-animate"),
  require('tailwind-scrollbar'),
],
};
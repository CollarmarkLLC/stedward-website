/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{njk,md,html,js}",
    "./src/_includes/**/*.{njk,html}",
    "./src/_layouts/**/*.{njk,html}"
  ],
  theme: {
    extend: {
      fontFamily: {
        serif: ['Playfair Display', 'Georgia', 'serif'],
      },
      colors: {
        'parish-blue': '#1e3a5f',
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};
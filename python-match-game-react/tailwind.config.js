/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // Add this line to scan all JS/JSX files in src
    "./public/index.html",       // Add this line to scan your public HTML file
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

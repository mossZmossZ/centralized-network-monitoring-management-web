/** @type {import('tailwindcss').Config} */
import daisyui from "daisyui";

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}", // Match everything in the src folder
    "./components/**/*.{js,ts,jsx,tsx}", // Match everything in the components folder
    "./pages/**/*.{js,ts,jsx,tsx}", // Match everything in the pages folder
  ],
  theme: {
    extend: {},
  },
  plugins: [daisyui],
  daisyui: {
    themes: ["light", "cupcake"],
  },
};
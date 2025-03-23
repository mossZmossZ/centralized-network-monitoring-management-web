/** @type {import('tailwindcss').Config} */
import daisyui from "daisyui";

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      animation: {
        typing: 'typing 3.5s steps(30) infinite', // Infinite loop for typing animation
        blink: 'blink 0.75s step-end infinite', // Cursor blink effect
      },
      keyframes: {
        typing: {
          '0%': { width: '0' }, // Start with an empty width
          '100%': { width: '100%' }, // Finish typing at full width
        },
        blink: {
          '0%': { borderColor: 'transparent' }, // Start with invisible cursor
          '100%': { borderColor: 'black' }, // Cursor visible
        },
      },
    },
  },
  plugins: [daisyui],
  daisyui: {
    themes: ["light", "cupcake"], // You can add more themes if you like
  },
};

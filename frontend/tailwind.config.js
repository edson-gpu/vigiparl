/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        navy: {
          DEFAULT: "#1A3C5E",
          50: "#E8EFF6",
          100: "#C5D5E7",
          500: "#1A3C5E",
          700: "#0F2238",
        },
        civic: {
          DEFAULT: "#C0392B",
          50: "#FAEAE8",
          100: "#F1C0BB",
          500: "#C0392B",
          700: "#8B2920",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

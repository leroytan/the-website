import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        blue: {
          100: '#E6F0FD',
          200: '#CCE3FC',
          500: '#3B82F6',
          600: '#2563EB',
          700: '#1D4ED8',
        },
        purple: {
          100: '#F3E8FF',
          600: '#9333EA',
          700: '#7E22CE',
        },
      },
    },
  },
  plugins: [],
};
export default config;

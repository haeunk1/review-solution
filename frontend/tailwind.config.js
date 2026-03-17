/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: 'hsl(var(--primary))', foreground: 'hsl(var(--primary-foreground))' },
        muted: { DEFAULT: 'hsl(var(--muted))', foreground: 'hsl(var(--muted-foreground))' },
        highlighted: 'hsl(var(--highlighted))',
        default: 'hsl(var(--default))',
        elevated: 'hsl(var(--elevated))',
      },
    },
  },
  plugins: [],
}

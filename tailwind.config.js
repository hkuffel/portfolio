module.exports = {
  purge: [],
  darkMode: 'class',
  theme: {
    fontFamily: {
      'mono': ['Hack']
    },
    textColor: {
      'primary': '#93A1A1',
      'secondary': '#002B36'
    },
    colors: {
      navy: '#002B36',
      white: 'white',
      pink: '#d33682',
      darkPink: '#b81f69',
      gray: '#586e75',
      orange: '#cb4b16'
    },
    fill: theme => theme('colors'),
    stroke: theme => theme('colors'),
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}

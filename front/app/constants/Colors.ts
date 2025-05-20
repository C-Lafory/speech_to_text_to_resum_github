// TODO : 
// Implémenter le reste des couleurs des thèmes.

const tintColorLight = '#0a7ea4';
const tintColorDark = '#fff';

export const Colors = {
  primary: '#ff0000',
  secondary: '#00ff00',
  light: {
    text: '#11181C',
    background: '#fff',
    tint: tintColorLight,
    icon: '#687076',
    tabIconDefault: '#687076',
    tabIconSelected: tintColorLight,
  },
  dark: {
    text: 'rgba(255, 255, 255, 0.9)',
    background: '#141414',
    tint: tintColorDark,
    icon: '#9BA1A6',
    tabIconDefault: '#262626',
    tabIconSelected: tintColorDark,
  },
};

export default Colors;
import { Colors } from '@/app/constants/Colors';
import { useColorScheme } from 'react-native';
import { useContext } from 'react';

// Récupère la couleur du thème actuel.
// Reprend tot ce qui est dans Colors et le met dans un tableau.

export function useThemeColor(
  props: { light?: string; dark?: string },
  colorName: keyof typeof Colors.light & keyof typeof Colors.dark
) {
  const theme = useColorScheme() ?? 'light';
  const colorFromProps = props[theme];

  if (colorFromProps) {
    return colorFromProps;
  } else {
    return Colors[theme][colorName].toString();
  }
}

export default useThemeColor;
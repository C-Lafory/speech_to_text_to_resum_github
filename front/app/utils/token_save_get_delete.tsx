import * as FileSystem from 'expo-file-system';

const TOKEN_FILE_PATH = `${FileSystem.documentDirectory}sessionToken.txt`;

// Fonction pour sauvegarder un token
export const saveToken = async (token: string): Promise<void> => {
  try {
    // Écrit la chaîne dans le fichier
    await FileSystem.writeAsStringAsync(TOKEN_FILE_PATH, token, {
      encoding: FileSystem.EncodingType.UTF8,
    });
    console.log('Token sauvegardé avec succès dans :', TOKEN_FILE_PATH);
  } catch (error) {
    console.error('Erreur lors de la sauvegarde du token :', error);
  }
};

// Fonction pour récupérer un token
export const getToken = async (): Promise<string | null> => {
  try {
    const fileInfo = await FileSystem.getInfoAsync(TOKEN_FILE_PATH);
    if (fileInfo.exists) {
      const token = await FileSystem.readAsStringAsync(TOKEN_FILE_PATH, {
        encoding: FileSystem.EncodingType.UTF8,
      });
      return token;
    } else {
      console.warn('Aucun token trouvé.');
      return null;
    }
  } catch (error) {
    console.error('Erreur lors de la récupération du token:', error);
    return null;
  }
};

// Fonction pour supprimer un token
export const deleteToken = async (): Promise<void> => {
  try {
    const fileInfo = await FileSystem.getInfoAsync(TOKEN_FILE_PATH);
    if (fileInfo.exists) {
      await FileSystem.deleteAsync(TOKEN_FILE_PATH);
      console.log('Token supprimé avec succès.');
    } else {
      console.warn('Aucun token à supprimer.');
    }
  } catch (error) {
    console.error('Erreur lors de la suppression du token:', error);
  }
};
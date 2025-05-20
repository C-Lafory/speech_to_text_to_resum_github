import * as FileSystem from 'expo-file-system';

const TOKEN_FILE_PATH = `${FileSystem.documentDirectory}sessionToken.txt`;

// Fonction pour sauvegarder un token
export const saveToken = async (token: string): Promise<void> => {
  try {
    console.log('Tentative de sauvegarde du token:', token.substring(0, 10) + '...');
    console.log('Chemin du fichier:', TOKEN_FILE_PATH);
    
    // Écrit la chaîne dans le fichier
    await FileSystem.writeAsStringAsync(TOKEN_FILE_PATH, token, {
      encoding: FileSystem.EncodingType.UTF8,
    });
    
    // Vérification que le token a bien été écrit
    const fileInfo = await FileSystem.getInfoAsync(TOKEN_FILE_PATH);
    console.log('Fichier créé:', fileInfo.exists);
    
    if (fileInfo.exists) {
      const savedToken = await FileSystem.readAsStringAsync(TOKEN_FILE_PATH);
      console.log('Token vérifié après sauvegarde:', savedToken.substring(0, 10) + '...');
    }
    
    console.log('Token sauvegardé avec succès dans :', TOKEN_FILE_PATH);
  } catch (error) {
    console.error('Erreur détaillée lors de la sauvegarde du token :', error);
    throw error; // Propager l'erreur pour la gérer dans le composant
  }
};

// Fonction pour récupérer un token
export const getToken = async (): Promise<string | null> => {
  try {
    console.log('Tentative de récupération du token depuis:', TOKEN_FILE_PATH);
    const fileInfo = await FileSystem.getInfoAsync(TOKEN_FILE_PATH);
    console.log('Statut du fichier:', fileInfo);
    
    if (fileInfo.exists) {
      const token = await FileSystem.readAsStringAsync(TOKEN_FILE_PATH, {
        encoding: FileSystem.EncodingType.UTF8,
      });
      console.log('Token récupéré:', token.substring(0, 10) + '...');
      return token;
    } else {
      console.warn('Aucun token trouvé.');
      return null;
    }
  } catch (error) {
    console.error('Erreur détaillée lors de la récupération du token:', error);
    return null;
  }
};

// Fonction pour supprimer un token
export const deleteToken = async (): Promise<void> => {
  try {
    console.log('Tentative de suppression du token depuis:', TOKEN_FILE_PATH);
    const fileInfo = await FileSystem.getInfoAsync(TOKEN_FILE_PATH);
    console.log('Statut du fichier avant suppression:', fileInfo);
    
    if (fileInfo.exists) {
      await FileSystem.deleteAsync(TOKEN_FILE_PATH);
      console.log('Token supprimé avec succès.');
    } else {
      console.warn('Aucun token à supprimer.');
    }
  } catch (error) {
    console.error('Erreur détaillée lors de la suppression du token:', error);
    throw error; // Propager l'erreur pour la gérer dans le composant
  }
};
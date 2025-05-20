import React, { useEffect, useState, } from 'react';
import { View, Text, FlatList, StyleSheet, Button, TouchableOpacity,Alert } from 'react-native';
import * as FileSystem from 'expo-file-system';
import { Audio } from 'expo-av';
import { deleteToken, getToken } from '../utils/token_save_get_delete';
import { useNavigation } from "@react-navigation/native";
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../types/_navigation'; // Import du type RootStackParamList
import { deleteAllFiles,fetchRecordings } from '../utils/fileUtils';

export default function Settings() {
    const [localRecordings, setLocalRecordings] = useState<string[]>([]);
    const [sound, setSound] = useState<Audio.Sound | null>(null);
    

  type LoginScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Main'>;
    const navigation = useNavigation<LoginScreenNavigationProp>();
    // console.log('Navigation object:', navigation);
    // Fonction pour logout
    const handleLogout = () => {
      deleteToken(); // Supprimer le token de session
      let test = getToken(); 
      // Vérifier que le token est bien supprimé (pour debug)
      console.log("Token after deletion:", test);
      Alert.alert("Logged Out", "You have been logged out successfully.");
      navigation.navigate("Login"); // Rediriger vers la page Login
    };

    const handleDeleteAllFiles = async () => {
        await deleteAllFiles();
        loadLocalRecordings(); // Recharger les fichiers locaux
  };

    // Fonction pour charger les fichiers locaux
    const loadLocalRecordings = async () => {
        try {
            const audioFiles = await fetchRecordings('.m4a'); // Charger uniquement les fichiers `.m4a`
            setLocalRecordings(audioFiles);
        } catch (error) {
            console.error('Error reading local recordings:', error);
        }
    };
    
    // const loadLocalRecordings = async () => {
    //     try {
    //         const directory = `${FileSystem.documentDirectory}recordings/`;
    //         const files = await FileSystem.readDirectoryAsync(directory);
    //         const audioFiles = files.filter(file => file.endsWith('.m4a')); // Filtrer les fichiers audio
    //         setLocalRecordings(audioFiles);
    //     } catch (error) {
    //         console.error('Error reading local recordings:', error);
    //     }
    // };

    // Fonction pour jouer un fichier audio
    const playRecording = async (fileName: string) => {
        const fileUri = `${FileSystem.documentDirectory}recordings/${fileName}`;
        console.log('Playing file:', fileUri);

        try {
            // Libérer le son précédent s'il existe
            if (sound) {
                await sound.unloadAsync();
            }

            const { sound: newSound } = await Audio.Sound.createAsync({ uri: fileUri });
            setSound(newSound);
            await newSound.playAsync();
        } catch (error) {
            console.error('Error playing audio:', error);
        }
    };

    // Libérer les ressources audio lorsque le composant est démonté
    useEffect(() => {
        return () => {
            if (sound) {
                sound.unloadAsync();
            }
        };
    }, [sound]);

    // Charger les fichiers au montage du composant
    useEffect(() => {
        loadLocalRecordings();
    }, []);

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Local Recordings</Text>
            {localRecordings.length > 0 ? (
                <FlatList
                    data={localRecordings}
                    keyExtractor={(item, index) => index.toString()}
                    renderItem={({ item }) => (
                        <TouchableOpacity onPress={() => playRecording(item)}>
                            <Text style={styles.item}>{item}</Text>
                        </TouchableOpacity>
                    )}
                />
            ) : (
                <Text style={styles.noFiles}>No recordings found.</Text>
            )}
            <Button title="Delete All Files" onPress={handleDeleteAllFiles} />
            <Button title="Refresh" onPress={loadLocalRecordings} />
            <Button title="Log Out" onPress={handleLogout} />
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 20,
        paddingBottom: 80, // Ajoutez un espace pour éviter que le bouton soit caché
        backgroundColor: '#f5f5f5',
    },
    title: {
        fontSize: 20,
        fontWeight: 'bold',
        marginBottom: 10,
    },
    item: {
        fontSize: 16,
        padding: 10,
        borderBottomWidth: 1,
        borderBottomColor: '#ccc',
        color: 'blue', // Ajoutez une couleur pour indiquer que c'est cliquable
    },
    noFiles: {
        fontSize: 16,
        color: '#888',
        textAlign: 'center',
        marginTop: 20,
    },
});

// import { Text, View, Button, Alert } from "react-native";
// import { useThemeColor } from "../hooks/useThemeColor";
// import { useNavigation } from "@react-navigation/native";
// import { StackNavigationProp } from '@react-navigation/stack';
// import { RootStackParamList } from '../types/navigation'; // Import du type RootStackParamList
// import { deleteToken, getToken } from '../func/token_save_get_delete';


// export default function Settings() {

//   type LoginScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Main'>;
//     const navigation = useNavigation<LoginScreenNavigationProp>();
//     // console.log('Navigation object:', navigation);

//   const handleLogout = () => {
//     // Logique de déconnexion (par exemple, réinitialiser les états globaux ou supprimer les tokens)
//     deleteToken(); // Supprimer le token de session
//     let test = getToken(); // Vérifier que le token est bien supprimé (pour debug)
//     console.log("Token after deletion:", test);
//     // console.log("Token deleted successfully");
//     Alert.alert("Logged Out", "You have been logged out successfully.");
//     navigation.navigate("Login"); // Rediriger vers la page Login
//   };

//   return (
//     <View
//       style={{
//         flex: 1,
//         justifyContent: "center",
//         alignItems: "center",
//         backgroundColor: useThemeColor({}, "background"),
//       }}
//     >
//       <Text>Settings page</Text>
//       <Button title="Log Out" onPress={handleLogout} />
//     </View>
//   );
// }
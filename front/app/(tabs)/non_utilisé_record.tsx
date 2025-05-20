import React, { createContext, useEffect, useRef, useState } from 'react';
import { View, SafeAreaView, FlatList, Text, StyleSheet, Button} from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import * as FileSystem from 'expo-file-system';
import { useThemeColor } from "../hooks/useThemeColor";
import Resume from '../components/description/resume';
import CheckFiles from '../components/Checkfile/Checkfile';
import { PlayerProvider} from '../contexts/playerContext';
import usePlayer from '../contexts/playerContext'; 

// Contexte pour gérer les enregistrements audio.
// Permet de charger, envoyer et supprimer des enregistrements audio.
// Utilisé dans les composants Recorder, Description et Player.

// Propriétés du contexte :
// recordings : Liste des enregistrements audio.
// sendRecording : Fonction pour envoyer un enregistrement audio en base 64.
// deleteRecording : Fonction pour supprimer un enregistrement audio.
// loadRecordings : Fonction pour charger les enregistrements audio.


export default function Record() {
    const textColor = useThemeColor({}, 'text');
    const { sendRecording,isLoadingJson } = usePlayer();

    const handleSendRecording = () => {
        const uri = (`${FileSystem.documentDirectory}recordings/`) // Remplacez par le chemin réel de votre enregistrement
        console.log("record.tsx Sending recording:", uri);
        if (sendRecording) {
            sendRecording(uri);
        } else {
            console.error("sendRecording is undefined");
        }
    };
        return (
            <PlayerProvider>
                <View style={{ backgroundColor: useThemeColor({}, "background"), flex: 1 }}>
                    <View style={styles.container}>
                        <Text style={[styles.text, { color: textColor }]}>Check the console for the list of files.</Text>
                        <Button title="Send Recording" onPress={handleSendRecording} />
                    </View>
                </View>
               <View style={styles.container}>
                {/* <CheckFiles style={styles.checkFilesContainer} /> */}
                </View>
            </PlayerProvider>
        );
    };


const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    checkFilesContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    text: {
        fontSize: 16,
        color: 'white', // Couleur par défaut, sera remplacée par textColor
    },
});


//   <View style={styles.container}>
//         {/* <Text style={[styles.text, { color: textColor }]}>Check the console for the list of files.</Text> */}
//         <CheckFiles style={styles.checkFilesContainer} />
//       </View> a ajouter dans record pour affciher les fichier enregistrer

// pour afficher les file enregistrer 
{/* <PlayerProvider>
            <View style={{ backgroundColor: useThemeColor({}, "background"), flex: 1 }}>
                <View style={styles.container}>
                    <Text style={[styles.text, { color: textColor }]}></Text>
                    <CheckFiles style={styles.checkFilesContainer} />
                </View>
            </View>
        </PlayerProvider> */}

// explication
//     Définir le contexte PlayerContext : Le contexte PlayerContext est défini dans playerContext.tsx et exporté pour être utilisé dans d'autres composants.
// Utiliser PlayerProvider : Le composant PlayerProvider enveloppe le composant principal dans record.tsx pour fournir le contexte à tous les composants enfants.
// Accéder au contexte : Les composants enfants peuvent accéder aux fonctions et aux états définis dans PlayerProvider en utilisant le hook usePlayer.

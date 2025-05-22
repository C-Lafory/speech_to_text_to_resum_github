import { createContext, useContext, useState } from "react";
import { getToken } from "../utils/token_save_get_delete";
import { Alert } from 'react-native';

// Contexte pour gérer les enregistrements audio.
// Permet de charger, envoyer et supprimer des enregistrements audio.
// Utilisé dans les composants Recorder, Description et Player.

// Propriétés du contexte :
// recordings : Liste des enregistrements audio.
// sendRecording : Fonction pour envoyer un enregistrement audio en base 64.
// deleteRecording : Fonction pour supprimer un enregistrement audio.
// loadRecordings : Fonction pour charger les enregistrements audio.

interface RecordingData {
    date: string;           // Date de création comme titre
    transcription: string;  // Contenu de la transcription
    summary: string;        // Contenu du résumé
    audioInputData: string; // Données audio en base64
    audioOutputData: string;// Données audio en base64
}

interface PlayerContextProps {
    recordings: string[];
    sendRecording?: (uri: string) => void;
    loadAllRecordings: () => void;
    jsonContent: any[];
    isLoadingJson: boolean;
}

const PlayerContext = createContext<PlayerContextProps>({
    recordings: [],
    loadAllRecordings: () => { },
    sendRecording: () => { },
    jsonContent: [],
    isLoadingJson: false,
});

export function usePlayer() {
    return useContext(PlayerContext);
}

export function PlayerProvider({ children }: any) {
    const [recordings, setRecordings] = useState<string[]>([]);
    const [jsonContent, setJsonContent] = useState<RecordingData[]>([]);
    const [isLoadingJson, setIsLoadingJson] = useState(false);

    const loadAllRecordings = async () => {
        try {
            //Alert.alert('Debug', '1. Début du chargement des enregistrements');
            
            const token = await getToken();
            //Alert.alert('Debug', `2. Token récupéré: ${token ? 'Oui' : 'Non'}`);
            
            if (!token) {
                Alert.alert('Debug', '3. Pas de token trouvé');
                throw new Error("No token found");
            }

            //Alert.alert('Debug', '4. Envoi de la requête au serveur');
            const response = await fetch('http://vps-692a3a83.vps.ovh.net:5048/api/files', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
            });
            
            // Ajout de plus de détails sur la réponse
    //         Alert.alert('Debug', `5. Réponse reçue:
    // Status: ${response.status}
    // Status Text: ${response.statusText}
    // Headers: ${JSON.stringify(Object.fromEntries(response.headers))}`);

            if (!response.ok) {
                // Tentative de lire le message d'erreur du serveur
                const errorText = await response.text();
    //             Alert.alert('Debug', `6. Réponse non OK:
    // Status: ${response.status}
    // Error: ${errorText}`);
                throw new Error(`Failed to fetch recordings from server: ${response.status} - ${errorText}`);
            }
            // Alert.alert('Debug', '7. Réponse OK, traitement des données');
            const data = await response.json();
            // Alert.alert('Debug', `8. Données reçues: ${JSON.stringify(data)}`);
            setJsonContent(data);
            setRecordings(data.map((item: RecordingData) => item.audioInputData));
            // Alert.alert('Debug', '9. Enregistrements chargés avec succès');
            // Affichage des enregistrements dans la console
            console.log('Enregistrements:', data);
            console.log('Enregistrements audio:', data.map((item: RecordingData) => item.audioInputData));
            console.log('Enregistrements audio:', recordings);

            // ... reste du code ...
        } catch (error) {
            console.error('Erreur détaillée:', error);
            return [];
        }
    }

    const sendRecording = async (uri: string) => {
        setIsLoadingJson(true);
        try {
            const token = await getToken();
            if (!token) {
                throw new Error("No token found");
            }

            const formData = new FormData();
            formData.append('file', {
                uri: uri,
                type: 'audio/mp4',
                name: 'recording.m4a'
            } as any);

            const response = await fetch("http://vps-692a3a83.vps.ovh.net:5048/api/audio", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Erreur HTTP: ${response.status}`);
            }

            setIsLoadingJson(false);
        } catch (err) {
            console.error("Erreur lors de l'envoi de l'enregistrement:", err);
            setIsLoadingJson(false);
        }
    };

    return (
        <PlayerContext.Provider value={{
            recordings,
            loadAllRecordings,
            sendRecording,
            jsonContent,
            isLoadingJson
        }}>
            {children}
        </PlayerContext.Provider>
    );
}

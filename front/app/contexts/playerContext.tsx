import { createContext, useContext, useState } from "react";
import { getToken } from "../utils/token_save_get_delete";

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
            alert('1. Début du chargement des enregistrements');
            const token = await getToken();
            alert('2. Token récupéré: ' + (token ? 'Oui' : 'Non'));
            
            if (!token) {
                throw new Error("No token found");
            }
    
            alert('3. Envoi de la requête au serveur');
            const response = await fetch('http://vps-692a3a83.vps.ovh.net:5048/api/files', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
            });
          
            alert('4. Réponse reçue, status: ' + response.status);
            if (!response.ok) {
                throw new Error(`Failed to fetch recordings from server: ${response.status}`);
            }
    
            const rawData = await response.json();
            alert('5. Données reçues: ' + JSON.stringify(rawData));
    
            const serverData: RecordingData[] = rawData;
            alert('6. Données formatées: ' + JSON.stringify(serverData));
          
            setJsonContent(serverData);
            return serverData;
        } catch (error) {
            alert('Erreur détaillée: ' + error);
            return [];
        }
    };

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

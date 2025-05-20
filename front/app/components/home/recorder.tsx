import { useState, useEffect } from "react";
import { Pressable, Text, View } from "react-native";

import MaterialIcons from "@expo/vector-icons/MaterialIcons";
import { Audio } from "expo-av";
import * as FileSystem from "expo-file-system";

import usePlayer from "@/app/contexts/playerContext";
import { useThemeColor } from "@/app/hooks/useThemeColor";

export default function Recorder() {
    // const [RecordName, setRecordName ] = useState(0);
    // const incrementer  = () => {
    //     setRecordName(prevCount => prevCount + 1);
    // }

    const [recording, setRecording] = useState<Audio.Recording | null>(null);
    // const [savedRecordings, setSavedRecordings] = useState<string[]>([]);

    const [isRecording, setIsRecording] = useState(false);
    const { sendRecording, loadRecordings } = usePlayer();

    // useEffect(() => {
    //     const fetchRecordings = async () => {
    //         const dir = `${FileSystem.documentDirectory}recordings/`;
    //         const files = await FileSystem.readDirectoryAsync(dir);
    //         setSavedRecordings(files);
    //     };

    //     fetchRecordings();
    // }, []);

    const createDirectory = async () => {
        const dir = `${FileSystem.documentDirectory}recordings/`;
        const dirInfo = await FileSystem.getInfoAsync(dir);

        if (dirInfo.exists) {
            console.log('Directory already exists at', dir);
            return dir;
        }

        await FileSystem.makeDirectoryAsync(dir, { intermediates: true });
        console.log('Directory created at', dir);
        return dir;
    };

    // fonction pour demmarer l'enregistrement ou l'arreter
    const toggleRecording = async () => {
        if (isRecording) {
            console.log("Stopping recording..");
            await recording?.stopAndUnloadAsync();

            const uri = recording?.getURI();
            const dir = await createDirectory();

            if (!uri) {
                console.error("Failed to get URI of the recording");
                return;
            }

            const newUri = `${dir}${Date.now()}.m4a`;
            await FileSystem.moveAsync({
                from: uri,
                to: newUri,
            });

            console.log("Recording moved to", newUri);

            // Convert the recording to base64
            if (newUri && sendRecording) {
                sendRecording(newUri);

                // Supprimer le fichier local après l'envoi
                // await FileSystem.deleteAsync(newUri);
                // console.log("Local recording deleted after upload");
            }

            loadRecordings();

            setRecording(null);
            setIsRecording(false);
        } else {
            try {

                console.log("Requesting permissions..");

                const { status } = await Audio.requestPermissionsAsync();
                if (status !== "granted") {
                    alert("Permission to access microphone is required!");
                }

                await Audio.setAudioModeAsync({
                    allowsRecordingIOS: true,
                    playsInSilentModeIOS: true,
                });

                console.log("Starting recording..");
                const { recording } = await Audio.Recording.createAsync(
                    Audio.RecordingOptionsPresets.HIGH_QUALITY
                );
                
                setRecording(recording);
                console.log("Recording started");
            } catch (err) {
                console.error("Failed to start recording", err);
            }
        }
        setIsRecording(!isRecording);
    }

    return (
        <View>
            <Pressable
                onPress={toggleRecording}
                style={({ pressed }) => [
                    {
                        backgroundColor: pressed ? 'white' : 'transparent',
                        borderColor: useThemeColor({}, 'icon'),
                        borderWidth: 1,
                        padding: 10,
                        borderRadius: 100,
                        width: 200,
                        height: 200,
                        justifyContent: 'center',
                        alignItems: 'center',
                    },
                ]}
            >
                <MaterialIcons size={150} name="mic" color={'purple'} />
            </Pressable>
        </View>
    )
}
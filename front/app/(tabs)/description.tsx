import React, { useEffect, useRef, useState } from 'react';
import { View, SafeAreaView, FlatList, Text, StyleSheet, ActivityIndicator, Pressable } from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { usePlayer } from '../contexts/playerContext';
import { Audio } from 'expo-av';
import MaterialIcons from "@expo/vector-icons/MaterialIcons";
import { getToken } from '../utils/token_save_get_delete';

export default function Description() {
    const { loadAllRecordings, jsonContent, isLoadingJson } = usePlayer();
    const scrollRef = useRef<FlatList>(null);
    const [sound, setSound] = useState<Audio.Sound | null>(null);
    const [isPlaying, setIsPlaying] = useState(false);

    useEffect(() => {
        loadAllRecordings();
        return () => {
            if (sound) {
                sound.unloadAsync();
            }
        };
    }, []);

    const playAudio = async (audioData: string) => {
        try {
            if (sound) {
                await sound.unloadAsync();
            }

            const { sound: newSound } = await Audio.Sound.createAsync(
                { uri: `data:audio/mp4;base64,${audioData}` },
                { shouldPlay: true }
            );

            setSound(newSound);
            setIsPlaying(true);

            newSound.setOnPlaybackStatusUpdate((status) => {
                if (status.isLoaded && status.didJustFinish) {
                    setIsPlaying(false);
                }
            });
        } catch (error) {
            console.error('Erreur lors de la lecture audio:', error);
        }
    };

    const stopAudio = async () => {
        if (sound) {
            await sound.stopAsync();
            setIsPlaying(false);
        }
    };

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleString('fr-FR', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    return (
        <GestureHandlerRootView style={{ flex: 1 }}>
            <SafeAreaView style={styles.container}>
                {isLoadingJson ? (
                    <ActivityIndicator size="large" color="#0000ff" />
                ) : (
                    <FlatList
                        ref={scrollRef}
                        data={jsonContent}
                        keyExtractor={(item, index) => index.toString()}
                        renderItem={({ item }) => (
                            <View style={styles.recordingItem}>
                                <Text style={styles.date}>
                                    Enregistré le {formatDate(item.date)}
                                </Text>
                                
                                <View style={styles.audioControls}>
                                    <Pressable
                                        onPress={() => isPlaying ? stopAudio() : playAudio(item.audioInputData)}
                                        style={styles.audioButton}
                                    >
                                        <MaterialIcons 
                                            name={isPlaying ? "stop" : "play-arrow"} 
                                            size={24} 
                                            color="purple" 
                                        />
                                        <Text style={styles.audioButtonText}>
                                            {isPlaying ? "Arrêter" : "Écouter l'enregistrement"}
                                        </Text>
                                    </Pressable>

                                    <Pressable
                                        onPress={() => isPlaying ? stopAudio() : playAudio(item.audioOutputData)}
                                        style={styles.audioButton}
                                    >
                                        <MaterialIcons 
                                            name={isPlaying ? "stop" : "play-arrow"} 
                                            size={24} 
                                            color="purple" 
                                        />
                                        <Text style={styles.audioButtonText}>
                                            {isPlaying ? "Arrêter" : "Écouter le résumé"}
                                        </Text>
                                    </Pressable>
                                </View>

                                <Text style={styles.title}>Transcription :</Text>
                                <Text style={styles.transcription}>{item.transcription}</Text>
                                <Text style={styles.title}>Résumé :</Text>
                                <Text style={styles.summary}>{item.summary}</Text>
                            </View>
                        )}
                    />
                )}
            </SafeAreaView>
        </GestureHandlerRootView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 16,
    },
    recordingItem: {
        marginBottom: 16,
        padding: 16,
        backgroundColor: '#f5f5f5',
        borderRadius: 8,
    },
    date: {
        fontSize: 12,
        color: '#666',
        marginBottom: 8,
    },
    audioControls: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        marginBottom: 16,
    },
    audioButton: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#fff',
        padding: 8,
        borderRadius: 20,
        borderWidth: 1,
        borderColor: 'purple',
    },
    audioButtonText: {
        marginLeft: 8,
        color: 'purple',
    },
    title: {
        fontSize: 16,
        fontWeight: 'bold',
        marginTop: 8,
        marginBottom: 4,
    },
    transcription: {
        fontSize: 16,
        marginBottom: 8,
    },
    summary: {
        fontSize: 14,
        color: '#666',
        marginBottom: 8,
    },
});
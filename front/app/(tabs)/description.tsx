import React, { useEffect, useRef, useState } from 'react';
import { View, SafeAreaView, FlatList, Text, StyleSheet, ActivityIndicator, Pressable, ScrollView } from 'react-native';
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
    }, []);

    const handleRefresh = async () => {
        alert('Rafraîchissement des données...');
        await loadAllRecordings();
    };

    useEffect(() => {
        if (jsonContent && jsonContent.length > 0) {
            alert('Données reçues : ' + jsonContent.length + ' enregistrements');
        }
    }, [jsonContent]);

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
            alert('Erreur lecture audio: ' + error);
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
                <View style={styles.header}>
                    <Text style={styles.headerTitle}>Mes enregistrements</Text>
                    <Pressable
                        onPress={handleRefresh}
                        style={styles.refreshButton}
                    >
                        <MaterialIcons 
                            name="refresh" 
                            size={24} 
                            color="purple" 
                        />
                    </Pressable>
                </View>

                {isLoadingJson ? (
                    <ActivityIndicator size="large" color="#0000ff" />
                ) : jsonContent && jsonContent.length > 0 ? (
                    <FlatList
                        ref={scrollRef}
                        data={jsonContent}
                        keyExtractor={(item, index) => index.toString()}
                        renderItem={({ item }) => {
                            alert('Rendu de l\'item : ' + JSON.stringify(item));
                            return (
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
                            );
                        }}
                    />
                ) : (
                    <View style={styles.noDataContainer}>
                        <Text style={styles.noDataText}>Aucun enregistrement disponible</Text>
                    </View>
                )}
            </SafeAreaView>
        </GestureHandlerRootView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 16,
        backgroundColor: '#fff',
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 16,
    },
    headerTitle: {
        fontSize: 20,
        fontWeight: 'bold',
        color: '#333',
    },
    refreshButton: {
        padding: 8,
        borderRadius: 20,
        backgroundColor: '#f5f5f5',
    },
    recordingItem: {
        marginBottom: 16,
        padding: 16,
        backgroundColor: '#f5f5f5',
        borderRadius: 8,
        elevation: 2,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
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
        color: '#333',
    },
    transcription: {
        fontSize: 16,
        marginBottom: 8,
        color: '#444',
        lineHeight: 24,
    },
    summary: {
        fontSize: 14,
        color: '#666',
        marginBottom: 8,
        lineHeight: 20,
    },
    noDataContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
    },
    noDataText: {
        fontSize: 16,
        color: '#666',
    },
});
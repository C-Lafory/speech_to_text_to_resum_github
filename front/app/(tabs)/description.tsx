import React, { useEffect, useRef } from 'react';
import { View, SafeAreaView, FlatList, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import {usePlayer} from '../contexts/playerContext';

export default function Description() {
    const { loadAllRecordings, jsonContent, isLoadingJson } = usePlayer();
    const scrollRef = useRef<FlatList>(null);

    // Charger les enregistrements au montage du composant
    useEffect(() => {
        loadAllRecordings();
    }, []);

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
                                <Text style={styles.transcription}>{item.transcription}</Text>
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
    transcription: {
        fontSize: 16,
        marginBottom: 8,
    },
    summary: {
        fontSize: 14,
        color: '#666',
    },
});
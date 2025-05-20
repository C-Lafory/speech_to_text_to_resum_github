import React, { useEffect, useState, useRef } from "react";
import { View, Button, Pressable, StyleSheet , FlatList, SafeAreaView} from "react-native";
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import Slider from '@react-native-community/slider';
import MaterialIcons from "@expo/vector-icons/MaterialIcons";

import * as FileSystem from "expo-file-system";
import { Audio } from "expo-av";

import { useThemeColor } from "@/app/hooks/useThemeColor";

// États locaux :

// soundState : Stocke l'état du son en cours de lecture.
// isPlaying : Indique si un enregistrement est en cours de lecture.
// isSliderChanging : Indique si l'utilisateur est en train de changer la position du curseur.
// position : Position actuelle de la lecture (en millisecondes).
// duration : Durée totale de l'enregistrement (en millisecondes).

// Fonctions principales :

// playRecording : Joue un enregistrement à partir d'une URI donnée.
// pauseRecording : Met en pause l'enregistrement en cours.
// onPlaybackStatusUpdate : Met à jour l'état de la lecture (position, durée) et gère la fin de la lecture.
// handleSliderChange : Met à jour la position de la lecture lorsque l'utilisateur change la position du curseur.

// Rendu du composant :

// Affiche un bouton de lecture/pause.
// Affiche un curseur pour contrôler la position de la lecture.
// Affiche un bouton pour supprimer l'enregistrement.

interface PlayerProps {
    item: string;
}

export default function Player({ item }: PlayerProps) {
    const [soundState, setSoundState] = useState<Audio.Sound | null>(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [isSliderChanging, setIsSliderChanging] = useState(false);
    const [position, setPosition] = useState(0);
    const [duration, setDuration] = useState(0);

    const playRecording = async (uri: string) => {
        const { sound } = await Audio.Sound.createAsync({ uri });
        sound?.setOnPlaybackStatusUpdate((status) => onPlaybackStatusUpdate(status, sound));
        await sound?.setPositionAsync(position);
        await sound?.playAsync();
        setSoundState(sound);
        setIsPlaying(true);
    };

    const pauseRecording = async () => {
        await soundState?.pauseAsync();
        setIsPlaying(false);
    };

    const onPlaybackStatusUpdate = async (status: any, sound: Audio.Sound) => {
        if (status.isLoaded) {
            setPosition(status.positionMillis);
            setDuration(status.durationMillis);
            if (status.didJustFinish) {
                setIsPlaying(false);
                setPosition(0);
                await sound?.unloadAsync();
                console.log("Playback finished");
            }
        }
    };

    const handleSliderChange = async (value: number) => {
        if (soundState && isSliderChanging) {
            await soundState?.setPositionAsync(value);
        }
    };

    const sliderStyle = StyleSheet.create({
        sliderDummy: {
            backgroundColor: useThemeColor({}, "icon"),
            width: 260,
            height: 10,
            borderRadius: 50,
            position: 'absolute',
        },
        sliderReal: {
            backgroundColor: useThemeColor({}, "tint"),
            width: (position / duration) * 260,
            borderBottomLeftRadius: 50,
            borderTopLeftRadius: 50,
            height: 10,
        }
    });

    return (
        <View style={{ flexDirection: 'row', justifyContent: 'space-evenly', padding: 10, alignItems: 'center', flex: 1 }}>
            <Pressable onPress={() => isPlaying ? pauseRecording() : playRecording(`${FileSystem.documentDirectory}${item}`)}>
                <MaterialIcons size={20} name={isPlaying ? "pause" : "play-arrow"} color={useThemeColor({}, "text")} />
            </Pressable>
            <View style={{ borderRadius: 50 }}>
                <View style={{ flexDirection: 'row', position: 'absolute' }}>
                    <View style={sliderStyle.sliderDummy}></View>
                    <View style={sliderStyle.sliderReal}></View>
                </View>
                <Slider
                    style={{width: 260, height: 10, borderRadius: 50}}
                    minimumValue={0}
                    maximumValue={duration}
                    value={position}
                    step={1}
                    onTouchStart={() => setIsSliderChanging(true)}
                    onTouchEnd={() => setIsSliderChanging(false)}
                    onValueChange={handleSliderChange}
                    maximumTrackTintColor="transparent"
                    minimumTrackTintColor="transparent"
                    thumbTintColor="transparent"
                />
            </View>
        </View>
    )
}
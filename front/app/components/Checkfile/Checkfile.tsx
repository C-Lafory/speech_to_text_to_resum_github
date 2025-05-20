import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, StyleSheet, ViewStyle } from 'react-native';
import * as FileSystem from 'expo-file-system';
// import Player from "../description/player"; // Commentez cette ligne si Player cause l'erreur
import usePlayer from '@/app/contexts/playerContext';

interface CheckFilesProps {
  style?: ViewStyle;
}

export default function CheckFiles({ style }: CheckFilesProps) {
  const [files, setFiles] = useState<string[]>([]);
  const [jsonContent, setJsonContent] = useState<any>(null);
  const { loadRecordings } = usePlayer();

  useEffect(() => {
    const checkFiles = async () => {
      try {
        const files = await FileSystem.readDirectoryAsync(`${FileSystem.documentDirectory}recordings/`);
        setFiles(files);
        console.log('Dans checkfile mes Files:', files);
        loadRecordings();
      } catch (error) {
        console.error('Error reading directory:', error);
      }
    };

    const readJsonFile = async () => {
      try {
        const fileUri = `${FileSystem.documentDirectory}response.json`;
        console.log('checkfile.tsx FileSystem.documentDirectory:', fileUri); 
        const json = await FileSystem.readAsStringAsync(fileUri, {
          encoding: FileSystem.EncodingType.UTF8,
        });
        setJsonContent(JSON.parse(json));
        console.log('Checkfile.tsx l36 JSON content:', jsonContent);
      } catch (error) {
        console.error('Error reading JSON file:', error);
      }
    };

    checkFiles();
    readJsonFile();
  }, []);

  return (
    <View style={[styles.container, style]}>
      <Text>Check the console for the list of files.</Text>
      <FlatList
        data={files}
        keyExtractor={(item) => item}
        renderItem={({ item }) => (
          <View style={styles.fileContainer}>
            <Text style={styles.fileText}>{item}</Text>
            {/* <Player item={item} /> */} {/* Commentez cette ligne si Player cause l'erreur */}
          </View>
        )}
      />
      {jsonContent && (
        <View style={styles.jsonContainer}>
          <Text>JSON Response:</Text>
          <Text>{JSON.stringify(jsonContent, null, 2)}</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'lightgrey', // Ajoutez une couleur de fond pour le débogage
  },
  fileContainer: {
    marginVertical: 10,
    alignItems: 'center',
  },
  fileText: {
    fontSize: 16,
    marginVertical: 5,
    color: 'black',
  },
  jsonContainer: {
    marginTop: 20,
    padding: 10,
    backgroundColor: 'white',
    borderRadius: 5,
  },
});
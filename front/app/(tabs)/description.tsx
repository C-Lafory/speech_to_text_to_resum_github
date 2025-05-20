import React, { useEffect, useRef, useState } from 'react';
import { View, SafeAreaView, FlatList, Text, StyleSheet,Button } from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import * as FileSystem from 'expo-file-system';
import { useThemeColor } from "../hooks/useThemeColor";
import Resume from "../components/description/resume";
import usePlayer from '../contexts/playerContext';
import loadRecordings from '../contexts/playerContext'; 


export default function Description() {
  const { jsonContent,recordings, loadRecordings } = usePlayer(); // Récupérer recordings et loadRecordings depuis le contexte
  // const { jsonContent } = usePlayer(); 
  const [jsonContents, setJsonContents] = useState<any[]>([]);
  const scrollRef = useRef<FlatList>(null);

  useEffect(() => {
    const readJsonFiles = async () => {
      try {
        if (!FileSystem.documentDirectory) {
          console.error("FileSystem.documentDirectory is null");
          return;
        }
  
        // Lire tous les fichiers dans le répertoire
        const files = await FileSystem.readDirectoryAsync(FileSystem.documentDirectory);
  
        // Filtrer uniquement les fichiers JSON
        const jsonFiles = files.filter(file => file.endsWith('.json'));
  
        // Lire et parser le contenu des fichiers JSON
        const parsedJsonContents = await Promise.all(
          jsonFiles.map(async (file) => {
            const fileUri = `${FileSystem.documentDirectory}${file}`;
            const json = await FileSystem.readAsStringAsync(fileUri, {
              encoding: FileSystem.EncodingType.UTF8,
            });
            return JSON.parse(json);
          })
        );
  
        // Mettre à jour l'état avec les nouvelles données
        setJsonContents(prevJsonContents => {
          const updatedContent = [...prevJsonContents, ...parsedJsonContents];
          console.log("DESCIPTION l44 Updated jsonContent:", updatedContent);
          return updatedContent;
        });
      } catch (error) {
        console.error('Error reading JSON files:', error);
      }
    };
  
    readJsonFiles();
  }, [recordings]);

  useEffect(() => {
    loadRecordings();
  }, []);


  const deleteAllFiles = async () => {
    try {
      if (!FileSystem.documentDirectory) {
        console.error("FileSystem.documentDirectory is null");
        return;
      }

      const files = await FileSystem.readDirectoryAsync(FileSystem.documentDirectory);

      await Promise.all(files.map(async (file) => {
        const fileUri = `${FileSystem.documentDirectory}${file}`;
        await FileSystem.deleteAsync(fileUri);
        console.log('Deleted file:', fileUri);
      }));

      setJsonContents([]);

      loadRecordings();
      console.log('description.tsx l84 All files deleted');
    } catch (error) {
      console.error('Error deleting files:', error);
    }
  };

  // Combiner recordings et jsonContents
  // const combinedData = [
  //   ...recordings.map((file) => ({
  //     audioUri: `${FileSystem.documentDirectory}recordings/${file}`,
  //     transcription: "",
  //     summary: "",
  //   })),
  //   ...jsonContents,
  // ];

  return (
    <GestureHandlerRootView>
      <View style={{ backgroundColor: useThemeColor({}, "background"), flex: 1 }}>
        <SafeAreaView
          style={{
            flex: 1,
            justifyContent: "center",
            alignItems: "center",
            paddingVertical: 30,
          }}
        >
          <Button title="Delete All Files" onPress={deleteAllFiles} />
            <FlatList
              ref={scrollRef}
              data={jsonContent} // Utilisation de jsonContent
              keyExtractor={(item, index) => index.toString()} // Utilisation de l'index comme clé
              renderItem={({ item, index }) => {
                  console.log("Data passed to Resume:", item);
                  return <Resume item={item} index={index} scrollRef={scrollRef} />;
              }}
          />
        </SafeAreaView>
      </View>
    </GestureHandlerRootView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  text: {
    fontSize: 16,
    color: 'white', // Couleur par défaut, sera remplacée par textColor
  },
});


//ANCIENNE FLATLIST POUR AFFICHER LES TRANDCRIPTION/RESUMER
{/* <Button title="Delete All Files" onPress={deleteAllFiles} /> 
          <FlatList
            ref={scrollRef}
            data={recordings} // quand je modifie avce jsonCOntent ca me modifie le contenus de mon print resume pourquoi 
            // (mais sa sauvegarde mes contenus de resume?
            keyExtractor={(item) => item}
            renderItem={({ item, index }) => (
              <Resume item={item} index={index} scrollRef={scrollRef} /> // Utilisez le composant Resume
            )}
          />
        </SafeAreaView>
      </View>
    </GestureHandlerRootView>
  );
} */}
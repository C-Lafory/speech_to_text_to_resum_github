pour build son repo : 
 - Crée un dossier
 - dans le dossier run "npx create-expo-app@latest <NOM DU PROJET>" 
 - commande pour avoir un projet vierge "npm run reset-project" (supprimer app-exemple)
 - npx expo start --tunnel( voir plus bas, pas besoin en local)

Pour build mon app :
- npx expo run

Pour lancer mon projet :
 - npx expo start (npx represente la verison local de mon projet)
 - Using : Expo go (fonctionne) et voir en mod devloppement switch avec "S".
 - (NPX est )
 - eas login (rentrée ces identifiant expo)
 - eas build:configure(choisir sont syteme d'exploitation android ios )


MODIFIER LA VARIABLE D'ENVIRONEMENT DE ANDROID : 
 - nano ~/.bashrc 
 - mettre ligne "export ANDROID_HOME="<chemin du sdk>"
 - ctrl+s 
 - ctrl + x
 - source ~/.bashrc
 - (verification echo $ANDROID_HOME) (cat ~/.bashrc)
 - npx expo run

--tunnel: Une option qui permet de créer un tunnel réseau, ce qui rend le projet accessible via une URL publique.
 Cela est utile pour tester sur des appareils physiques sans être sur le même réseau local.

OPTION : 
- restart lappli si elle freeze entrée "r" dans le terminal
Si le devices n'est pas detecter :
- adb kill-server
- adb start-server
- adb devices
Verifier que je suis dans le bon mod developement build (Press s)

--------------------------------------------------------------
POUR REBUILD MON PROJET :
eas build --platform android
-----------------------------------------------------------------

Pour les requetes utiliser AXIOS(plus de securiter) ou fetch (plus simple)

npx Un outil qui permet d'exécuter des packages Node.js sans les installer globalement.

expo Un framework et une plateforme pour les applications React Native.

start Une commande d'Expo qui démarre le serveur de développement.



DETAIL DU LANGAGE : 
view c'est comme une **DIV** en **HTML**
Text afficher du **texte**. Il prend en charge le **style**, la mise en forme, et la gestion des **événements tactiles**.

- cd speech_to_text
- npm start # you can open iOS, Android, or web from here, or run them directly with the commands below.
- npm run android
- npm run ios # requires an iOS device or macOS for access to an iOS simulator
- npm run web


1. VIDER LE CACHE DE TYPESCRIPT :
rm -rf node_modules/.cache
rm -rf .expo
2. reinstaller les dependance :
npm install
npx expo start

<!-- "Clef:" -->
- <!-- TODO: Ajouter une introduction détaillée ici -->
- <!-- FIXME: Corriger les liens brisés dans la section suivante -->
- <!-- REVIEW: Vérifier la mise en forme des listes -->
- <!-- IDEA: Ajouter une nouvelle section pour les FAQ -->

projet par partie : 
Collecting workspace information

Je n'ai pas modifié le code car vous n'avez pas demandé de modifications spécifiques. Voici un résumé des fichiers et de leurs responsabilités dans votre projet :

### Fichiers et leurs responsabilités

#### 

description.tsx


- **Responsabilité**: Affiche une liste d'enregistrements audio.
- **Affichage**: Utilise le composant resume.tsx pour chaque enregistrement.
- **Appelé par**: Lui-même, en tant que composant de la page Description.

#### 

resume.tsx


- **Responsabilité**: Affiche un résumé d'un enregistrement audio avec des options pour le lire et le supprimer.
- **Affichage**: Utilise le composant player.tsx pour lire l'audio.
- **Appelé par**: description.tsx

#### 

player.tsx


- **Responsabilité**: Lit un enregistrement audio.
- **Affichage**: Affiche des contrôles de lecture et un curseur pour la position de lecture.
- **Appelé par**: resume.tsx

#### 

index.tsx


- **Responsabilité**: Affiche la page d'accueil avec des options pour enregistrer de l'audio et sélectionner une langue.
- **Affichage**: Utilise les composants dropdown.tsx et recorder.tsx

- **Appelé par**: Lui-même, en tant que composant de la page d'accueil.

#### 

dropdown.tsx


- **Responsabilité**: Affiche un menu déroulant pour sélectionner une langue.
- **Affichage**: Affiche les options de langue.
- **Appelé par**: index.tsx


#### 

recorder.tsx


- **Responsabilité**: Enregistre de l'audio et affiche les enregistrements sauvegardés.
- **Affichage**: Affiche un bouton d'enregistrement et une liste des enregistrements.
- **Appelé par**: index.tsx

#### 

record.tsx


- **Responsabilité**: Affiche une liste des fichiers d'enregistrement.
- **Affichage**: Utilise le composant Checkfile.tsx pour afficher les fichiers.
- **Appelé par**: Lui-même, en tant que composant de la page Record.

#### 

Checkfile.tsx


- **Responsabilité**: Vérifie et affiche les fichiers d'enregistrement.
- **Affichage**: Affiche une liste des fichiers d'enregistrement.
- **Appelé par**: record.tsx

Si vous avez besoin de modifications spécifiques ou d'ajouter des fonctionnalités, veuillez me le faire savoir !

 <!-- -------------------------------------------------------------------------------------------------------------- -->
 <!-- -------------------------------------------------------------------------------------------------------------- -->
 <!-- -------------------------------------------------------------------------------------------------------------- -->

 Base React Native : 

 Les composants les plus utilisés sont :
    View : Un conteneur qui sert à regrouper plusieurs éléments
    Text : Pour afficher du texte
    Image : Pour afficher des images
    TextInput : Pour saisir du texte
    Button : Pour ajouter un bouton

useEffect :
    useEffect(() => {...}, [])	Exécute le code une seule fois quand le composant est affiché.
    useEffect(() => {...}, [variable])	Exécute le code chaque fois que la variable change.
    useEffect(() => {...}, []) avec return () => {...}	Nettoie les effets (ex: arrêter un setInterval).
    fetch(URL)	Appelle une API et récupère des données.

cheminement logique du record :


j'ai bien mes record dans le useffect de description.tsx (debut et fin "description.tsx JSON CONTEXT")
jaimerais comprendre exactement ce qui permet de recuperer ces record de jsonContent et de les afficher/mettre dans mes resume(faut il faire une fonction qui recupe mes record en local pour les renvoyer a mes resume au redemarage de mon appli) (peut etre modifier le double tableau en hashmap ?)

// quand je modifie avce jsonCOntent ca me modifie le contenus de mon print resume pourquoi ? (description.tsx l.107)

<!-- iimport React, { useEffect, useState, useRef } from "react";
import { View, Text, StyleSheet, TouchableOpacity, Dimensions, Animated, Button } from "react-native";
import { FlatList, ScrollView } from "react-native-gesture-handler";

import * as FileSystem from "expo-file-system";

import { useThemeColor } from "@/app/hooks/useThemeColor";
import Player from "./player";
import usePlayer from "@/app/contexts/playerContext";

// Rendu du composant :

// Affiche un résumé d'un enregistrement audio.

// Fonctions principales :

// useEffect : Met à jour et anime la hauteur et la largeur du composant en fonction de l'état de l'élément. (0 = base, 1 = semi-développé, 2 = totalement développé) 
// styleSheet : Feuille de styles en français. Regroupe tous les styles css du composant.
// handlePress : Gère le clic sur le composant et change l'état de l'élément.
// deleteRecording : Supprime l'enregistrement et recharge la liste des enregistrements.

// TODO : 

// Ajouter une icône de suppression pour l'enregistrement.
// Implémenter les vrais textes pour les résumés.
// Ajouter des points de pagination, pour swiper entre la transcription et le résumé. (Voir Enzo pour les détails du style)

// Bugs:

// Si il y a une liste assez longue de transcriptions, certaines transcriptions peuvent ne pas se dérouler. Il faut scroll de nouveau pour faire en sorte que ça refonctionne.
// La font ne s'affiche pas correctement tout le temps.
interface ResumeProps {
    item: string;
    index: number;
    scrollRef: React.RefObject<any>;
}

export default function Resume({ item, index, scrollRef }: ResumeProps) {
    const [itemState, setItemState] = useState(0);

    const heightAnim = useRef(new Animated.Value(40)).current; // Valeur animée pour la hauteur
    const minWidthAnim = useRef(new Animated.Value(0)).current; // Valeur animée pour la largeur

    const { loadRecordings, jsonContent } = usePlayer();

    useEffect(() => {
        const timeoutId = setTimeout(() => {
            scrollRef.current?.scrollToIndex({ animated: true, index });
            return () => clearTimeout(timeoutId);
        }, 100);

        let toHeightValue;
        if (itemState === 0) {
            toHeightValue = 40;
        } else if (itemState === 1) {
            toHeightValue = 250;
        } else {
            const screenHeight = Dimensions.get("window").height;
            toHeightValue = screenHeight * 0.9;
        }

        let toWidthValue;
        const screenWidth = Dimensions.get("window").width;
        if (itemState === 0) {
            toWidthValue = screenWidth * 0.80;
        } else {
            toWidthValue = screenWidth * 0.90;
        }

        Animated.timing(heightAnim, {
            toValue: toHeightValue,
            duration: 200,
            useNativeDriver: false,
        }).start();

        Animated.timing(minWidthAnim, {
            toValue: toWidthValue,
            duration: 200,
            useNativeDriver: false,
        }).start();
    }, [itemState, heightAnim, minWidthAnim]);

    const styles = StyleSheet.create({
        container: {
            display: 'flex',
            justifyContent: 'flex-start',
            padding: 5,
            backgroundColor: useThemeColor({}, "tabIconDefault"),
            marginVertical: 10,
            borderRadius: 10,
            borderColor: useThemeColor({}, 'icon'),
            borderWidth: 1,
        },
        // Suivre le figma pour le style de la page.
        title: {
            fontSize: 19,
            marginLeft: 8,
            fontWeight: 'bold',
            color: useThemeColor({}, 'text'),
            fontFamily: 'Montserrat_700Bold',
        },
        text: {
            fontSize: 16,
            marginLeft: 8,
            color: useThemeColor({}, 'text'),
            fontFamily: 'Montserrat_400Regular',
        },
        jsonContainer: {
            marginTop: 10,
            padding: 10,
            backgroundColor: 'white',
            borderRadius: 5,
        },
    });

    const handlePress = () => {
        itemState < 1 ? setItemState(itemState + 1) : setItemState(0); // a l'origine il etait a inferieur à 2
        console.log("resume.tsx l.118 Pressed on", item, "state : ", itemState);
    };

    const deleteRecording = async (uri: string) => {
        try {
            await FileSystem.deleteAsync(uri);
            loadRecordings(); // Reload recordings after deletion
        } catch (error) {
            console.error("Failed to delete recording", error);
        }
    };

    return (
        <Animated.View style={[styles.container, { height: heightAnim, minWidth: minWidthAnim, maxWidth: minWidthAnim }]}>
            <TouchableOpacity onPress={handlePress}>
                <Text style={styles.title}>RESUME {index + 1}</Text>
            </TouchableOpacity>
            {itemState > 0 &&
                <>
                    <View style={{ height: '85%', width: '100%', marginTop: 10 }}>
                        <ScrollView style={{ width: '100%' }}>
                            <Text style={styles.text}>
                                
                                {jsonContent[index] ? jsonContent[index].Transcription : "Loading..."}
                            </Text>
                        </ScrollView>
                    </View>
                </>
            }
        </Animated.View>
    );
}
// changer le jsonContent[index] ? jsonContent[index].Transcription en item.transcription mais ca ne met pas a jour instant mes record.

// {itemState > 1 &&
//     <>
//         <Player item={item} />
//         {/* <Button title="Delete" onPress={() => deleteRecording(`${FileSystem.documentDirectory}${item}`)} /> */}
//     </>
// }-->

commande pour la limte de mon application ou de mes fichier (pas sur)
fs.inotify.max_user_watches=524288
sudo sysctl -p

modife de build.gradle dans android et dans app

lien vers mon build avce l'extension .aab
il faut le convertir en .apk pour l'installer sur un android ou deployer sur l'appstore
pour generer un .apk localement utiliser "eas build --profile preview --platform android"

POUR REBUILD MON PROJET :
eas build --platform android 
ou
eas build --profile development --platform android (pour utiliser les libraries react native)
adress de mon dernier build : 
https://expo.dev/accounts/fayer/projects/speech_to_text/builds/1041c349-c53c-49af-b5a7-6089f40210f0
✔ Using Keystore from configuration: Build Credentials tq6BLlVVPO (default)

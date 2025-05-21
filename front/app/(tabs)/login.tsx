import React, { useState } from 'react';
import { View, TextInput, Button, StyleSheet, Alert } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../types/_navigation'; // Import du type
import { getToken,saveToken } from '../utils/token_save_get_delete';
// import AsyncStorage from '@react-native-async-storage/async-storage';

// const LoginPage = () => {
//   const [username, setEmail] = useState('');
//   const [password, setPassword] = useState('');
//   // const navigation = useNavigation();

//   type LoginScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Main'>;
//   const navigation = useNavigation<LoginScreenNavigationProp>();
//   // console.log('Navigation object:', navigation);
  
//   const navigateToRegister = () => {
//     navigation.navigate('Register'); // Navigate to the Register page
//   };
//   const navigateToMain = () => {
//     navigation.navigate('Main'); // Navigate to the Register page
//   };

//   const handleLogin = async () => {
//     // Handle login logic here
//     if (username && password) {
//       console.log('Login check', `yur username connection, ${username}!`);
//     } else {
//       console.log('Error', 'Please enter both ID and password.');
//       Alert.alert('Please fill in all fields.');
//       return;
//     }
//     // il faut comenter navigation.navigate('Main'); si je veux tester le fetch et le decommanter pour acceder a mon record description
//     // navigation.navigate('Main');
//     try {
//       // Envoyer les données au backend
//       const response = await fetch('http://vps-692a3a83.vps.ovh.net:5048/api/login', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({
//           username: username,
//           password: password,
//         }),
//       });
  
//       //verification de la reponse en brut 
//       if (!response.ok) {
//         throw new Error(`HTTP error! status: ${response.status}`);
//       }
//       // pour lire la response en brut si j'ai besoin de debugg
//       // const textResponse = await response.text();
//       // console.log('Raw response from server:', textResponse);

//       const data = await response.json(); // Lire directement en JSON
//       console.log('Response from server:', data);
      
//       // stockage du session token en local, en acces dans toute l'appli
//       if (data.Tokken) {
//         await saveToken(data.Tokken);
//         console.log('Token stored successfully');
//       }else {
//         console.log('Token not found in response');
//         throw new Error('Token not found in response, cannot proceed with login');
//       }
//       // pour verifier que le token est bien stocker (a supprimer)
//       const token = await getToken();
//       if (token) {
//         // Utilisez le token ici
//         console.log('Token retrieved:', token);
//       } else {
//         console.warn('Aucun token trouvé.');
//       }
    
//       if (response.ok) {
//         Alert.alert('Login Successful', `Welcome back, ${username}`);
//         navigation.navigate('Main'); // Naviguer vers TabLayout
//       } else {
//         Alert.alert('Login Failed', data.message || 'Invalid credentials');
//       }
//     } catch (error) {
//       console.error('Login error:', error);
//       Alert.alert('Error', 'An error occurred. Please try again.');
//     }
//   };
const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  // const navigation = useNavigation();

  type LoginScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Main'>;
  const navigation = useNavigation<LoginScreenNavigationProp>();
  // console.log('Navigation object:', navigation);
  
  const navigateToRegister = () => {
    navigation.navigate('Register'); // Navigate to the Register page
  };
  const navigateToMain = () => {
    navigation.navigate('Main'); // Navigate to the Register page
  };

  const handleLogin = async () => {
    if (!username || !password) {
      Alert.alert('Erreur', 'Veuillez remplir tous les champs.');
      return;
    }

    try {
      const response = await fetch('http://vps-692a3a83.vps.ovh.net:5048/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          username: username,
          password: password
        }),
      });

      const data = await response.json();
      console.log('Réponse du serveur:', data);

      if (response.ok) {
        if (data.token) {
          await saveToken(data.token);
          console.log('Token stocké avec succès');
          Alert.alert('Connexion réussie', `Bienvenue, ${username}!`);
          navigation.navigate('Main');
        } else {
          Alert.alert('Erreur', 'Token non reçu du serveur');
        }
      } else {
        Alert.alert('Échec de la connexion', data.message || 'Identifiants invalides');
      }
    } catch (error) {
      console.error('Erreur de connexion:', error);
      Alert.alert('Erreur', 'Une erreur est survenue. Veuillez réessayer.');
    }
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Nom d'utilisateur"
        value={username}
        onChangeText={setUsername}
      />
      <TextInput
        style={styles.input}
        placeholder="Mot de passe"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <Button title="Se connecter" onPress={handleLogin} />
      <Button title="Créer un compte" onPress={navigateToRegister} />
      <Button title="Acceder a l'appli" onPress={navigateToMain} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 16,
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 12,
    paddingHorizontal: 8,
  },
});

export default LoginPage;
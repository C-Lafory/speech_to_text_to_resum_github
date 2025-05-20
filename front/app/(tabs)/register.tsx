import React, { useState } from 'react';
import { View, TextInput, Button, StyleSheet, Alert } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../types/_navigation'; // Import du type RootStackParamList
// import AsyncStorage from '@react-native-async-storage/async-storage';

const RegistrationPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  
  type RegisterScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Main'>;
  const navigation = useNavigation<RegisterScreenNavigationProp>();

  // Navigation vers la page de connexion
  const navigateToLogin = () => {
    navigation.navigate('Login'); // Naviguer vers l'écran Login
  };

  // Fonction pour gérer l'enregistrement
  const handleRegistration = async () => {
    if (!username || !email || !password || !confirmPassword) {
      Alert.alert('Erreur', 'Veuillez remplir tous les champs.');
      return;
    }

    if (password !== confirmPassword) {
      Alert.alert('Erreur', 'Les mots de passe ne correspondent pas.');
      return;
    }

    try {
      const response = await fetch('http://vps-692a3a83.vps.ovh.net:5048/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          username: username,
          password: password,
          email: email
        }),
      });

      const data = await response.json();
      console.log('Réponse du serveur:', data);

      if (response.ok) {
        Alert.alert('Inscription réussie', `Bienvenue, ${username}!`);
        navigation.navigate('Login'); // Naviguer vers la page Login
      } else {
        Alert.alert('Échec de l\'inscription', data.message || 'Erreur lors de l\'inscription');
      }
    } catch (error) {
      console.error('Erreur d\'inscription:', error);
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
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
        autoCapitalize="none"
      />
      <TextInput
        style={styles.input}
        placeholder="Mot de passe"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <TextInput
        style={styles.input}
        placeholder="Confirmer le mot de passe"
        value={confirmPassword}
        onChangeText={setConfirmPassword}
        secureTextEntry
      />
      <Button title="Créer un compte" onPress={handleRegistration} />
      <Button title="Se connecter" onPress={navigateToLogin} />
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

export default RegistrationPage;
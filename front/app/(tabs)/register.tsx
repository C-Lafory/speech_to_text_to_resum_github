import React, { useState } from 'react';
import { View, TextInput, Button, StyleSheet, Alert } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../types/_navigation'; // Import du type RootStackParamList
// import AsyncStorage from '@react-native-async-storage/async-storage';

const RegistrationPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [Email, setEmail] = useState('');
  const [ConfirmPassword, setConfirmPassword] = useState('');
  
  type RegisterScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Main'>;
  const navigation = useNavigation<RegisterScreenNavigationProp>();

  // Navigation vers la page de connexion
  const navigateToLogin = () => {
    navigation.navigate('Login'); // Naviguer vers l'écran Login
  };

  // Fonction pour gérer l'enregistrement
  const handleRegistration = async () => {
    if (!username || !Email || !password || !ConfirmPassword) {
      console.log('Error', 'Please fill in all fields.');
      Alert.alert('Please fill in all fields.');
      return;
    }

    if (password !== ConfirmPassword) {
      console.log('Error', 'Passwords do not match.');
      return;
    }

    try {
      const response = await fetch('http://vps-692a3a83.vps.ovh.net:5050/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          Username: username,
          Password: password,
          Email: Email,
          Confirmation: ConfirmPassword,
        }),
      });

      // if (!response.ok) {
      //   throw new Error(`HTTP error! status: ${response.status}`);
      // }
      
      // pour lire la response en brut si j'ai besoin de debugg
      // const textResponse = await response.text();
      // console.log('Raw response from server:', textResponse);

      const data = await response.json();
      console.log('Response from server:', data);

      // if (data.Token) {
      //   await AsyncStorage.setItem('session_token', data.Token);
      //   console.log('Token stored successfully');
      // }

      if (response.ok) {
        Alert.alert('Register Successful', `Welcome, ${username}!`);
        navigation.navigate('Login'); // Naviguer vers la page Login
      } else {
        Alert.alert('Register Failed', data.message || 'Invalid inputs');
      }
    } catch (error) {
      console.error('Register error:', error);
      Alert.alert('Error', 'An error occurred. Please try again.');
    }
  };

  

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Username"
        value={username}
        onChangeText={setUsername}
      />
      <TextInput
        style={styles.input}
        placeholder="Email"
        value={Email}
        onChangeText={setEmail}
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <TextInput
        style={styles.input}
        placeholder="Confirm Password"
        value={ConfirmPassword}
        onChangeText={setConfirmPassword}
        secureTextEntry
      />
      <Button title="Create your new account" onPress={handleRegistration} />
      <Button title="Login" onPress={navigateToLogin} />
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
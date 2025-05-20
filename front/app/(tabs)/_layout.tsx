// TEST PAGE LOGIN ET REGISTER AVEC NAVIGATION

//----------------------------------------------------------------------------------------------------------
import React from 'react';
import { Platform } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { RootStackParamList } from '../types/_navigation'; // Import du type RootStackParamList
import MaterialIcons from '@expo/vector-icons/MaterialIcons';

import useThemeColor from '../hooks/useThemeColor';

// Importez vos écrans
// import HomeScreen from '../screens/HomeScreen';
import description from './description';
import index from './index';
import settings from './settings';
import register from './register';
import login from './login';

// const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();
const Stack = createStackNavigator<RootStackParamList>();

function TabLayout() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: useThemeColor({}, 'tint'),
        tabBarStyle: Platform.select({
          ios: {
            position: 'absolute',
          },
          default: {
            backgroundColor: useThemeColor({}, 'tabIconDefault'),
            position: 'absolute',
            borderRadius: 50,
            borderTopWidth: 0,
            width: '80%',
            marginLeft: '10%',
            marginBottom: 15,
          },
        }),
      }}
    >
      <Tab.Screen
        name="Record"
        component={index}
        options={{
          title: 'Record',
          tabBarIcon: ({ color }) => <MaterialIcons size={28} name="mic" color={color} />,
        }}
      />
      <Tab.Screen
        name="Description"
        component={description}
        options={{
          title: 'Description',
          tabBarIcon: ({ color }) => <MaterialIcons size={28} name="description" color={color} />,
        }}
      />
      
      <Tab.Screen
        name="Settings"
        component={settings}
        options={{
          title: 'Settings',
          tabBarIcon: ({ color }) => <MaterialIcons size={28} name="settings" color={color} />,
        }}
      />
    </Tab.Navigator>
  );
}

export default function App() {
  return (
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        <Stack.Screen name="Login" component={login} />
        <Stack.Screen name="Register" component={register} />
        <Stack.Screen name="Main" component={TabLayout} />
      </Stack.Navigator>
  );
}
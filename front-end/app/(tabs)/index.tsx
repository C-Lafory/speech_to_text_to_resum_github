import { View } from "react-native";
import React from "react";
import Checkfile from "../components/Checkfile/Checkfile";
import Svg, { SvgProps, Path } from "react-native-svg"

import Dropdown from "../components/home/dropdown";
import Recorder from "../components/home/recorder";

import { useThemeColor } from "../hooks/useThemeColor";

// Rendu du composant :

// Affiche la page d'accueil de l'application.
// Affiche un composant Dropdown pour sélectionner la langue de la transcription.
// Affiche un composant Recorder pour enregistrer un message audio.

export default function Record() {
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "flex-start",
        alignItems: "center",
        backgroundColor: useThemeColor({}, "background"),
      }}
    >
      <View style={{ display: "flex", flexDirection: "row", justifyContent: "space-between", alignItems: 'center', position: 'relative', top: 30, width: '100%', height: '10%', padding: 10 }} >
        {/* <SvgComponent /> */}
        <Dropdown />
      </View>
      <View style={{ height: '90%', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <Recorder />
      </View>
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
    </View>
    </View >
  );
}

// Svg pour le titre.

// const SvgComponent = (props: SvgProps) => (
//   <Svg
//     width={166}
//     height={52}
//     fill="none"
//     {...props}
//   >
//     <Path
//       fill="#fff"
//       d="M36.832 40h-5.424v-9.456l-12.624-8.208V40H13.36V12.016L31.408 24.16V12.736h5.424V40Zm18.14.24c-7.584 0-11.425-4.752-11.425-12.288V12.736h5.425v15.216c0 4.992 1.584 7.488 6.047 7.488 4.465 0 6.049-2.496 6.049-7.488V12.736h5.424v15.216c0 7.536-3.84 12.288-11.52 12.288Zm23.671-11.088v5.904H92.18V40H73.22V12.736h18.96v4.944H78.643v6.672h10.848v4.8H78.643Zm37.082-14.64-1.968 4.368c-1.488-.576-4.752-1.488-6.528-1.488-4.272 0-4.368 2.496-4.368 3.072 0 4.992 14.16 3.264 14.16 12.528 0 4.464-5.232 7.248-9.12 7.248-3.792 0-6.96-.48-10.32-2.64l2.064-4.08c1.296.768 3.936 1.92 7.584 1.92 2.256 0 4.416-1.248 4.416-2.832 0-4.512-14.208-2.784-14.208-12.384 0-4.896 3.456-7.824 9.648-7.824 3.264 0 7.056 1.392 8.64 2.112ZM122.391 40V12.736h5.424V40h-5.424ZM152.1 14.512l-1.968 4.368c-1.488-.576-4.752-1.488-6.528-1.488-4.272 0-4.368 2.496-4.368 3.072 0 4.992 14.16 3.264 14.16 12.528 0 4.464-5.232 7.248-9.12 7.248-3.792 0-6.96-.48-10.32-2.64l2.064-4.08c1.296.768 3.936 1.92 7.584 1.92 2.256 0 4.416-1.248 4.416-2.832 0-4.512-14.208-2.784-14.208-12.384 0-4.896 3.456-7.824 9.648-7.824 3.264 0 7.056 1.392 8.64 2.112Z"
//     />
//   </Svg>
// )
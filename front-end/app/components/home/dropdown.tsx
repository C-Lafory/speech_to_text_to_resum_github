import { View, Text, StyleSheet } from "react-native";
import SelectDropdown from "react-native-select-dropdown";

import { useThemeColor } from "@/app/hooks/useThemeColor";

import MaterialIcons from "@expo/vector-icons/MaterialIcons";


export default function Dropdown() {

    const items = [
        { title: 'Fr', icon: 'option1' },
        { title: 'Eng', icon: 'option2' },
    ];

    const styles = StyleSheet.create({
        dropdownButtonStyle: {
            minWidth: 120,
            maxWidth: 150,
            height: 40,

            backgroundColor: useThemeColor({}, "tabIconDefault"),

            borderRadius: 10,
            borderWidth: 1,
            borderColor: useThemeColor({}, "icon"),

            flexDirection: 'row',
            justifyContent: 'space-between',
            alignItems: 'center',

            paddingHorizontal: 12,
        },
        dropdownButtonTxtStyle: {
            flex: 1,
            fontSize: 15,
            marginLeft: 8,
            color: useThemeColor({}, "text"),
        },
        dropdownButtonIconStyle: {
            fontSize: 28,
            marginRight: 8,
        },
        dropdownMenuStyle: {
            marginTop: -30,
            backgroundColor: useThemeColor({}, "tabIconDefault"),
            borderRadius: 8,
        },
        dropdownItemStyle: {
            width: '100%',
            flexDirection: 'row',
            paddingHorizontal: 12,
            justifyContent: 'center',
            alignItems: 'center',
            paddingVertical: 8,
        },
        dropdownItemTxtStyle: {
            flex: 1,
            fontSize: 18,
            fontWeight: '500',
            color: useThemeColor({}, "text"),
        },
        dropdownItemIconStyle: {
            fontSize: 28,
            marginRight: 8,
        },
    });

    return (
        <SelectDropdown
            data={items}
            onSelect={(selectedItem, index) => {
                console.log(selectedItem, index);
            }}
            renderButton={(selectedItem, isOpened) => {
                return (
                    <View style={styles.dropdownButtonStyle}>
                        <MaterialIcons size={18} name={'translate'} color={useThemeColor({}, 'text')} />
                        {selectedItem && (
                            <Text style={styles.dropdownButtonTxtStyle}>{selectedItem.title}</Text>
                        )}
                        <MaterialIcons size={18} name={isOpened ? 'keyboard-arrow-up' : 'keyboard-arrow-down'} color={useThemeColor({}, 'text')} />
                    </View>
                );
            }}
            renderItem={(item, index, isSelected) => {
                return (
                    <View style={{ ...styles.dropdownItemStyle }}>
                        <Text style={styles.dropdownItemTxtStyle}>{item.title}</Text>
                    </View>
                );
            }}
            showsVerticalScrollIndicator={false}
            dropdownStyle={styles.dropdownMenuStyle}
        />
    );
}
import * as FileSystem from 'expo-file-system';

export const deleteAllFiles = async () => {
    try {
        if (!FileSystem.documentDirectory) {
            console.error("FileSystem.documentDirectory is null");
            return;
        }

        const directory = `${FileSystem.documentDirectory}recordings/`;

        // Vérifiez si le répertoire existe
        const dirInfo = await FileSystem.getInfoAsync(directory);
        if (!dirInfo.exists) {
            console.error("Directory does not exist:", directory);
            return;
        }

        const files = await FileSystem.readDirectoryAsync(directory);

        await Promise.all(files.map(async (file) => {
            const fileUri = `${directory}${file}`;
            await FileSystem.deleteAsync(fileUri);
            console.log('Deleted file:', fileUri);
        }));

        console.log('All files deleted');
    } catch (error) {
        console.error('Error deleting files:', error);
    }
};


export const fetchRecordings = async (filterExtension: string | null = null) => {
    const directory = `${FileSystem.documentDirectory}recordings/`;
    const dirInfo = await FileSystem.getInfoAsync(directory);

    if (!dirInfo.exists) {
        console.log("Directory does not exist:", directory);
        return [];
    }

    const files = await FileSystem.readDirectoryAsync(directory);
    if (filterExtension) {
        return files.filter(file => file.endsWith(filterExtension));
    }
    return files;
};

//ancienne fonction

//   const deleteAllFiles = async () => {
//     try {
//       if (!FileSystem.documentDirectory) {
//         console.error("FileSystem.documentDirectory is null");
//         return;
//       }

//       const files = await FileSystem.readDirectoryAsync(FileSystem.documentDirectory);

//       await Promise.all(files.map(async (file) => {
//         const fileUri = `${FileSystem.documentDirectory}${file}`;
//         await FileSystem.deleteAsync(fileUri);
//         console.log('Deleted file:', fileUri);
//       }));

//       setJsonContents([]);

//       loadRecordings();
//       console.log('description.tsx l84 All files deleted');
//     } catch (error) {
//       console.error('Error deleting files:', error);
//     }
//   };
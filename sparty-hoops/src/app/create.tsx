import {
  StyleSheet,
  Text,
  View,
  TextInput,
  Pressable,
} from 'react-native';

export default function CreateScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Create a Run</Text>

      <Text style={styles.subtitle}>
        Start a new pickup run at the SRWC.
      </Text>

      <Text style={styles.label}>Time</Text>

      <TextInput
        style={styles.input}
        placeholder="Example: 8:00 PM"
      />

      <Text style={styles.label}>Skill Level</Text>

      <TextInput
        style={styles.input}
        placeholder="Example: Intermediate"
      />

      <Text style={styles.label}>Max Players</Text>

      <TextInput
        style={styles.input}
        placeholder="Example: 10"
        keyboardType="numeric"
      />

      <Pressable style={styles.button}>
        <Text style={styles.buttonText}>CREATE RUN</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },

  title: {
    fontSize: 32,
    fontWeight: 'bold',
    marginTop: 50,
  },

  subtitle: {
    fontSize: 16,
    marginTop: 5,
    marginBottom: 30,
  },

  label: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 8,
    marginTop: 15,
  },

  input: {
    borderWidth: 1,
    borderColor: '#cccccc',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
  },

  button: {
    backgroundColor: '#18453B',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 30,
  },

  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
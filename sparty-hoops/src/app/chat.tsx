import {
  StyleSheet,
  Text,
  View,
  TextInput,
  Pressable,
  ScrollView,
} from 'react-native';

export default function ChatScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Chat</Text>

      <Text style={styles.subtitle}>
        Talk with other Sparty Hoopers.
      </Text>

      <ScrollView style={styles.messages}>
        <View style={styles.message}>
          <Text style={styles.username}>Kam</Text>
          <Text style={styles.messageText}>
            Anyone hooping at 8 tn?
          </Text>
        </View>

        <View style={styles.message}>
          <Text style={styles.username}>Marquis</Text>
          <Text style={styles.messageText}>
            yeah i'm sliding
          </Text>
        </View>

        <View style={styles.message}>
          <Text style={styles.username}>Cody</Text>
          <Text style={styles.messageText}>
            I'll be there around 8:30
          </Text>
        </View>
      </ScrollView>

      <View style={styles.inputRow}>
        <TextInput
          style={styles.input}
          placeholder="Type a message..."
        />

        <Pressable style={styles.sendButton}>
          <Text style={styles.sendText}>Send</Text>
        </Pressable>
      </View>
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
    marginBottom: 20,
  },

  messages: {
    flex: 1,
  },

  message: {
    backgroundColor: '#f0f0f0',
    padding: 12,
    borderRadius: 10,
    marginBottom: 10,
  },

  username: {
    fontWeight: 'bold',
    marginBottom: 4,
  },

  messageText: {
    fontSize: 16,
  },

  inputRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 90,
  },

  input: {
    flex: 1,
    borderWidth: 1,
    borderColor: '#cccccc',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
  },

  sendButton: {
    backgroundColor: '#18453B',
    padding: 12,
    borderRadius: 8,
    marginLeft: 8,
  },

  sendText: {
    color: 'white',
    fontWeight: 'bold',
  },
});
import {
  StyleSheet,
  Text,
  View,
  Pressable,
} from 'react-native';

export default function ProfileScreen() {
  return (
    <View style={styles.container}>
      <View style={styles.profilePicture}>
        <Text style={styles.profilePictureText}>🏀</Text>
      </View>

      <Text style={styles.username}>Marquis</Text>

      <Text style={styles.skill}>Competitive</Text>

      <View style={styles.infoSection}>
        <Text style={styles.label}>Height</Text>
        <Text style={styles.value}>6'0"</Text>

        <Text style={styles.label}>Position</Text>
        <Text style={styles.value}>Guard</Text>

        <Text style={styles.label}>Play Style</Text>
        <Text style={styles.value}>3 and D</Text>
      </View>

      <View style={styles.socialSection}>
        <Text style={styles.label}>Instagram</Text>
        <Text style={styles.value}>@marquisburton_</Text>

        <Text style={styles.label}>Snapchat</Text>
        <Text style={styles.value}>kingquis2007</Text>
      </View>

      <Pressable style={styles.button}>
        <Text style={styles.buttonText}>EDIT PROFILE</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    alignItems: 'center',
  },

  profilePicture: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#e5e5e5',
    justifyContent: 'center',
    alignItems: 'center',
    marginTop: 50,
  },

  profilePictureText: {
    fontSize: 40,
  },

  username: {
    fontSize: 26,
    fontWeight: 'bold',
    marginTop: 15,
  },

  skill: {
    fontSize: 16,
    marginTop: 5,
  },

  infoSection: {
    width: '100%',
    marginTop: 30,
  },

  socialSection: {
    width: '100%',
    marginTop: 20,
  },

  label: {
    fontSize: 14,
    fontWeight: 'bold',
    marginTop: 10,
  },

  value: {
    fontSize: 17,
    marginTop: 3,
  },

  button: {
    backgroundColor: '#18453B',
    padding: 15,
    borderRadius: 8,
    width: '100%',
    alignItems: 'center',
    marginTop: 30,
  },

  buttonText: {
    color: 'white',
    fontWeight: 'bold',
  },
});
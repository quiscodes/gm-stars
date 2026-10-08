import { StyleSheet, Text, View, Pressable } from 'react-native';

type RunCardProps = {
  time: string;
  skill: string;
  players: number;
  maxPlayers: number;
};

export default function RunCard({
  time,
  skill,
  players,
  maxPlayers,
}: RunCardProps) {
  return (
    <View style={styles.card}>
      <Text style={styles.location}>SRWC</Text>

      <Text style={styles.time}>{time}</Text>

      <Text style={styles.skill}>{skill}</Text>

      <Text style={styles.players}>
        {players} / {maxPlayers} players
      </Text>

      <Pressable style={styles.button}>
        <Text style={styles.buttonText}>JOIN RUN</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 20,
    marginBottom: 15,
  },

  location: {
    fontSize: 20,
    fontWeight: 'bold',
  },

  time: {
    fontSize: 18,
    marginTop: 5,
  },

  skill: {
    fontSize: 16,
    marginTop: 5,
  },

  players: {
    fontSize: 16,
    marginTop: 10,
  },

  button: {
  marginTop: 15,
  padding: 12,
  borderRadius: 8,
  alignItems: 'center',
  backgroundColor: '#18453B',
  },

  buttonText: {
  color: 'white',
  fontWeight: 'bold',
  },


});
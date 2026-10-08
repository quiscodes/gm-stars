import { StyleSheet, Text, View } from 'react-native';
import RunCard from './components/RunCard';

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>🏀 Sparty Hoops</Text>

      <Text style={styles.subtitle}>
        Welcome back, Marquis!
      </Text>

      <Text style={styles.sectionTitle}>
        🔥 ACTIVE RUNS
      </Text>

      <RunCard
        time="3:00 PM"
        skill="Competitive"
        players={6}
        maxPlayers={10}
      />

      <RunCard
        time="5:00 PM"
        skill="Intermediate"
        players={3}
        maxPlayers={10}
      />

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1, // take up whats available on screen
    justifyContent: 'center', // vertical centering
    alignItems: 'center', // horizontal centering
    padding: 20, // space from the sides
  },

  title: {
    fontSize: 32,
    fontWeight: 'bold',
  },

  subtitle: {
    marginTop: 10, // space between sparty hoops and find your next run
    fontSize: 16, 
  },

  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 20,
    marginBottom: 20,
  },
  
});
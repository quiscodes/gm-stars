import {
  StyleSheet,
  Text,
  View,
  ScrollView,
} from 'react-native';

import RunCard from './components/RunCard';

const runs = [
  {
    time: '3:00 PM',
    skill: 'Competitive',
    players: 6,
    maxPlayers: 10,
  },
  {
    time: '5:00 PM',
    skill: 'Intermediate',
    players: 3,
    maxPlayers: 10,
  },
  {
    time: '6:30 PM',
    skill: 'Any Skill',
    players: 8,
    maxPlayers: 10,
  },
];

export default function FindScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Find Runs</Text>

      <Text style={styles.subtitle}>
        Live pickup basketball at the SRWC
      </Text>

      <ScrollView style={styles.runList}>
        {runs.map((run) => (
          <RunCard
            key={run.time}
            time={run.time}
            skill={run.skill}
            players={run.players}
            maxPlayers={run.maxPlayers}
          />
        ))}
      </ScrollView>
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

  runList: {
    flex: 1,
  },
});
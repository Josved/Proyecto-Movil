import { View, Text, TouchableOpacity, StyleSheet } from "react-native";

export default function CajaHomeScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <Text style={styles.titulo}>Módulo de Caja</Text>

      <TouchableOpacity
        style={styles.boton}
        onPress={() => navigation.navigate("PedidosPendientes")}
      >
        <Text style={styles.textoBoton}>Pedidos Pendientes</Text>
      </TouchableOpacity>

      <TouchableOpacity
        style={styles.boton}
        onPress={() => navigation.navigate("Ventas")}
      >
        <Text style={styles.textoBoton}>Ventas</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
  },

  titulo: {
    fontSize: 28,
    fontWeight: "bold",
    marginBottom: 40,
  },

  boton: {
    width: "80%",
    backgroundColor: "#1976D2",
    padding: 15,
    borderRadius: 10,
    marginBottom: 20,
    alignItems: "center",
  },

  textoBoton: {
    color: "white",
    fontSize: 18,
    fontWeight: "bold",
  },
});
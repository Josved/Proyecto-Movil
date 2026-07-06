import { View, Text, TouchableOpacity, StyleSheet } from "react-native";

export default function DetallePedidoScreen({ route, navigation }) {
  const { pedido } = route.params;

  return (
    <View style={styles.container}>
      <Text style={styles.titulo}>Detalle del Pedido</Text>

      <View style={styles.card}>
        <Text style={styles.texto}>Pedido #{pedido.id}</Text>
        <Text>Mesa: {pedido.mesa_id}</Text>
        <Text>Mesero: {pedido.mesero_id}</Text>
        <Text>Estado: {pedido.estado}</Text>
        <Text>Fecha: {pedido.fecha}</Text>
      </View>

      <TouchableOpacity
        style={styles.boton}
        onPress={() =>
          navigation.navigate("RegistrarPago", {
            pedido,
          })
        }
      >
        <Text style={styles.textoBoton}>Registrar Pago</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },

  titulo: {
    fontSize: 28,
    fontWeight: "bold",
    marginBottom: 20,
  },

  card: {
    backgroundColor: "#f2f2f2",
    padding: 20,
    borderRadius: 10,
    marginBottom: 30,
  },

  texto: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 10,
  },

  boton: {
    backgroundColor: "#2E7D32",
    padding: 15,
    borderRadius: 10,
    alignItems: "center",
  },

  textoBoton: {
    color: "white",
    fontWeight: "bold",
    fontSize: 18,
  },
});
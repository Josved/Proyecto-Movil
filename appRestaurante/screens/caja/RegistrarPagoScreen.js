import { View, Text, TouchableOpacity, StyleSheet, Alert } from "react-native";
import { useState } from "react";
import api from "../../services/api";

export default function RegistrarPagoScreen({ route, navigation }) {
  const { pedido } = route.params;

  const [metodoPago, setMetodoPago] = useState("Efectivo");

  const registrarPago = async () => {
    try {
      await api.post("/pagos/", {
        pedido_id: pedido.id,
        metodo_pago: metodoPago,
        total: 0
      });

      Alert.alert("Éxito", "Pago registrado correctamente");

      navigation.navigate("Ventas");
    } catch (error) {
      console.log(error);
      Alert.alert("Error", "No se pudo registrar el pago");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.titulo}>Registrar Pago</Text>

      <View style={styles.card}>
        <Text>Pedido: #{pedido.id}</Text>
        <Text>Mesa: {pedido.mesa_id}</Text>
        <Text>Método: {metodoPago}</Text>
      </View>

      <TouchableOpacity
        style={styles.boton}
        onPress={registrarPago}
      >
        <Text style={styles.textoBoton}>Confirmar Pago</Text>
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

  boton: {
    backgroundColor: "#1976D2",
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
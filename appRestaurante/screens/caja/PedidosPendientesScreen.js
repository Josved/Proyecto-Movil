import { View, Text, FlatList, TouchableOpacity, StyleSheet } from "react-native";
import { useEffect, useState } from "react";
import api from "../../services/api";

export default function PedidosPendientesScreen({ navigation }) {
  const [pedidos, setPedidos] = useState([]);

  useEffect(() => {
    cargarPedidos();
  }, []);

  const cargarPedidos = async () => {
    try {
      const response = await api.get("/pedidos/");

      console.log("RESPUESTA:", response.data);
      console.log("ES ARRAY:", Array.isArray(response.data));

      setPedidos(response.data);

    } catch (error) {
      console.log("ERROR AXIOS:", error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.titulo}>Pedidos Pendientes</Text>

      <FlatList
        data={pedidos}
        keyExtractor={(item) => item.id.toString()}
        ListEmptyComponent={
          <Text style={styles.vacio}>No hay pedidos pendientes.</Text>
        }
        renderItem={({ item }) => (
          <TouchableOpacity
            style={styles.card}
            onPress={() =>
              navigation.navigate("DetallePedido", {
                pedido: item,
              })
            }
          >
            <Text style={styles.texto}>Pedido #{item.id}</Text>
            <Text>Mesa: {item.mesa_id}</Text>
            <Text>Mesero: {item.mesero_id}</Text>
            <Text>Estado: {item.estado}</Text>
            <Text>Fecha: {item.fecha}</Text>
          </TouchableOpacity>
        )}
      />
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
    padding: 15,
    borderRadius: 10,
    marginBottom: 15,
    borderRadius: 10,
  },

  texto: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 5,
  },

  vacio: {
    textAlign: "center",
    marginTop: 30,
    fontSize: 18,
    color: "gray",
  },
});
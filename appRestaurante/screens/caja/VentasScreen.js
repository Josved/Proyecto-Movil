import { View, Text, FlatList, StyleSheet } from "react-native";
import { useEffect, useState } from "react";
import api from "../../services/api";

export default function VentasScreen() {
  const [ventas, setVentas] = useState([]);

  useEffect(() => {
    cargarVentas();
  }, []);

  const cargarVentas = async () => {
    try {
      const response = await api.get("/ventas/");
      setVentas(response.data);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.titulo}>Ventas</Text>

      <FlatList
        data={ventas}
        keyExtractor={(item) => item.id.toString()}
        ListEmptyComponent={
          <Text style={styles.vacio}>No hay ventas registradas.</Text>
        }
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.texto}>Venta #{item.id}</Text>
            <Text>Pago ID: {item.pago_id}</Text>
            <Text>Folio: {item.folio}</Text>
            <Text>Fecha: {item.fecha}</Text>
          </View>
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
  },

  texto: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 5,
  },

  vacio: {
    textAlign: "center",
    marginTop: 30,
    color: "gray",
    fontSize: 18,
  },
});
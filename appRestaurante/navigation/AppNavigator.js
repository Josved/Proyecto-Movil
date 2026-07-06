import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

import CajaHomeScreen from "../screens/caja/CajaHomeScreen";
import PedidosPendientesScreen from "../screens/caja/PedidosPendientesScreen";
import DetallePedidoScreen from "../screens/caja/DetallePedidoScreen";
import RegistrarPagoScreen from "../screens/caja/RegistrarPagoScreen";
import VentasScreen from "../screens/caja/VentasScreen";

const Stack = createNativeStackNavigator();

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Caja">
        <Stack.Screen
          name="Caja"
          component={CajaHomeScreen}
          options={{ title: "Caja" }}
        />

        <Stack.Screen
          name="PedidosPendientes"
          component={PedidosPendientesScreen}
          options={{ title: "Pedidos Pendientes" }}
        />

        <Stack.Screen
          name="DetallePedido"
          component={DetallePedidoScreen}
          options={{ title: "Detalle del Pedido" }}
        />

        <Stack.Screen
          name="RegistrarPago"
          component={RegistrarPagoScreen}
          options={{ title: "Registrar Pago" }}
        />

        <Stack.Screen
          name="Ventas"
          component={VentasScreen}
          options={{ title: "Ventas" }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
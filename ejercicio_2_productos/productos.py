import json


class StockInvalidoError(Exception):
    pass


class DispositivoEcológico:
    def __init__(self, nombre, precio, stock) -> None:
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    @property
    def stock(self):
        return self.__stock

    @stock.setter
    def stock(self, valor):
        if valor < 0:
            raise StockInvalidoError("El stock no puede ser negativo.")
        self.__stock = valor

    def generar_ficha_tecnica(self):
        return f"FICHA COMERCIAL BÁSICA:\nNombre: {self.nombre}\nPrecio: {self.precio}\nStock: {self.stock}"


class PanelSolar(DispositivoEcológico):
    def __init__(self, nombre, precio, stock, eficiencia, potencia_w) -> None:
        super().__init__(nombre, precio, stock)
        self.eficiencia = eficiencia
        self.potencia_w = potencia_w

    def generar_ficha_tecnica(self):
        return f"FICHA COMERCIAL SOLAR:\nNombre: {self.nombre}\nPrecio: {self.precio}\nStock: {self.stock}\nPotencia: {self.potencia_w}\nEficiencia: {self.eficiencia}"


class GestorInventario:
    @staticmethod
    def guardar_catalogo_json(lista_dispositivos, ruta_archivo):
        datos_serializar = []
        for dispositivo in lista_dispositivos:
            datos_dispositivo = {
                "nombre": dispositivo.nombre,
                "precio": dispositivo.precio,
                "stock": dispositivo.stock
            }

            if isinstance(dispositivo, PanelSolar):
                datos_dispositivo["eficiencia"] = dispositivo.eficiencia
                datos_dispositivo["potencia_w"] = dispositivo.potencia_w

            datos_serializar.append(datos_dispositivo)

        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos_serializar, archivo, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    inventario_prueba = []

    print("--- Cargando catálogo ---")
    try:
        d = DispositivoEcológico("Lámpara LED", 1500, 10)
        inventario_prueba.append(d)
        p = PanelSolar("Panel X", 1000, 5, "18%", 300)
        inventario_prueba.append(p)
        print("Productos válidos creados.")
    except StockInvalidoError as e:
        print(f"Error inesperado: {e}")

    try:
        print("Intentando crear panel con stock erróneo (-1)...")
        panel_malo = PanelSolar("Panel Malo", 500, -1, "15%", 200)
        inventario_prueba.append(panel_malo)
    except StockInvalidoError as e:
        print(f"Captura controlada exitosa: {e}")

    print("\n--- Mostrando catálogo ---")
    for dispositivo in inventario_prueba:
        print(dispositivo.generar_ficha_tecnica())
        print("---")

    GestorInventario.guardar_catalogo_json(inventario_prueba, "catalogo_ecotech.json")
    print("Catálogo exportado a 'catalogo_ecotech.json'.")
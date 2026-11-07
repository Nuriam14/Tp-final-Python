import json


# 1. Excepción personalizada
class StockInvalidoError(Exception):
    """Excepción lanzada cuando el stock es negativo o inválido."""
    pass


# 2. Clase Base
class DispositivoEcológico:
    def __init__(self, nombre, precio, stock=0):
        self.nombre = nombre
        self.precio = float(precio)
        self._stock = 0
        self.stock = stock  # Llama al setter para validar

    # Encapsulamiento del stock
    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        if not isinstance(valor, int):
            raise StockInvalidoError("El stock debe ser un número entero.")
        if valor < 0:
            raise StockInvalidoError("El stock no puede ser negativo.")
        self._stock = valor

    # Método que se va a sobrescribir (Polimorfismo)
    def ficha_tecnica(self):
        return (
            f"Dispositivo ecológico: {self.nombre} | "
            f"Precio: ${self.precio:.2f} | Stock: {self.stock}"
        )

    def to_dict(self):
        return {
            "tipo": self.__class__.__name__,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
        }


# 3. Clase Especializada (Herencia)
class PanelSolar(DispositivoEcológico):
    def __init__(self, nombre, precio, stock, potencia_w, eficiencia):
        super().__init__(nombre, precio, stock)
        self.potencia_w = float(potencia_w)
        self.eficiencia = float(eficiencia)

    # Polimorfismo: cambiamos el mensaje de la ficha técnica
    def ficha_tecnica(self):
        return (
            f"Panel Solar: {self.nombre} | "
            f"Potencia: {self.potencia_w:.0f} W | "
            f"Eficiencia: {self.eficiencia:.1f}% | "
            f"Precio: ${self.precio:.2f} | Stock: {self.stock}"
        )

    def to_dict(self):
        datos = super().to_dict()
        datos.update({
            "potencia_w": self.potencia_w,
            "eficiencia": self.eficiencia,
        })
        return datos


# 4. Gestor de Inventario (Persistencia)
class GestorInventario:
    @staticmethod
    def guardar_catalogo_json(lista_dispositivos, ruta_archivo="catalogo_ecotech.json"):
        datos = [dispositivo.to_dict() for dispositivo in lista_dispositivos]

        with open(ruta_archivo, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, ensure_ascii=False, indent=4)

        return ruta_archivo


# 5. Bloque de ejecución y prueba
if __name__ == "__main__":
    catalogo = []

    print("--- PRUEBA DE EXCEPCIÓN ---")
    try:
        # Intentamos crear un panel con stock negativo (debe fallar)
        panel_erroneo = PanelSolar(
            nombre="Panel inválido",
            precio=100.0,
            stock=-3,
            potencia_w=300,
            eficiencia=18.0
        )
        catalogo.append(panel_erroneo)
    except StockInvalidoError as error:
        print(f"✅ StockInvalidoError capturado correctamente: {error}")

    print("\n--- CREANDO PRODUCTOS VÁLIDOS ---")
    # Productos válidos
    panel1 = PanelSolar("Panel Solar 300W", 250.0, 10, 300, 18.5)
    panel2 = PanelSolar("Panel Solar 450W", 390.0, 5, 450, 21.0)

    catalogo.extend([panel1, panel2])

    print("\n=== FICHAS TÉCNICAS ===")
    for dispositivo in catalogo:
        print("-", dispositivo.ficha_tecnica())

    print("\n--- GUARDANDO EN JSON ---")
    ruta = GestorInventario.guardar_catalogo_json(
        catalogo,
        "catalogo_ecotech.json"
    )

    print(f"✅ Catálogo exportado correctamente a: {ruta}")
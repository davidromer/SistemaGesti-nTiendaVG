# =============================================================================
# PROYECTO FINAL - MÓDULO 3: SISTEMA DE GESTIÓN DE TIENDA DE VIDEOJUEGOS
# =============================================================================
# Autor     : David Romero          
# Fecha     : 18 de mayo de 2026
# Versión   : 1.0
# =============================================================================

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE LA TIENDA
# Cambia estos valores para personalizar el sistema a tu tienda
# -----------------------------------------------------------------------------
NOMBRE_TIENDA = "GameZone Store"    
MONEDA = "$"                        # Símbolo de moneda
LIMITE_STOCK_BAJO = 3               # Umbral para alertas de stock bajo
LIMITE_DESCUENTO = 500_000          # Compras mayores a este valor tienen descuento
PORCENTAJE_DESCUENTO = 0.10         # 10% de descuento

# -----------------------------------------------------------------------------
# DATOS DE PRUEBA INICIALES
# Agrega aquí los videojuegos reales de tu tienda o modifica los existentes
# -----------------------------------------------------------------------------
videojuegos_iniciales = {
    "VG001": {
        "nombre": "God of War: Ragnarok",
        "plataforma": "PlayStation 5",
        "precio": 250000,
        "cantidad": 10
    },
    "VG002": {
        "nombre": "MARIO KART 8 DELUXE",
        "plataforma": "Nintendo Switch",
        "precio": 220000,
        "cantidad": 5
    },
    "VG003": {
        "nombre": "EA SPORTS FIFA 26",
        "plataforma": "Xbox Series X",
        "precio": 210000,
        "cantidad": 8
    }
}

# Historial de ventas (reto adicional)
historial_ventas = []


# -----------------------------------------------------------------------------
# FUNCIONES AUXILIARES
# -----------------------------------------------------------------------------

def leer_entero(mensaje: str, minimo: int = None) -> int:
    """Solicita un número entero al usuario con validación."""
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"  El valor debe ser mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("  Ingrese un número entero válido.")


def leer_flotante(mensaje: str, minimo: float = None) -> float:
    """Solicita un número flotante al usuario con validación."""
    while True:
        try:
            valor = float(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"  El valor debe ser mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("  Ingrese un número válido.")


def alerta_stock_bajo(videojuegos: dict) -> None:
    """Muestra alertas para videojuegos con cantidad menor al límite configurado."""
    bajos = [
        (codigo, datos)
        for codigo, datos in videojuegos.items()
        if datos["cantidad"] < LIMITE_STOCK_BAJO
    ]
    if bajos:
        print(f"\n  *** ALERTA: Videojuegos con stock bajo (< {LIMITE_STOCK_BAJO} unidades) ***")
        for codigo, datos in bajos:
            print(f"  - [{codigo}] {datos['nombre']} — {datos['cantidad']} unidad(es)")


# -----------------------------------------------------------------------------
# FUNCIÓN 1: AGREGAR VIDEOJUEGO
# -----------------------------------------------------------------------------

def agregar_videojuego(videojuegos: dict) -> None:
    """Solicita datos al usuario y agrega un nuevo videojuego al inventario."""
    print("\n--- AGREGAR VIDEOJUEGO ---")

    codigo = input("Código del videojuego: ").strip().upper()
    if not codigo:
        print("  El código no puede estar vacío.")
        return
    if codigo in videojuegos:
        print(f"  Ya existe un videojuego con el código '{codigo}'.")
        return

    nombre = input("Nombre del juego: ").strip()
    if not nombre:
        print("  El nombre no puede estar vacío.")
        return

    plataforma = input("Plataforma: ").strip()
    if not plataforma:
        print("  La plataforma no puede estar vacía.")
        return

    precio = leer_flotante("Precio (pesos): $", minimo=0.01)
    cantidad = leer_entero("Cantidad inicial: ", minimo=0)

    videojuegos[codigo] = {
        "nombre": nombre,
        "plataforma": plataforma,
        "precio": precio,
        "cantidad": cantidad
    }
    print(f"\n  Videojuego '{nombre}' agregado exitosamente con código {codigo}.")


# -----------------------------------------------------------------------------
# FUNCIÓN 2: MOSTRAR INVENTARIO
# -----------------------------------------------------------------------------

def mostrar_inventario(videojuegos: dict) -> None:
    """Muestra todos los videojuegos registrados en formato tabular."""
    print("\n--- INVENTARIO DE VIDEOJUEGOS ---")
    if not videojuegos:
        print("  El inventario está vacío.")
        return

    encabezado = f"{'Código':<8} {'Nombre':<35} {'Plataforma':<22} {'Precio':>12} {'Stock':>6}"
    print(encabezado)
    print("-" * len(encabezado))

    for codigo, datos in videojuegos.items():
        print(
            f"{codigo:<8} {datos['nombre']:<35} {datos['plataforma']:<22} "
            f"${datos['precio']:>11,.0f} {datos['cantidad']:>6}"
        )

    alerta_stock_bajo(videojuegos)


# -----------------------------------------------------------------------------
# FUNCIÓN 3: BUSCAR VIDEOJUEGO POR CÓDIGO
# -----------------------------------------------------------------------------

def buscar_videojuego(videojuegos: dict) -> None:
    """Busca y muestra la información completa de un videojuego por código."""
    print("\n--- BUSCAR VIDEOJUEGO ---")
    codigo = input("Ingrese el código del videojuego: ").strip().upper()

    if codigo not in videojuegos:
        print(f"  No se encontró ningún videojuego con el código '{codigo}'.")
        return

    datos = videojuegos[codigo]
    print(f"\n  Código     : {codigo}")
    print(f"  Nombre     : {datos['nombre']}")
    print(f"  Plataforma : {datos['plataforma']}")
    print(f"  Precio     : ${datos['precio']:,.0f}")
    print(f"  Stock      : {datos['cantidad']} unidades")


# -----------------------------------------------------------------------------
# FUNCIÓN 4: ACTUALIZAR PRECIO
# -----------------------------------------------------------------------------

def actualizar_precio(videojuegos: dict) -> None:
    """Permite modificar el precio de un videojuego existente."""
    print("\n--- ACTUALIZAR PRECIO ---")
    codigo = input("Código del videojuego: ").strip().upper()

    if codigo not in videojuegos:
        print(f"  No existe un videojuego con el código '{codigo}'.")
        return

    datos = videojuegos[codigo]
    print(f"  Juego: {datos['nombre']} — Precio actual: ${datos['precio']:,.0f}")

    nuevo_precio = leer_flotante("Nuevo precio: $", minimo=0.01)
    datos["precio"] = nuevo_precio
    print(f"  Precio actualizado a ${nuevo_precio:,.0f} correctamente.")


# -----------------------------------------------------------------------------
# FUNCIÓN 5: REGISTRAR VENTA
# -----------------------------------------------------------------------------

def registrar_venta(videojuegos: dict) -> None:
    """Procesa una venta, actualiza el inventario y muestra la factura."""
    print("\n--- REGISTRAR VENTA ---")
    codigo = input("Código del videojuego: ").strip().upper()

    if codigo not in videojuegos:
        print(f"  No existe un videojuego con el código '{codigo}'.")
        return

    datos = videojuegos[codigo]
    print(f"  Juego: {datos['nombre']} — Stock disponible: {datos['cantidad']}")

    if datos["cantidad"] == 0:
        print("  Sin stock disponible para este videojuego.")
        return

    cantidad = leer_entero("Cantidad a vender: ", minimo=1)

    if cantidad > datos["cantidad"]:
        print(f"  Stock insuficiente. Solo hay {datos['cantidad']} unidades disponibles.")
        return

    subtotal = datos["precio"] * cantidad
    descuento = 0.0
    if subtotal > LIMITE_DESCUENTO:
        descuento = subtotal * PORCENTAJE_DESCUENTO
        print(f"  Descuento del {int(PORCENTAJE_DESCUENTO*100)}% aplicado por compra mayor a {MONEDA}{LIMITE_DESCUENTO:,.0f}.")

    total = subtotal - descuento

    # Actualizar inventario
    datos["cantidad"] -= cantidad

    # Guardar en historial
    historial_ventas.append({
        "codigo": codigo,
        "nombre": datos["nombre"],
        "cantidad": cantidad,
        "precio_unitario": datos["precio"],
        "total": total
    })

    # Factura
    separador = "=" * 38
    print(f"\n{separador}")
    print("          FACTURA DE VENTA")
    print(separador)
    print(f"  Juego          : {datos['nombre']}")
    print(f"  Plataforma     : {datos['plataforma']}")
    print(f"  Precio unitario: ${datos['precio']:>10,.0f}")
    print(f"  Cantidad       : {cantidad}")
    if descuento > 0:
        print(f"  Descuento (10%): ${descuento:>10,.0f}")
    print(f"  {'TOTAL':<15}  : ${total:>10,.0f}")
    print(separador)
    print("  ¡Venta registrada exitosamente!")

    if datos["cantidad"] < 3:
        print(f"\n  *** ALERTA: Solo quedan {datos['cantidad']} unidades de '{datos['nombre']}' ***")


# -----------------------------------------------------------------------------
# FUNCIÓN 6: MOSTRAR ESTADÍSTICAS
# -----------------------------------------------------------------------------

def mostrar_estadisticas(videojuegos: dict) -> None:
    """Genera reportes estadísticos del inventario."""
    print("\n--- ESTADÍSTICAS DEL INVENTARIO ---")
    if not videojuegos:
        print("  No hay videojuegos registrados.")
        return

    total_juegos = len(videojuegos)
    valor_inventario = sum(d["precio"] * d["cantidad"] for d in videojuegos.values())
    promedio_precios = sum(d["precio"] for d in videojuegos.values()) / total_juegos

    mas_costoso_codigo = max(videojuegos, key=lambda c: videojuegos[c]["precio"])
    mas_costoso = videojuegos[mas_costoso_codigo]

    mayor_stock_codigo = max(videojuegos, key=lambda c: videojuegos[c]["cantidad"])
    mayor_stock = videojuegos[mayor_stock_codigo]

    print(f"  Total de videojuegos registrados : {total_juegos}")
    print(f"  Valor total del inventario       : ${valor_inventario:,.0f}")
    print(f"  Videojuego más costoso           : {mas_costoso['nombre']} (${mas_costoso['precio']:,.0f})")
    print(f"  Mayor cantidad disponible        : {mayor_stock['nombre']} ({mayor_stock['cantidad']} unidades)")
    print(f"  Promedio de precios              : ${promedio_precios:,.0f}")

    # Estadísticas adicionales del historial de ventas
    if historial_ventas:
        total_recaudado = sum(v["total"] for v in historial_ventas)
        ventas_por_juego: dict = {}
        for venta in historial_ventas:
            nombre = venta["nombre"]
            ventas_por_juego[nombre] = ventas_por_juego.get(nombre, 0) + venta["cantidad"]
        mas_vendido = max(ventas_por_juego, key=lambda n: ventas_por_juego[n])

        print(f"\n  --- Historial de ventas ---")
        print(f"  Total recaudado en ventas        : ${total_recaudado:,.0f}")
        print(f"  Videojuego más vendido           : {mas_vendido} ({ventas_por_juego[mas_vendido]} unidades)")


# -----------------------------------------------------------------------------
# FUNCIÓN 7: ELIMINAR VIDEOJUEGO
# -----------------------------------------------------------------------------

def eliminar_videojuego(videojuegos: dict) -> None:
    """Remueve un videojuego del inventario."""
    print("\n--- ELIMINAR VIDEOJUEGO ---")
    codigo = input("Código del videojuego a eliminar: ").strip().upper()

    if codigo not in videojuegos:
        print(f"  No existe un videojuego con el código '{codigo}'.")
        return

    nombre = videojuegos[codigo]["nombre"]
    confirmacion = input(f"  ¿Confirma eliminar '{nombre}'? (s/n): ").strip().lower()
    if confirmacion == "s":
        del videojuegos[codigo]
        print(f"  Videojuego '{nombre}' eliminado del inventario.")
    else:
        print("  Operación cancelada.")


# -----------------------------------------------------------------------------
# FUNCIÓN ADICIONAL: BUSCAR POR PLATAFORMA
# -----------------------------------------------------------------------------

def buscar_por_plataforma(videojuegos: dict) -> None:
    """Busca videojuegos filtrando por plataforma."""
    print("\n--- BUSCAR POR PLATAFORMA ---")
    plataforma = input("Ingrese la plataforma: ").strip()
    if not plataforma:
        print("  La plataforma no puede estar vacía.")
        return

    resultados = {
        codigo: datos
        for codigo, datos in videojuegos.items()
        if plataforma.lower() in datos["plataforma"].lower()
    }

    if not resultados:
        print(f"  No se encontraron videojuegos para la plataforma '{plataforma}'.")
        return

    print(f"\n  Resultados para '{plataforma}':")
    for codigo, datos in resultados.items():
        print(f"  [{codigo}] {datos['nombre']} — ${datos['precio']:,.0f} — Stock: {datos['cantidad']}")


# -----------------------------------------------------------------------------
# FUNCIÓN ADICIONAL: MOSTRAR HISTORIAL DE VENTAS
# -----------------------------------------------------------------------------

def mostrar_historial_ventas() -> None:
    """Muestra el historial completo de ventas registradas en la sesión."""
    print("\n--- HISTORIAL DE VENTAS ---")
    if not historial_ventas:
        print("  No se han registrado ventas aún.")
        return

    for i, venta in enumerate(historial_ventas, start=1):
        print(
            f"  {i}. [{venta['codigo']}] {venta['nombre']} — "
            f"x{venta['cantidad']} — Total: ${venta['total']:,.0f}"
        )


# -----------------------------------------------------------------------------
# FUNCIÓN 8: MENÚ PRINCIPAL
# -----------------------------------------------------------------------------

def bienvenida() -> None:
    """Muestra el mensaje de bienvenida al iniciar el sistema."""
    # Personaliza este mensaje con el nombre de tu tienda y un eslogan propio
    print("\n" + "*" * 40)
    print(f"   Bienvenido a {NOMBRE_TIENDA}")
    print("   'Tu mundo gamer, a un clic'")
    print("*" * 40)


def menu() -> None:
    """Muestra el menú principal y gestiona la navegación del sistema."""
    videojuegos = dict(videojuegos_iniciales)  # Copia de trabajo
    bienvenida()

    while True:
        print("\n" + "=" * 36)
        print(f"   {NOMBRE_TIENDA}")  # <--- El nombre de tu tienda aparece aquí
        print("=" * 36)
        print("  1. Agregar videojuego")
        print("  2. Mostrar inventario")
        print("  3. Buscar videojuego por código")
        print("  4. Actualizar precio")
        print("  5. Registrar venta")
        print("  6. Mostrar estadísticas")
        print("  7. Eliminar videojuego")
        print("  8. Buscar por plataforma")
        print("  9. Historial de ventas")
        print("  0. Salir")
        print("-" * 36)

        opcion = input("  Seleccione una opción: ").strip()

        if opcion == "1":
            agregar_videojuego(videojuegos)
        elif opcion == "2":
            mostrar_inventario(videojuegos)
        elif opcion == "3":
            buscar_videojuego(videojuegos)
        elif opcion == "4":
            actualizar_precio(videojuegos)
        elif opcion == "5":
            registrar_venta(videojuegos)
        elif opcion == "6":
            mostrar_estadisticas(videojuegos)
        elif opcion == "7":
            eliminar_videojuego(videojuegos)
        elif opcion == "8":
            buscar_por_plataforma(videojuegos)
        elif opcion == "9":
            mostrar_historial_ventas()
        elif opcion == "0":
            # Personaliza el mensaje de despedida
            print(f"\n  ¡Gracias por usar {NOMBRE_TIENDA}! Hasta la próxima. 👾")
            break
        else:
            print("  Opción no válida. Ingrese un número del 0 al 9.")


# -----------------------------------------------------------------------------
# PUNTO DE ENTRADA
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    menu()

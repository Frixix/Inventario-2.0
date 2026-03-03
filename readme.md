# Inventario-2.0

Sistema de gestión de inventario desarrollado en Python utilizando Tkinter y SQLite.

---

## Descripción General

Inventario-2.0 es una aplicación de escritorio diseñada bajo principios de arquitectura limpia y separación de responsabilidades. El sistema permite registrar productos y gestionar inventario mediante movimientos controlados.

---

## Tecnologías Utilizadas

- Python 3.10
- Tkinter (Interfaz gráfica)
- SQLite (Base de datos local)
- Arquitectura por capas

---

## Arquitectura del Proyecto

El sistema está dividido en tres capas principales:

### 1. Presentación (GUI)
Ubicada en la carpeta `ui/`
- Ventana principal con tabla de productos
- Formulario modal para registro
- Manejo controlado del estado de interfaz

### 2. Lógica de Negocio
Ubicada en `core/logica_inventario.py`
- Validaciones críticas
- Control de stock
- Registro de movimientos
- Protección contra stock negativo

### 3. Acceso a Datos
Ubicada en `core/database.py`
- Creación de tablas
- Consultas a SQLite
- Registro de movimientos

La GUI nunca interactúa directamente con la base de datos.

---

## Estado Actual del Proyecto

### FASE 2
- Registro de productos funcional
- Arquitectura limpia implementada
- Validaciones completas
- Reemplazo del sistema de consola por GUI

### FASE 3 – Día 1
- Implementación de ventana modal real
- Control de apertura única del formulario
- Manejo correcto del cierre con la X
- Mejora visual del Treeview
- Mejor control de estado de interfaz

---

## Próximas Implementaciones

- Entrada de inventario desde GUI
- Salida de inventario
- Alertas visuales de stock mínimo
- Historial de movimientos
- Posible sistema de roles

---

## Principios del Proyecto

- Separación estricta por capas
- Validaciones en la lógica, no en la interfaz
- Modificaciones de stock únicamente mediante movimientos
- Código estructurado para escalabilidad futura

---

## Autor

Proyecto desarrollado como parte de proceso de aprendizaje estructurado en desarrollo de software.
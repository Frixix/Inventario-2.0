# Arquitectura del Sistema de Inventario

> Documento vivo. Esta arquitectura evoluciona a medida que el sistema crece.
> En esta fase (FASE 1) el objetivo es un inventario funcional, simple y confiable.

---

## Objetivo del Sistema (FASE 1)

Aplicación de escritorio local para:

* Registrar productos
* Registrar salidas de inventario
* Visualizar stock actual
* Ajustar stock manualmente desde un modo administrador

Contexto:

* País: Colombia
* Moneda base: Pesos Colombianos (COP)
* Uso local (sin red, sin nube, sin DIAN por ahora)

---

## Principios de Diseño

1. Simplicidad antes que completitud
2. El stock es resultado de movimientos, no edición directa
3. Una responsabilidad por capa
4. Las reglas viven en la lógica, no en la interfaz
5. Toda modificación de stock debe ser trazable

---

## Arquitectura General

```
INTERFAZ (GUI)
    ↓
LÓGICA DE NEGOCIO
    ↓
BASE DE DATOS (SQLite)
```

---

## Capa de Interfaz

Responsabilidades:

* Capturar datos del usuario
* Mostrar información de productos y stock
* Enviar acciones a la capa de lógica

Restricciones:

* No contiene reglas de negocio
* No modifica el stock directamente
* No accede directamente a la base de datos

---

## Capa de Lógica de Negocio

Responsabilidades:

* Validar reglas del inventario
* Controlar modificaciones de stock
* Registrar movimientos (salidas y ajustes)
* Coordinar operaciones entre interfaz y base de datos

Esta capa es el núcleo del sistema.

---

## Capa de Datos

Responsabilidades:

* Persistir información en SQLite
* Ejecutar consultas parametrizadas
* Garantizar integridad básica de los datos

Restricciones:

* No contiene reglas de negocio
* No toma decisiones

---

## Modelo de Inventario (FASE 1)

### Tabla: productos

Propósito:
Representa los artículos que el negocio maneja. Un producto puede existir aunque aún no tenga movimientos registrados.

Campos:

* id

  * Clave primaria (PRIMARY KEY)
  * Entero autoincremental
  * Identifica de forma única a cada producto

* nombre

  * Texto
  * Obligatorio
  * Nombre legible del producto

* precio_venta

  * Entero
  * Representa el valor en Pesos Colombianos (COP)
  * No admite valores negativos

* stock_actual

  * Entero
  * Representa la cantidad disponible actual
  * Este valor se modifica únicamente desde la lógica

* stock_minimo

  * Entero
  * Umbral para alertas de inventario bajo

* activo

  * Entero (0 o 1)
  * Indica si el producto está disponible para operaciones

---

### Tabla: movimientos_inventario

Propósito:
Registra todos los cambios que afectan el stock de un producto. Es la base de la trazabilidad del inventario.

Campos:

* id

  * Clave primaria (PRIMARY KEY)
  * Entero autoincremental

* producto_id

  * Clave foránea (FOREIGN KEY)
  * Referencia a productos(id)
  * Un movimiento no puede existir sin producto asociado

* tipo_movimiento

  * Texto
  * Valores esperados: ENTRADA, SALIDA, AJUSTE_ADMIN

* cantidad

  * Entero
  * Siempre positivo
  * El signo (suma o resta) depende del tipo de movimiento

* fecha

  * Texto o timestamp
  * Fecha y hora en que ocurrió el movimiento

* motivo

  * Texto
  * Obligatorio solo cuando el tipo es AJUSTE_ADMIN

---

## Relación entre tablas

* Un producto puede tener cero o muchos movimientos
* Cada movimiento pertenece a un solo producto

Esta relación se implementa mediante la clave foránea movimientos_inventario.producto_id → productos.id

---

## Reglas de Integridad (a nivel conceptual)

* No pueden existir movimientos sin producto
* No se permiten cantidades iguales a cero
* El stock no se modifica directamente en la base de datos
* Toda modificación de stock debe generar un movimiento asociado

Estas reglas se aplican desde la capa de lógica, no desde la base de datos




---

## Línea de Tiempo de Desarrollo (Roadmap Evolutivo)

> Esta línea de tiempo describe dónde estamos y hacia dónde vamos.
> Es un bloque vivo y se actualizará conforme el sistema evolucione.

### FASE 0 — Fundamentos (COMPLETADA)

**Objetivo:** establecer la base técnica mínima.

Incluyó:
- Estructura del proyecto definida
- Base de datos SQLite creada
- Tablas `productos` y `movimientos_inventario`
- Conexión a base de datos y operaciones básicas

Resultado:
- Persistencia funcional
- Base estable para el inventario

---

### FASE 1 — Inventario Funcional (EN PROGRESO — ESTAMOS AQUÍ)

**Objetivo:** inventario usable, consistente y controlado.

Incluye:
- Inserción de productos
- Consulta de stock actual
- Registro de movimientos (ENTRADA / SALIDA / AJUSTE_ADMIN)
- Validación de stock negativo desde la lógica
- Ajustes manuales trazables

Estado actual:
- Modelo de datos definido
- Funciones de base de datos operativas
- Obtención de stock por producto funcionando
- En desarrollo: validación de salidas desde la lógica

Resultado esperado:
- Stock siempre consistente
- Ningún movimiento inválido
- Trazabilidad completa

---

### FASE 1.1 — Formalización de la Lógica (PENDIENTE)

**Objetivo:** separar completamente la lógica de negocio del punto de entrada.

Incluye:
- Módulo o clase dedicada a la lógica de inventario
- Centralización de validaciones
- Preparación para múltiples interfaces

---

### FASE 2 — Interfaz Gráfica Básica (PENDIENTE)

**Objetivo:** operar el inventario sin interacción directa con código.

Incluye:
- Listado de productos
- Registro de entradas y salidas
- Visualización de stock
- Alertas básicas

---

### FASE 3 — Usuarios y Control (FUTURO)

**Objetivo:** control de acceso y responsabilidades.

Incluye:
- Usuarios
- Roles (administrador / operador)
- Restricción de acciones críticas

---

### FASE 4 — Facturación e Impuestos (FUTURO)

**Objetivo:** soporte para operación comercial en Colombia.

Incluye:
- Facturación
- IVA Colombia
- Totales y reportes básicos

---

### FASE 5 — Escalabilidad (FUTURO)

**Objetivo:** preparar el sistema para crecimiento técnico.

Incluye:
- Refactor de arquitectura
- Posible cambio de motor de base de datos
- API o sincronización externa

---

### Principio Rector del Roadmap

- No se avanza de fase con inconsistencias
- Cada fase deja el sistema estable
- La claridad tiene prioridad sobre la velocidad

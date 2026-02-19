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

### Producto

Campos mínimos:

* id
* nombre
* precio_venta (entero, COP)
* stock_actual
* stock_minimo
* activo

---

### Movimiento de Inventario

Todo cambio de stock se registra como un movimiento.

Tipos de movimiento:

* ENTRADA
* SALIDA
* AJUSTE_ADMIN

Campos mínimos:

* id
* producto_id
* tipo_movimiento
* cantidad
* fecha
* motivo (obligatorio para AJUSTE_ADMIN)

---

## Reglas Fundamentales

* No se permite stock negativo
* No se permiten precios negativos
* El nombre del producto es obligatorio
* El stock solo se modifica a través de la lógica
* Todo ajuste manual debe quedar registrado

---

## Estado del Documento

Este documento se actualizará progresivamente a medida que se agreguen:

* Usuarios y roles
* Facturación
* Impuestos (IVA Colombia)
* Reportes
* Integraciones externas

Cada cambio deberá justificar su impacto en esta arquitectura.

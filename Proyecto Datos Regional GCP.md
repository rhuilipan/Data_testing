# 🧾 Diseño de Plataforma de Datos Federada – Google Cloud Platform

**Cliente**: Global Airline Group  
**Proyecto**: Plataforma Federada de Ingesta y Procesamiento de Datos  
**Consultor**: GCP – Especialista en Arquitectura Cloud  
**Fecha**: Abril 2025

---

## 1. Introducción

Este documento presenta una solución integral para construir una **plataforma de datos federada sobre Google Cloud Platform (GCP)**. Esta plataforma tiene como fin integrar y armonizar datos distribuidos geográficamente en distintas regiones y proyectos de GCP, permitiendo análisis corporativos eficientes sobre indicadores clave como rentabilidad de rutas, eficiencia de combustible y satisfacción del cliente.

El objetivo es maximizar el **valor del dato** con una arquitectura escalable, gobernada y optimizada en costos, mediante servicios administrados de GCP, manteniendo alta disponibilidad y rendimiento en operaciones interregionales.

---

## 2. Problemática

Actualmente, la organización enfrenta desafíos técnicos y operativos derivados de:

- **Silos de datos regionales** en múltiples proyectos GCP.
- **Esquemas inconsistentes** entre fuentes.
- Latencias elevadas en análisis multi-región.
- Costos crecientes por replicación manual o soluciones ad-hoc.
- Falta de trazabilidad y unificación del modelo de datos global.

---

## 3. Solución Propuesta

Se propone una **arquitectura federada**, que permita ingestar, catalogar y procesar datos provenientes de BigQuery, Cloud Storage y CloudSQL en múltiples regiones de GCP, soportando flujos en **tiempo real y batch**, con herramientas nativas para gobernanza, eficiencia y análisis avanzado.

---

### 3.1 Arquitectura General

La solución incluye los siguientes componentes:

- **Cloud Pub/Sub**: canal de ingestión de eventos para procesamiento en tiempo real.
- **Cloud Functions**: disparadores ligeros para automatización basada en eventos.
- **Cloud Dataflow**: procesamiento ETL/ELT en batch y streaming.
- **Cloud Storage**: zona de datos crudos y almacenamiento intermedio.
- **BigQuery**: motor principal de almacenamiento analítico y federación SQL.
- **BigQuery Omni** (opcional): consultas entre nubes o regiones remotas.
- **Dataplex**: gobernanza de datos y definición de zonas (raw, curado, analítico).
- **Data Catalog**: catálogo de metadatos y control de versiones de esquemas.
- **Looker / BI Engine**: visualización y análisis de alto rendimiento.

---

### 3.2 Flujo de Datos

1. **Captura**
   - **CloudSQL (PostgreSQL)**: extraído con Dataflow vía JDBC.
   - **Cloud Storage**: eventos `OBJECT_FINALIZE` disparan funciones para ETL.
   - **BigQuery**: datasets regionales exportados con `EXPORT DATA`.

2. **Ingesta**
   - Archivos aterrizan en buckets por región/domino (`raw/region_x/...`).
   - Cloud Dataflow mueve datos a BigQuery y los transforma.

3. **Procesamiento**
   - Transformación y normalización de esquemas.
   - Aplicación de reglas de negocio (e.g., conversión de monedas, unificación de columnas).
   - Consolidación en datasets curados listos para análisis.

4. **Federación y Consumo**
   - Consultas SQL desde BigQuery entre regiones o proyectos.
   - Materialización de vistas para KPIs de alta demanda.
   - Dashboards en Looker / Data Studio con acceso controlado.

---

## 4. Servicios y Costos Estimados

| Servicio              | Rol en la Arquitectura | Estimación Mensual (USD) |
|-----------------------|-------------------------|---------------------------|
| **Cloud Pub/Sub**     | Ingesta de eventos      | $10 – $20                 |
| **Cloud Functions**   | Disparadores            | $5 – $15                  |
| **Cloud Storage**     | 10 TB (landing/raw)     | $100 – $150               |
| **CloudSQL**          | PostgreSQL regional     | $200 – $500               |
| **Cloud Dataflow**    | Procesamiento diario    | $500 – $1,200             |
| **BigQuery**          | 10 TB almacenados + 5 TB consultados | $400 – $800 |
| **BigQuery Omni**     | Opcional (multi-cloud)  | $100 – $300               |
| **Dataplex / Catalog**| Gobernanza, metadatos   | Sin costo directo         |
| **Looker / Studio**   | BI y dashboards         | Incluido (según plan)     |

> ⚠️ Los costos varían según el volumen de datos, frecuencia de consulta, y ubicación regional. Se recomienda aplicar prácticas como **particionado, clustering y uso de vistas materializadas** para optimizar.

---

## 5. Gobernanza y Consistencia

- **Dataplex** se usará para definir zonas de datos: `raw`, `curated`, `analytics`.
- **Data Catalog** permite clasificar y versionar esquemas.
- Los pipelines incorporan validación de esquema antes de cargar datos.
- Uso de JSON schemas versionados con Git para asegurar integridad en transformaciones.

---

## 6. Estrategias de Optimización

- **Vistas materializadas** para reducir consultas interregionales costosas.
- **BI Engine** para acelerar dashboards con caché en memoria.
- **Job scheduling** de agregaciones pesadas en horarios de baja demanda.
- **Dataflow autoscaling** para adaptarse al volumen dinámico.

---

## 7. Riesgos y Mitigaciones

| Riesgo                        | Mitigación                                   |
|------------------------------|----------------------------------------------|
| Latencia entre regiones      | Caching + vistas materializadas              |
| Cambios en esquemas fuente   | Validación automática + versionado de esquema |
| Costos de escaneo elevado    | Particionado + Clustering + vistas agregadas |
| Fallos en pipelines          | Alertas + retries + DLQ con Pub/Sub          |

---

## 8. Recomendaciones

- Establecer un proyecto “core” para almacenamiento y consumo central.
- Aplicar IaC (Terraform) para replicabilidad y control de cambios.
- Establecer prácticas DevOps/DataOps para despliegue y monitoreo.
- Monitorear adopción y calidad de datos con herramientas de lineage.

---

## 9. Conclusión

Esta arquitectura federada permite a la compañía superar sus limitaciones actuales de integración, disponibilidad y análisis de datos. Gracias a servicios nativos de GCP, se logra una solución moderna, segura, escalable y lista para habilitar tanto analítica descriptiva como casos de uso avanzados de inteligencia artificial y machine learning.

---

## 10. Repositorio y Entrega

El código, diagramas y documentación se encuentran en el siguiente repositorio público:  
🔗 [https://github.com/juanperez/latam-challenge](https://github.com/juanperez/latam-challenge)

Estructura recomendada del repositorio:


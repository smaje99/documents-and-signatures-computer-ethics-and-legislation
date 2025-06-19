# Documents and Signature

## Objetivo general

Diseñar e implementar una solución informática que permita a personas y organizaciones en Colombia **crear contratos electrónicos válidos, firmarlos digitalmente y garantizar su fuerza legal**, cumpliendo con la normativa colombiana vigente en materia de protección de datos, firma digital, comercio electrónico y prueba digital.

## Normas legales clave en Colombia

| Norma                                         | Contenido clave                                                                                     |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| **Ley 527 de 1999**                     | Reconoce validez legal de mensajes de datos, contratos electrónicos y firma digital.               |
| **Ley 1581 de 2012**                    | Regula el tratamiento de datos personales. Requiere consentimiento previo, informado y verificable. |
| **Decreto 2364 de 2012**                | Define firma electrónica y permite su uso siempre que sea confiable.                               |
| **Ley 1437 de 2011**                    | Código de Procedimiento Administrativo. Reconoce medios electrónicos.                             |
| **Ley 1266 de 2008**                    | Datos financieros y comerciales (Habeas Data financiero).                                           |
| **Circular externa 005 de 2017 – SIC** | Parámetros para gestión segura del consentimiento y firma.                                        |
| **Código General del Proceso**         | Establece la admisibilidad de pruebas electrónicas en juicio.                                      |

## Alcance funcional del Sistema

### Módulos principales

1. **Gestión de usuarios y autenticación**
   * Registro y login de personas naturales y jurídicas.
   * Identificación del rol: firmante, generador, testigo, representante legal.
   * Autenticación robusta (correo, OTP, etc.).
2. **Gestión de contratos**
   * Creación de contratos desde:
     * Texto libre.
     * Plantillas parametrizadas (laboral, arriendo, servicios, etc.).
   * Guardado como borrador.
   * Asociación de partes firmantes y testigos.
   * Programación del orden de firma (secuencial o paralelo).
   * Generación automática del hash del contenido.
3. **Manejo de consentimiento**
   * Solicitud explícita y verificable del consentimiento antes de firmar.
   * Registro del consentimiento con IP, fecha/hora y método.
4. **Firma digital y electrónica**
   * Soporte para dos niveles:
     * Firma electrónica simple (clave + hash + IP).
     * Firma digital certificada (uso de certificados X.509 válidos en Colombia).
   * Cifrado con clave privada del usuario.
   * Verificación de la firma con clave pública (por sistema o entidad de certificación).
   * Validación de integridad mediante hash.
5. Generación de contrato firmado
   * Documento PDF con:
     * Contenido firmado.
     * Código de verificación.
     * Huella digital (hash SHA-256).
     * Trazabilidad de cada firma aplicada.
   * Sellado temporal (timestamp trusted, si se integra con OCSP/TSA).
6. **Registro de auditoría**
   * Cada acción relevante queda registrada:
     * Creación del contrato.
     * Firma.
     * Consentimiento.
     * Validación.
   * Registro con:
     * IP, navegador, geolocalización (opcional), usuario, timestamp.
7. **Gestión documental**
   * Visualización y descarga de contratos.
   * Historial de contratos firmados y estado del flujo.
   * Buscador por nombre, estado, fecha.
8. **Notificaciones**
   * Correo electrónico o push en cada cambio de estado:
     * Firma pendiente, firma aplicada, contrato finalizado, etc.

### Lo que NO incluye el sistema en esta primera fase
* No se incluye generación automática de contratos por IA (solo plantillas definidas).
* No se incluye validación judicial automática (pero cumple requisitos legales para ser admisible).
* No se conecta inicialmente con una entidad certificadora externa (opcional en fases futuras).
* No se incluyen contratos en idiomas diferentes al español.

### Casos de uso clave
1. Juan, abogado independiente, crea un contrato de prestación de servicios, lo firma y lo envía al cliente para su firma digital.
2. Lucía, representante legal de una empresa, sube un contrato laboral y lo firma con su certificado digital.
3. Carlos, freelancer, firma electrónicamente un contrato generado por una plataforma de contratación.

## Arquitectura legal

| Componente Legal                   | Normativa Aplicada                                                  | Implementación Técnica                                                                                       |
| ---------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Validez del contrato**           | Ley 527 de 1999                                                     | Contratos como mensaje de datos almacenado en formato inalterable (PDF + hash)                               |
| **Firma digital**                  | Ley 527 de 1999 + Decreto 2364 de 2012                              | Algoritmos RSA/ECDSA + uso opcional de certificados digitales X.509 emitidos por entidades certificadoras    |
| **Consentimiento informado**       | Ley 1581 de 2012                                                    | Registro de consentimiento con evidencia (IP, fecha, hash del contrato)                                      |
| **Protección de datos personales** | Ley 1581 de 2012 + Circular SIC 005 de 2017                         | Consentimiento previo, autorización explícita, opción de revocar, y política de tratamiento                  |
| **Auditoría de eventos**           | Código General del Proceso + buenas prácticas de gestión probatoria | Registro inmutable de eventos (creación, firma, validación, acceso), incluyendo evidencia técnica y legal    |
| **Fuerza probatoria**              | Código General del Proceso (Art. 244 y 247)                         | Documentos electrónicos firmados y auditados que cumplen requisitos de autenticidad, integridad y no repudio |

### Estándares criptográficos que cumpliremos
| Función                | Estándar                                  |
| ---------------------- | ----------------------------------------- |
| Firma digital          | RSA 2048 o ECDSA + SHA256                 |
| Certificados digitales | X.509                                     |
| Hash                   | SHA-256                                   |
| Firma PDF              | PDF Signature (ISO 32000-2)               |
| Cifrado                | PKCS#1 OAEP o PSS (según firma o cifrado) |

#### Casos de uso con estas herramientas
* Firmante carga su certificado digital (.pem o .pfx) → el sistema extrae la clave * pública y firma con cryptography.
* Contratos se convierten a PDF con reportlab.
* PDF firmado con pyHanko usando clave privada o certificado de la entidad certificadora.
* Sistema registra hash SHA-256 del documento firmado antes y después de la firma.
* Firma validable por terceros a través de hash o UUID en un endpoint tipo /verificar/{código}.

## Arquitectura Técnica
### Componentes del backend

| Módulo              | Función                                      | Tecnología sugerida             |
| ------------------- | -------------------------------------------- | ------------------------------- |
| **Auth & Usuarios** | Registro, login, permisos                    | FastAPI + OAuth2 + JWT          |
| **Contratos**       | Creación y edición de contratos              | SQLAlchemy + Pydantic           |
| **Firma digital**   | Aplicación y verificación                    | `cryptography` con RSA y SHA256 |
| **PDF Generator**   | Conversión a PDF inalterable                 | ReportLab o WeasyPrint          |
| **Consentimiento**  | Captura legal de autorización                | Formularios y hash + logs       |
| **Auditoría**       | Registro de todas las acciones               | Base de datos + timestamps      |
| **Notificaciones**  | Alertas de cambios o requerimientos de firma | Email (SMTP) o Push             |

### Base de datos
* Modelo relacional compatible con SQLite o PostgreSQL, con tablas como:
* users (nombre, rol, correo, clave pública)
* contracts (contenido, estado, hash, pdf_path)
* signatures (contrato_id, firmante, firma, verificado)
* audit_logs (evento, usuario, timestamp, ip)
* consents (usuario, contrato, hash, fecha)

### Seguridad
* Autenticación robusta (JWT, hashed passwords con bcrypt).
* Encriptación de claves privadas en reposo.
* Verificación de integridad con hash SHA-256.
* Protección contra acceso no autorizado a contratos.
* Firma digital real usando certificados o claves locales.

### Formato de contrato final
El contrato firmado debe contener:
* Contenido inalterable (PDF).
* Lista de firmantes y sus huellas digitales.
* Hash del contrato.
* Firma(s) incrustada(s).
* Metadata de auditoría.
* Código de verificación para terceros (por ejemplo, en URL tipo verificar/{uuid}).

## Actores del Sistema
| Actor                      | Descripción                                                                      |
| -------------------------- | -------------------------------------------------------------------------------- |
| **Generador del contrato** | Persona o entidad que redacta y estructura el contrato.                          |
| **Firmante**               | Persona natural o jurídica que debe firmar el contrato.                          |
| **Administrador**          | Encargado de supervisar operaciones, validar identidades, y gestionar auditoría. |
| **Verificador externo**    | Persona o entidad que consulta la validez de un contrato firmado.                |

## Procesos clave
1. Creación del contrato
   * Redacción del contrato desde texto libre o plantilla.
   * Selección de partes involucradas (firmantes, testigos).
   * Generación del hash del contenido.
   * Programación del orden de firma.
   * Guardado como borrador o solicitud de firma inmediata.
2. Solicitud de firma y consentimiento
   * Envío de notificaciones a los firmantes.
   * Visualización del contrato.
   * Aceptación del consentimiento informado (Ley 1581 de 2012).
   * Registro del consentimiento (IP, fecha, hash, firmante).
3. Firma digital del contrato
   * El firmante firma usando:
      * Clave privada personal
      * Certificado digital X.509 (opcional)
   * Se genera firma criptográfica sobre el hash del contrato.
   * Se almacena firma, timestamp, y evidencia.
4. Validación y auditoría
   * Verificación de firma con clave pública del firmante.
   * Revisión del historial de eventos (creación, consentimiento, firma).
   * Validación externa del contrato firmado (vía hash o UUID).
5. Generación de contrato final
   * PDF con contenido + firmas incrustadas.
   * Metadatos del contrato y código de verificación.
   * Protección contra alteración.

## Requisitos funcionales
| ID   | Requisito funcional                                                                    |
| ---- | -------------------------------------------------------------------------------------- |
| RF01 | El sistema debe permitir a un usuario crear un contrato desde texto libre o plantilla. |
| RF02 | El sistema debe permitir agregar múltiples firmantes a un contrato.                    |
| RF03 | El sistema debe generar un hash (SHA-256) único del contenido del contrato.            |
| RF04 | El sistema debe registrar consentimiento explícito del firmante antes de la firma.     |
| RF05 | El sistema debe permitir aplicar firma digital sobre el contrato.                      |
| RF06 | El sistema debe validar la firma digital usando la clave pública del firmante.         |
| RF07 | El sistema debe generar un documento PDF final con firmas embebidas.                   |
| RF08 | El sistema debe permitir consultar un contrato firmado desde un código hash o UUID.    |
| RF09 | El sistema debe registrar cada acción importante en un log de auditoría.               |
| RF10 | El sistema debe garantizar la integridad del contrato en todo momento.                 |
| RF11 | El sistema debe permitir autenticar a usuarios de manera segura (JWT).                 |
| RF12 | El sistema debe permitir al administrador revisar eventos, registros y firmas.         |

## Requisitos adicionales no funcionales
* RFN01: Compatibilidad legal con Ley 527 de 1999, Ley 1581 de 2012.
* RFN02: Seguridad criptográfica (RSA, SHA-256, claves privadas protegidas).
* RFN03: Rendimiento aceptable para múltiples operaciones concurrentes.
* RFN04: Escalabilidad a PostgreSQL u otros motores de base de datos.
* RFN05: Interfaz clara, accesible, y con trazabilidad total.

## Diccionario de datos
### Tabla: `users` — Usuarios del sistema
| Campo          | Tipo         | Restricciones                    | Descripción                     |
| -------------- | ------------ | -------------------------------- | ------------------------------- |
| id             | UUID      | PK                | Identificador único del usuario |
| full\_name     | VARCHAR(150) | NOT NULL                         | Nombre completo                 |
| email          | VARCHAR(100) | UNIQUE, NOT NULL                 | Correo electrónico del usuario  |
| password\_hash | TEXT         | NOT NULL                         | Hash de la contraseña           |
| public\_key    | TEXT         | NULLABLE                         | Clave pública del usuario (PEM) |
| role           | VARCHAR(20)  | NOT NULL (admin, user, verifier) | Rol del usuario en el sistema   |
| is\_active     | BOOLEAN      | DEFAULT TRUE                     | Estado del usuario              |
| created\_at    | TIMESTAMP       | DEFAULT timestamp                | Fecha de creación (Unix)        |

### Tabla: `contracts` — Contratos electrónicos
| Campo       | Tipo         | Restricciones          | Descripción                                       |
| ----------- | ------------ | ---------------------- | ------------------------------------------------- |
| id          | UUID    | PK,       | Identificador único del contrato                  |
| creator\_id | UUID      | FK(users.id), NOT NULL | Usuario que creó el contrato                      |
| title       | VARCHAR(150) | NOT NULL               | Título del contrato                               |
| content     | TEXT         | NOT NULL               | Contenido del contrato                            |
| hash        | VARCHAR(64)  | NOT NULL, UNIQUE       | Hash SHA-256 del contenido                        |
| status      | VARCHAR(20)  | DEFAULT 'pendiente'    | Estado: pendiente, firmado, cancelado, finalizado |
| pdf\_path   | TEXT         | NULLABLE               | Ruta del PDF generado con firmas                  |
| uuid        | UUID         | UNIQUE, NOT NULL       | Código público de validación externa              |
| created\_at | TIMESTAMP       | DEFAULT timestamp      | Fecha de creación (Unix)                          |

### Tabla: signatures — Firmas aplicadas
| Campo        | Tipo        | Restricciones                  | Descripción                      |
| ------------ | ----------- | ------------------------------ | -------------------------------- |
| id           | UUID     | PK              | Identificador único de la firma  |
| contract\_id | INTEGER     | FK(contracts.id), NOT NULL     | Contrato relacionado             |
| user\_id     | INTEGER     | FK(users.id), NOT NULL         | Usuario firmante                 |
| signature    | BLOB/TEXT   | NOT NULL                       | Firma digital (binaria o base64) |
| method       | VARCHAR(20) | NOT NULL (digital/electrónica) | Tipo de firma aplicada           |
| verified     | BOOLEAN     | DEFAULT FALSE                  | Si fue verificada con éxito      |
| verified\_at | TIMESTAMP      | NULLABLE                       | Timestamp de verificación        |
| signed\_at   | TIMESTAMP      | DEFAULT timestamp              | Fecha de aplicación de la firma  |

### Tabla: consents — Consentimiento informado
| Campo          | Tipo        | Restricciones              | Descripción                                     |
| -------------- | ----------- | -------------------------- | ----------------------------------------------- |
| id             | UUID     | PK          | Identificador único del consentimiento          |
| user\_id       | INTEGER     | FK(users.id), NOT NULL     | Usuario que da el consentimiento                |
| contract\_id   | INTEGER     | FK(contracts.id), NOT NULL | Contrato relacionado                            |
| ip\_address    | VARCHAR(45) | NOT NULL                   | IP del usuario al momento del consentimiento    |
| hash\_snapshot | VARCHAR(64) | NOT NULL                   | Hash del contrato al momento del consentimiento |
| created\_at    | TIMESTAMP      | DEFAULT timestamp          | Fecha del consentimiento                        |

### Tabla: audit_logs — Registro de auditoría
| Campo       | Tipo         | Restricciones          | Descripción                                               |
| ----------- | ------------ | ---------------------- | --------------------------------------------------------- |
| id          | UUID      | PK      | Identificador del evento                                  |
| user\_id    | INTEGER      | FK(users.id), NULLABLE | Usuario que originó el evento (puede ser null si externo) |
| action      | VARCHAR(100) | NOT NULL               | Acción realizada (crear, firmar, validar, etc.)           |
| detail      | TEXT         | NOT NULL               | Descripción específica de la acción                       |
| ip\_address | VARCHAR(45)  | NULLABLE               | IP del origen del evento                                  |
| timestamp   | TIMESTAMP       | DEFAULT timestamp      | Momento exacto del evento                                 |

### Tabla: verifications — Consultas de validación pública
| Campo        | Tipo        | Restricciones     | Descripción                     |
| ------------ | ----------- | ----------------- | ------------------------------- |
| id           | UUID     | PK | Identificador único de consulta |
| contract\_id | INTEGER     | FK(contracts.id)  | Contrato verificado             |
| source\_ip   | VARCHAR(45) | NOT NULL          | IP del verificador externo      |
| method       | VARCHAR(20) | NULLABLE          | Método usado (hash, uuid)       |
| timestamp    | TIMESTAMP      | DEFAULT timestamp | Fecha de la consulta            |

### Consideraciones técnicas adicionales
* Todos los timestamps se manejan en formato Unix (int) por compatibilidad con SQLite, PostgreSQL y eficiencia de indexación.
* Las firmas se almacenan como TEXT (Base64) o BLOB, dependiendo del motor de base de datos.
* Los campos uuid se generan con uuid4() y permiten validaciones externas sin exponer IDs internos.
* Se contemplan roles diferenciados (user, admin, verifier) para aplicar lógica de permisos.






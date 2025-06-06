/* -----------------------------------------------------------
   B.D. Investigación de Accidentes  |  MySQL 8.0
   Versión: JUN-2025 – ajustes finales
      • “resumen” y “relato” pasan a ACCIDENTES
      • “plazo” en PRESCRIPCIONES ahora es DATE
----------------------------------------------------------- */

SET FOREIGN_KEY_CHECKS = 0;
SET NAMES utf8mb4;

/* 0. HOLDINGS (sin RUT) */
CREATE TABLE IF NOT EXISTS holdings (
  holding_id   INT AUTO_INCREMENT PRIMARY KEY,
  nombre       VARCHAR(255) NOT NULL,
  created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

/* 1. EMPRESAS */
CREATE TABLE IF NOT EXISTS empresas (
  empresa_id          INT AUTO_INCREMENT PRIMARY KEY,
  holding_id          INT,
  empresa_sel         VARCHAR(255) NOT NULL,      -- razón social
  rut_empresa         VARCHAR(20)  NOT NULL UNIQUE,
  actividad           VARCHAR(255),
  direccion_empresa   VARCHAR(255),
  telefono            VARCHAR(30),
  representante_legal VARCHAR(255),
  region              VARCHAR(100),
  comuna              VARCHAR(100),
  created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_emp_holding
    FOREIGN KEY (holding_id) REFERENCES holdings (holding_id)
);

/* 2. CENTROS DE TRABAJO */
CREATE TABLE IF NOT EXISTS centros_trabajo (
  centro_id        INT AUTO_INCREMENT PRIMARY KEY,
  empresa_id       INT NOT NULL,
  nombre_local     VARCHAR(255) NOT NULL,
  direccion_centro VARCHAR(255),
  CONSTRAINT fk_centro_empresa
    FOREIGN KEY (empresa_id) REFERENCES empresas (empresa_id)
);

/* 3. TRABAJADORES (datos permanentes) */
CREATE TABLE IF NOT EXISTS trabajadores (
  trabajador_id     INT AUTO_INCREMENT PRIMARY KEY,
  empresa_id        INT,                          -- empleador vigente
  nombre_trabajador VARCHAR(255),
  rut_trabajador    VARCHAR(20) UNIQUE,
  fecha_nacimiento  DATE,
  nacionalidad      VARCHAR(100),
  estado_civil      VARCHAR(50),
  domicilio         VARCHAR(255),
  created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_trab_emp
    FOREIGN KEY (empresa_id) REFERENCES empresas (empresa_id)
);

/* 4. ACCIDENTES (snapshot laboral + resumen/relato) */
CREATE TABLE IF NOT EXISTS accidentes (
  accidente_id         INT AUTO_INCREMENT PRIMARY KEY,
  centro_id            INT NOT NULL,
  trabajador_id        INT,
  fecha_accidente      DATE,
  hora_accidente       TIME,
  lugar_accidente      VARCHAR(255),
  tipo_accidente       VARCHAR(100),
  naturaleza_lesion    VARCHAR(255),
  parte_afectada       VARCHAR(255),
  tarea                VARCHAR(255),
  operacion            VARCHAR(255),

  /* ----- snapshot del trabajador en la fecha del accidente ----- */
  cargo_trabajador     VARCHAR(255),
  contrato             VARCHAR(50),       -- tipo de contrato
  antiguedad_empresa   VARCHAR(50),
  antiguedad_cargo     VARCHAR(50),

  /* ----- consecuencias y síntesis ----- */
  danos_personas       TEXT,
  danos_propiedad      TEXT,
  perdidas_proceso     TEXT,
  resumen              TEXT,
  relato               TEXT,

  CONSTRAINT fk_acc_centro
    FOREIGN KEY (centro_id)     REFERENCES centros_trabajo (centro_id),
  CONSTRAINT fk_acc_trab
    FOREIGN KEY (trabajador_id) REFERENCES trabajadores     (trabajador_id)
);

/* 5. INFORMES (versionados; ya SIN resumen/relato) */
CREATE TABLE IF NOT EXISTS informes (
  informe_id      INT AUTO_INCREMENT PRIMARY KEY,
  accidente_id    INT NOT NULL,
  version         SMALLINT NOT NULL,
  is_current      BOOLEAN  DEFAULT 0,
  codigo          VARCHAR(50),
  fecha_informe   DATE,
  investigador    VARCHAR(255),
  created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY unq_acc_version (accidente_id, version),
  CONSTRAINT fk_inf_acc
    FOREIGN KEY (accidente_id) REFERENCES accidentes(accidente_id)
);

/* Trigger: sólo un informe vigente por accidente */
DELIMITER $$
CREATE TRIGGER trg_informes_before_ins
BEFORE INSERT ON informes
FOR EACH ROW
BEGIN
  IF NEW.is_current = 1 THEN
    UPDATE informes SET is_current = 0
    WHERE accidente_id = NEW.accidente_id;
  END IF;
END$$
DELIMITER ;

/* 6. ÁRBOLES DE CAUSAS (JSON, versionados) */
CREATE TABLE IF NOT EXISTS arbol_causas (
  arbol_id       INT AUTO_INCREMENT PRIMARY KEY,
  accidente_id   INT NOT NULL,
  version        SMALLINT NOT NULL,
  is_current     BOOLEAN DEFAULT 0,
  arbol_json     JSON,
  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY unq_arbol_acc_ver (accidente_id, version),
  CONSTRAINT fk_arbol_acc
    FOREIGN KEY (accidente_id) REFERENCES accidentes(accidente_id)
);

/* Trigger: sólo un árbol vigente por accidente */
DELIMITER $$
CREATE TRIGGER trg_arbol_before_ins
BEFORE INSERT ON arbol_causas
FOR EACH ROW
BEGIN
  IF NEW.is_current = 1 THEN
    UPDATE arbol_causas SET is_current = 0
    WHERE accidente_id = NEW.accidente_id;
  END IF;
END$$
DELIMITER ;

/* 7. HECHOS */
CREATE TABLE IF NOT EXISTS hechos (
  hecho_id      INT AUTO_INCREMENT PRIMARY KEY,
  accidente_id  INT NOT NULL,
  secuencia     SMALLINT,
  descripcion   TEXT,
  CONSTRAINT fk_hecho_acc
    FOREIGN KEY (accidente_id) REFERENCES accidentes(accidente_id)
);

/* 8. PRESCRIPCIONES (plazo ahora DATE) */
CREATE TABLE IF NOT EXISTS prescripciones (
  prescripcion_id INT AUTO_INCREMENT PRIMARY KEY,
  accidente_id    INT NOT NULL,
  tipo            VARCHAR(100),
  prioridad       VARCHAR(50),
  plazo           DATE,            -- fecha límite para la medida
  responsable     VARCHAR(255),
  descripcion     TEXT,
  CONSTRAINT fk_presc_acc
    FOREIGN KEY (accidente_id) REFERENCES accidentes(accidente_id)
);

/* 9. DECLARACIONES */
CREATE TABLE IF NOT EXISTS declaraciones (
  declaracion_id INT AUTO_INCREMENT PRIMARY KEY,
  accidente_id   INT NOT NULL,
  tipo_decl      ENUM('accidentado','testigo') DEFAULT 'testigo',
  nombre         VARCHAR(255),
  rut            VARCHAR(20),
  cargo          VARCHAR(255),
  texto          TEXT,
  CONSTRAINT fk_decl_acc
    FOREIGN KEY (accidente_id) REFERENCES accidentes(accidente_id)
);

/* 10. ADJUNTOS (archivo embebido opcional) */
CREATE TABLE IF NOT EXISTS adjuntos (
  adjunto_id     INT AUTO_INCREMENT PRIMARY KEY,
  accidente_id   INT NOT NULL,
  etiqueta       VARCHAR(255),
  nombre_archivo VARCHAR(255),
  mime_type      VARCHAR(50),
  ruta           VARCHAR(255),                 -- si contenido = NULL
  contenido      MEDIUMBLOB,                   -- binario, opcional
  subido_el      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_adj_acc
    FOREIGN KEY (accidente_id) REFERENCES accidentes(accidente_id)
);

SET FOREIGN_KEY_CHECKS = 1;

ALTER TABLE empresas
  MODIFY holding_id INT NULL;

ALTER TABLE accidentes
  ADD COLUMN contexto            TEXT NULL AFTER perdidas_proceso,
  ADD COLUMN circunstancias      TEXT NULL AFTER contexto,
  ADD COLUMN preinitial_story    TEXT NULL AFTER circunstancias,
  ADD COLUMN preguntas_entrevista TEXT NULL AFTER preinitial_story;




CREATE TABLE IF NOT EXISTS preguntas_guia (
  pregunta_id      INT AUTO_INCREMENT PRIMARY KEY,
  accidente_id     INT NOT NULL,
  uuid             CHAR(36)     NOT NULL,        -- el que genera Streamlit
  categoria        ENUM('accidentado','testigos','supervisores') NOT NULL,
  pregunta         TEXT,
  objetivo         TEXT,
  respuesta        TEXT,                         -- NULL hasta que se conteste
  CONSTRAINT unq_preg_uuid     UNIQUE (accidente_id, uuid),
  CONSTRAINT fk_preg_accidente FOREIGN KEY (accidente_id)
           REFERENCES accidentes(accidente_id) ON DELETE CASCADE
);
# src/db.py
import mysql.connector
from mysql.connector import pooling
import streamlit as st
from contextlib import contextmanager

_pool = pooling.MySQLConnectionPool(
    pool_name="ist_pool", pool_size=5, pool_reset_session=True,
    host=st.secrets["db_host"],
    user=st.secrets["db_user"],
    password=st.secrets["db_password"],
    database=st.secrets["db_name"],
    autocommit=False           # manejaremos transacciones a mano
)

@contextmanager
def get_conn():
    cnx = _pool.get_connection()
    try:
        yield cnx
        cnx.commit()
    except Exception:
        cnx.rollback()
        raise
    finally:
        cnx.close()


def upsert_holding(nombre: str) -> int:
    sql = """
        INSERT INTO holdings (nombre)
        VALUES (%s)
        ON DUPLICATE KEY UPDATE nombre = VALUES(nombre)
    """
    with get_conn() as cnx:
        cur = cnx.cursor()
        cur.execute("SELECT holding_id FROM holdings WHERE nombre = %s", (nombre,))
        row = cur.fetchone()
        if row:
            return row[0]
        cur.execute(sql, (nombre,))
        return cur.lastrowid

def upsert_empresa(holding_id: int, data: dict) -> int:
    sql = """
        INSERT INTO empresas
        (holding_id, empresa_sel, rut_empresa, actividad,
         direccion_empresa, telefono, representante_legal,
         region, comuna)
        VALUES (%(holding_id)s, %(empresa_sel)s, %(rut)s, %(act)s,
                %(dir)s, %(tel)s, %(rep)s, %(reg)s, %(com)s)
        ON DUPLICATE KEY UPDATE
            actividad          = VALUES(actividad),
            direccion_empresa  = VALUES(direccion_empresa),
            telefono           = VALUES(telefono),
            representante_legal= VALUES(representante_legal),
            region             = VALUES(region),
            comuna             = VALUES(comuna)
    """
    with get_conn() as cnx:
        cur = cnx.cursor(buffered=True)   # <- la clave
        cur.execute("SELECT empresa_id FROM empresas WHERE rut_empresa=%s",
                    (data["rut"],))
        row = cur.fetchone()
        if row:
            cur.execute(sql, data)          # para refrescar datos
            return row[0]
        cur.execute(sql, data)
        return cur.lastrowid

# src/db.py  (añade debajo de upsert_empresa)
def upsert_centro_trabajo(empresa_id: int,
                          nombre_local: str,
                          direccion_centro: str | None = None) -> int:
    """Inserta o actualiza un centro de trabajo y devuelve centro_id."""
    sel_sql = """
        SELECT centro_id
          FROM centros_trabajo
         WHERE empresa_id = %s
           AND nombre_local = %s
         LIMIT 1
    """
    ins_sql = """
        INSERT INTO centros_trabajo (empresa_id, nombre_local, direccion_centro)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            direccion_centro = VALUES(direccion_centro)
    """

    with get_conn() as cnx:
        cur = cnx.cursor(buffered=True)   # <- la clave
        cur.execute(sel_sql, (empresa_id, nombre_local))
        row = cur.fetchone()

        if row:
            # Refresca dirección si cambió
            cur.execute(ins_sql, (empresa_id, nombre_local, direccion_centro))
            return row[0]

        cur.execute(ins_sql, (empresa_id, nombre_local, direccion_centro))
        return cur.lastrowid


# src/db.py  (añade debajo de upsert_centro_trabajo)
def upsert_trabajador(empresa_id: int, data: dict) -> int:
    """
    Crea o actualiza datos permanentes del trabajador.
    La clave única es el RUT.
    """
    sql = """
        INSERT INTO trabajadores
        (empresa_id, nombre_trabajador, rut_trabajador,
         fecha_nacimiento, nacionalidad, estado_civil, domicilio)
        VALUES (%(empresa_id)s, %(nombre)s, %(rut)s,
                %(fec_nac)s, %(nac)s, %(estado)s, %(dom)s)
        ON DUPLICATE KEY UPDATE
            empresa_id       = VALUES(empresa_id),
            nombre_trabajador= VALUES(nombre_trabajador),
            fecha_nacimiento = VALUES(fecha_nacimiento),
            nacionalidad     = VALUES(nacionalidad),
            estado_civil     = VALUES(estado_civil),
            domicilio        = VALUES(domicilio)
    """
    with get_conn() as cnx:
        cur = cnx.cursor(buffered=True)  # <- la clave
        cur.execute(
            "SELECT trabajador_id FROM trabajadores WHERE rut_trabajador = %s",
            (data["rut"],),
        )
        row = cur.fetchone()
        if row:
            # Actualiza por si cambió algún dato permanente
            cur.execute(sql, data)
            return row[0]

        cur.execute(sql, data)
        return cur.lastrowid

# src/db.py  (debajo de upsert_trabajador)
def insert_accidente(**kwargs) -> int:
    """
    Inserta un accidente y devuelve accidente_id.
    Todos los campos de kwargs deben coincidir con las columnas de la tabla.
    """
    cols = ", ".join(kwargs.keys())
    ph   = ", ".join(["%({})s".format(k) for k in kwargs.keys()])

    sql = f"INSERT INTO accidentes ({cols}) VALUES ({ph})"
    with get_conn() as cnx:
        cur = cnx.cursor()
        cur.execute(sql, kwargs)
        return cur.lastrowid


def update_accidente(accidente_id: int, **kwargs) -> None:
    """
    Actualiza sólo las columnas pasadas en kwargs para un accidente existente.
    Útil más adelante para guardar `resumen`, `relato`, etc.
    """
    sets = ", ".join([f"{col} = %({col})s" for col in kwargs])
    sql  = f"UPDATE accidentes SET {sets} WHERE accidente_id = %(acc)s"
    kwargs["acc"] = accidente_id

    with get_conn() as cnx:
        cur = cnx.cursor()
        cur.execute(sql, kwargs)


# --- helpers de consulta -------------------------------------------------
def search_accidentes(
    empresa: str | None = None,
    rut_trab: str | None = None,
    fecha_ini: str | None = None,   # 'YYYY-MM-DD'
    fecha_fin: str | None = None,
) -> list[dict]:
    """
    Devuelve una lista de accidentes que cumplan los filtros.
    Se traen también razón social, centro y nombre trabajador
    para mostrar en la tabla de resultados.
    """
    sql = """
        SELECT a.accidente_id, e.empresa_sel, c.nombre_local,
               t.nombre_trabajador, a.fecha_accidente, a.hora_accidente
        FROM   accidentes a
        JOIN   centros_trabajo c ON c.centro_id = a.centro_id
        JOIN   empresas        e ON e.empresa_id = c.empresa_id
        LEFT JOIN trabajadores t ON t.trabajador_id = a.trabajador_id
        WHERE 1=1
    """
    params = {}
    if empresa:
        sql += " AND e.empresa_sel LIKE %(emp)s"
        params["emp"] = f"%{empresa}%"
    if rut_trab:
        sql += " AND t.rut_trabajador LIKE %(rut)s"
        params["rut"] = f"%{rut_trab}%"
    if fecha_ini:
        sql += " AND a.fecha_accidente >= %(fi)s"
        params["fi"] = fecha_ini
    if fecha_fin:
        sql += " AND a.fecha_accidente <= %(ff)s"
        params["ff"] = fecha_fin

    with get_conn() as cnx:
        cur = cnx.cursor(dictionary=True)
        cur.execute(sql, params)
        return cur.fetchall()


def fetch_accidente_full(accidente_id: int) -> dict:
    """
    Devuelve todos los datos necesarios para poblar session_state
    a partir de un accidente existente.
    """
    with get_conn() as cnx:
        cur = cnx.cursor(dictionary=True)

        # Accidente + centro + empresa + trabajador
        cur.execute(
            """
            SELECT a.*, c.*, e.*, t.*
            FROM accidentes a
            JOIN centros_trabajo c ON c.centro_id = a.centro_id
            JOIN empresas        e ON e.empresa_id = c.empresa_id
            LEFT JOIN trabajadores t ON t.trabajador_id = a.trabajador_id
            WHERE a.accidente_id = %s
            """,
            (accidente_id,),
        )
        base = cur.fetchone() or {}

        # Adjuntos, declaraciones, etc. se pueden traer en nuevas consultas
        # (omito para abreviar; añádelas según lo que quieras precargar)

        return base

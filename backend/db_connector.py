"""
Backend DB Connector for ScoutIQ
--------------------------------

Responsibilities:
- Build a SQLAlchemy engine from the DATABASE_URL in .env (fallback provided)
- List public tables
- Reflect ORM classes on demand (schema already exists)
- Fetch a small sample of rows from any public table

This module is intentionally framework-agnostic so it can be imported by
scripts, FastAPI routes, or notebooks.
"""

from __future__ import annotations

import os
from typing import Dict, List, Tuple

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, select, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.ext.automap import automap_base


# --------------------------------------------------------------
# Engine creation
# --------------------------------------------------------------

def get_engine(database_url: str | None = None) -> Engine:
    """Create (or reuse) a SQLAlchemy engine.

    Reads DATABASE_URL from `.env` if not explicitly provided. A sensible local
    default is used if nothing is set.
    """
    load_dotenv()
    url = database_url or os.getenv("DATABASE_URL") or "postgresql://dheeraj@localhost/scoutiq"
    engine = create_engine(url, pool_pre_ping=True, future=True)
    return engine


# --------------------------------------------------------------
# Introspection helpers
# --------------------------------------------------------------

def list_tables(engine: Engine | None = None) -> List[str]:
    """Return a sorted list of public table names.

    Example:
        >>> list_tables()
        ['blackland_capital_group_taxassessor_0001_sample', 'blackland_capital_group_avm_0002', ...]
    """
    engine = engine or get_engine()
    insp = inspect(engine)
    tables = insp.get_table_names(schema="public")
    return sorted(tables)


def reflect_orm(engine: Engine | None = None):
    """Reflect ORM classes for all public tables using Automap.

    Returns a tuple of (Base, classes_mapping) where classes_mapping is a dict
    mapping `table_name -> ORM class`.
    """
    engine = engine or get_engine()
    Base = automap_base()
    Base.prepare(autoload_with=engine, schema="public")

    # Build a name -> class mapping for convenience
    classes: Dict[str, type] = {}
    for attr, cls in vars(Base.classes).items():
        if attr.startswith("_"):
            continue
        try:
            table_name = cls.__table__.name  # type: ignore[attr-defined]
            classes[table_name] = cls
        except Exception:
            # Fallback to attribute name if table not available
            classes[attr] = cls
    return Base, classes


# --------------------------------------------------------------
# Data access
# --------------------------------------------------------------

def get_table_sample(table_name: str, limit: int = 5, engine: Engine | None = None) -> List[dict]:
    """Return a small sample of rows from a given public table.

    Uses SQLAlchemy reflection to safely handle quoted identifiers and
    non-standard column names.
    """
    if not table_name:
        raise ValueError("table_name is required")

    engine = engine or get_engine()
    metadata = MetaData(schema="public")
    table = Table(table_name, metadata, autoload_with=engine, schema="public")
    stmt = select(table).limit(limit)

    with engine.connect() as conn:
        rows = conn.execute(stmt).mappings().all()
        return [dict(r) for r in rows]


# --------------------------------------------------------------
# CLI for quick debugging
# --------------------------------------------------------------

if __name__ == "__main__":
    eng = get_engine()
    print("Connected to:", eng.url)
    print("\nPublic tables:")
    for t in list_tables(eng):
        print(" -", t)
    try:
        tables = list_tables(eng)
        if tables:
            print("\nSample from", tables[0])
            sample = get_table_sample(tables[0], limit=5, engine=eng)
            for row in sample:
                print(row)
    except Exception as e:
        print("Error sampling table:", e)




from sqlalchemy import text

from src.load import get_engine


def save_analysis(filename, total_rows, valid_rows, stats):
    engine = get_engine()

    query = text("""
        INSERT INTO analysis_history (
            filename,
            total_rows,
            valid_rows,
            removed_rows,
            total_revenue,
            average_order,
            products_sold
        )
        VALUES (
            :filename,
            :total_rows,
            :valid_rows,
            :removed_rows,
            :total_revenue,
            :average_order,
            :products_sold
        )
        RETURNING id
    """)

    params = {
        "filename": filename,
        "total_rows": total_rows,
        "valid_rows": valid_rows,
        "removed_rows": total_rows - valid_rows,
        "total_revenue": stats["revenue"],
        "average_order": stats["average_order"],
        "products_sold": stats["products_sold"]
    }

    try:
        with engine.begin() as connection:
            result = connection.execute(query, params)
            return result.scalar_one()
    finally:
        engine.dispose()


def get_analysis_history():
    engine = get_engine()

    query = text("""
        SELECT
            id,
            filename,
            analyzed_at,
            total_rows,
            valid_rows,
            removed_rows,
            total_revenue,
            average_order,
            products_sold
        FROM analysis_history
        ORDER BY analyzed_at DESC, id DESC
    """)

    try:
        with engine.connect() as connection:
            rows = connection.execute(query).mappings().all()
            return [dict(row) for row in rows]
    finally:
        engine.dispose()

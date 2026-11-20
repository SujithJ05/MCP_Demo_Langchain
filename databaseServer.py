import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from mcp.server.fastmcp import FastMCP

load_dotenv() # loads the environment variables from .env file

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)

mcp = FastMCP("Database")

@mcp.tool()
def get_employee_count() -> int:
    """Get the total number of employees."""

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT COUNT(*) FROM employees")
        )

        return result.scalar()

@mcp.tool()
def get_all_employees() -> list:
    """Get details of all employees."""
    with engine.connect() as connection:
        result = connection.execute(
            text("""
                SELECT employee_id, employee_name,
                       department, designation, status
                FROM employees
                ORDER BY employee_id
            """)
        )
        return [dict(row) for row in result.mappings()]


if __name__ == "__main__":
    mcp.run(transport="stdio")
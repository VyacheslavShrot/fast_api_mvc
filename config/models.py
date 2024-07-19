from sqlalchemy import Table, Column, Integer, String, MetaData

metadata: MetaData = MetaData()

"""
            Models
"""
users: Table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("email", String(50), unique=True),
    Column("password", String(50)),
)

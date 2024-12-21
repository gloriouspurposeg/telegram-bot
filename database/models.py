import os
from dotenv import load_dotenv
from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

load_dotenv()
engine = create_async_engine(url=os.getenv('DB_URL'))

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column(String(50))
    referals_count: Mapped[int] = mapped_column(BigInteger)
    refer_id = mapped_column(BigInteger)


class Admin(Base):
    __tablename__ = 'admins'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id = mapped_column(BigInteger)

class Channel(Base):
    __tablename__ = 'channels'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    link: Mapped[str] = mapped_column(String(50))
    chat_id = mapped_column(BigInteger)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
from .session import engine, session
from .models import Base, ParserData
from sqlalchemy import inspect, update, select, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import InterfaceError


def create_tables_if_not_exist():
    with engine.begin() as conn:
        inspector = inspect(engine)
        if not inspector.get_table_names():
            Base.metadata.create_all(conn)
        

def drop_tables():
    with engine.begin() as conn:
        Base.metadata.drop_all(conn)
        
def add_post(url, header, text, theme=None, author=None, date=None):
    try:
        with Session(engine) as session:
            session.add(
                ParserData(
                    url=url,
                    theme=theme,
                    header=header,
                    text=text,
                    author=author,
                    date=date
                )
            )
            session.commit()
    except InterfaceError:
        pass
        
def update_post_by_url(url, data):
    with Session(engine) as session:
        stmt = (
            update(ParserData)
            .where(ParserData.url == url)
            .values(
                url=url,
                theme=data["theme"],
                header=data["header"],
                text=data["text"],
                author=data["author"],
                date=None # ! Временно
            )
        )
        session.execute(stmt)
        session.commit()
        
def select_post_by_theme(theme: str):
    with Session(engine) as session:
        stmt = (
            select(ParserData.header, ParserData.url)
            .where(ParserData.theme == theme)
        )
        result = session.execute(stmt)
        return result.all()
    
def delete_post_by_url(url: str):
    with Session(engine) as session:
        session.execute(
            delete(ParserData)
            .where(ParserData.url == url)
        )
        session.commit()

def get_last_date_post():
    pass


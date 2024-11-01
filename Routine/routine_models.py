from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm import sessionmaker

connection_str = "sqlite:///data230.db"
engine = create_engine(connection_str)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Activity(Base) :
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_id = Column(Text)
    routin = Column(Text)
    status = Column(Boolean, default=False)

    def save(self):
        session.add(self)
        session.commit()

    @classmethod
    def read(cls, user_id):
        veiw_list = session.query(cls).filter_by(user_id=user_id).all()
        return veiw_list
    
    @classmethod
    def delete(cls, id):
        data = session.query(cls).filter_by(id=id).first()
        session.delete(data)
        session.commit()
        
    @classmethod
    def update(cls, text, id):
        data = session.query(cls).filter_by(id=id).first()
        data.routin = text
        session.commit()

    @classmethod
    def change_status(cls, id, status = True):
        data = session.query(cls).filter_by(id=id).first()
        data.status = status
        session.commit()

    @classmethod
    def reset_all_status(cls):
        data = session.query(cls).filter_by().all()
        for user_status in data:
            user_status.status = False
        session.commit()

Base.metadata.create_all(engine)









        




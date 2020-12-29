from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
from sqlalchemy.orm import relationship

from resources import Base

from resources.Exceptions import AttributeException

from resources.Mixins import MixinsTables,MixinsTablesMeasurements


class Transformer(Base, MixinsTables):
    __tablename__="transformer"
    __table_args__ ={"schema": "ges_ativos"}

    id_transformer  = Column(Text, primary_key=True)
    age             = Column(Integer)
    nominal_voltage = Column(Float)

    weights = relationship('Weights', back_populates='transformer')
    furfural = relationship("Furfural", back_populates="transformer")
    load = relationship("Load", back_populates="transformer")
    oil_quality = relationship("Oil_Quality", back_populates="transformer")
    dissolved_gases = relationship("Dissolved_Gases", back_populates="transformer")

    def __init__(self, **kwargs):
        MixinsTables.__init__(self, **kwargs)

    def get_measurements(self, session, table):
        self=self.get(session)
        
        relationships=self.__mapper__.relationships
        for relation in relationships:
            clsname = relation.entity.class_.__name__
            if clsname == table and clsname != 'Weights':
                key = relation.key
                break
        
        if 'key' in locals():
            return getattr(self,key)
        else:
            pass # raise error ....... table does not exist

    def get_all_measurements(self, session):
        self=self.get(session)
        relationships=self.__mapper__.relationships
        res={}
        for relation in relationships:
            clsname = relation.entity.class_.__name__
            key = relation.key
            if clsname == 'Weights':
                continue
            res[clsname] = getattr(self,key) 
        return res

    def get_by_time_interval(self, session, **kwargs):
        
        self=self.get(session)
        relationships=self.__mapper__.relationships
        res={}
        
        for relation in relationships:
            Table = relation.entity.class_
            if Table.__name__ == 'Weights':
                continue
            
            query = session.query(Table).filter(Table.id_transformer == self.id_transformer)

            for key, value in kwargs.items():
                if key == 'mindate':
                    query=query.filter(Table.datestamp>=value)
                elif key == 'maxdate':
                    query=query.filter(Table.datestamp<=value)

            res[Table.__name__] = query 
        
        return res

    def get_by_interval(self, session, listkwargs):
        
        self=self.get(session)
        relationships=self.__mapper__.relationships
        relationship_names=[relation.entity.class_.__name__ for relation in relationships]
        relationship_names.remove('Weights')
        
        res={}
        
        for relation in relationships:
            
            Table = relation.entity.class_
            if Table.__name__ == 'Weights':
                continue

            col_names = [col.name for col in Table.__table__.columns]
            
            query = session.query(Table).filter(Table.id_transformer == self.id_transformer)
            
            for kwargs in listkwargs:
                column = None
                for key, value in kwargs.items():
                    if key == 'column':
                        if value in col_names:
                            column = value
                        else:
                            break
                    if key == 'min' and column != None:
                        query=query.filter(getattr(Table,column)>=value)
                    elif key == 'max' and column != None:
                        query=query.filter(getattr(Table,column)<=value)

            res[Table.__name__] = query 
        
        return res

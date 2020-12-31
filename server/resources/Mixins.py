from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, Date

class MixinsTables:

    def __init__(self, **kwargs):
        """ 
        Ex:
            tr = Transformer(id_transformer="SE1", age=20)

        Descrição:
            Este método cria instâncias de classes que tenham herdado do MixinsTables

        Inputs:
            self - objeto que chama o metodo
            kwargs - keyword arguments que caracterizam cada atributo do objeto
        Outputs:
            None

        Exceptions (não tem em conta exceções geradas por outros métodos):
            AttributeException - No caso de serem fornecidos atributos que nao tenham o mesmo nome de uma coluna da tabela da classe.
        """
        col_names = [col.name for col in self.__table__.columns]
        for key, value in kwargs.items():
            if key in col_names:
                print(key,value)
                setattr(self, key, value)
            else:
                raise AttributeException()


    def get(self, session):
        """ 
        Ex:
            tr = Transformer(id_transformer="SE1")
            tr = tr.get(session)

        Descrição:
            Através da primary definida no objeto (self) é retornado o objeto que esta a ser tracked pelo session.

        Inputs:
            self - objeto que chama o metodo
            session - objeto de Session que relaciona o objeto python com os objetos da base de dados
        Outputs:
            O objeto que esta a ser "tracked" por session

        Exceptions (não tem em conta exceções geradas por outros métodos):

        """
        pks = [c.name for c in self.__table__.primary_key.columns]
        attr = tuple(getattr(self, pk) for pk in pks)
        try:
            return session.query(self.__class__).get(attr)
        except Exception as e:
            session.rollback()
            raise e

    def add(self, session):
        """ 
        Ex:
            tr = Transformer(id_transformer="SE1", age=50)
            tr.add(session)

        Descrição:
            Este metodo adiciona o objeto que chama o metodo 

        Inputs:
            self - objeto que chama o metodo
            session - objeto de Session que relaciona o objeto python com os objetos da base de dados
        Outputs:
            None            

        Exceptions (não tem em conta exceções geradas por outros métodos):

        """
        session.add(self)
        try:
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            error = str(e.__dict__['orig'])
            return error
        except Exception as e:
            session.rollback()
            return str(e)

    def update(self, session):
        """ 
        Ex:
            tr = Transformer(id_transformer="SE1", age=20)
            tr.update(session)

        Descrição:
            Este metodo pesquisa o objeto pelo seu primary key, e os atributos que sejam diferentes de None serão alterados nos objetos da base de dados

        Inputs:
            self - objeto que chama o metodo
            session - objeto de Session que relaciona o objeto python com os objetos da base de dados
        Outputs:
            None            

        Exceptions (não tem em conta exceções geradas por outros métodos):

        """
        pks = [c.name for c in self.__table__.primary_key.columns]
        attr = {pk: getattr(self, pk) for pk in pks}
        aux = self.__class__(**attr)
        try:
            aux = aux.get(session)
            for col in self.__table__.columns: 
                if getattr(self, col.name) != None:
                    setattr(aux, col.name, getattr(self, col.name))
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def delete(self, session):
        """ 
        Ex:
            tr = Transformer(id_transformer="SE1")
            tr.delete(session)

        Descrição:
            Este metodo pesquisa o objeto pelo seu primary key, e remove-o da base de dados

        Inputs:
            self - objeto que chama o metodo
            session - objeto de Session que relaciona o objeto python com os objetos da base de dados
        Outputs:
            None            

        Exceptions (não tem em conta exceções geradas por outros métodos):

        Partes a Implementar:
            caso se pretenda apagar um atributo de um objeto
        """
        self = self.get(session)
        session.delete(self)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e 


    def get_batch(self, session):
        """ 
        Ex:
            tr = Transformer(age=50)
            objs = tr.get_batch(session)

        Descrição:
            Este metodo pesquisa os objetos que tenham os atributos do objeto self criado, e retorna-os numa lista
            No caso do exemplo ilustrado, pesquisa os transformadores que tenham age==50 

        Inputs:
            self - objeto que chama o metodo
            session - objeto de Session
        Outputs:
            lista com objetos com os atributos de self

        Exceptions (não tem em conta exceções geradas por outros métodos):

        """
        try:
            return session.query(self.__class__).filter(*[getattr(self.__class__, col.name) == getattr(self, col.name) 
                                                            for col in self.__table__.columns 
                                                            if getattr(self, col.name) != None
                                                         ]).all()
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def add_batch(cls, session, obj_list):
        """ 
        Ex:
            objs = [Transformer(id_transformer="SE1"), Furfural(id_transformer="SE1"), Oil_Quality(id_transformer="SE1")]
            objs = tr.add_batch(session)

        Descrição:
            Este metodo adiciona todos os objetos que estejam dentro da lista obj_list às suas respetivas tabelas na base de dados

        Inputs:
            cls - Classe MixinsTables que chama este metodo
            session - objeto de Session
            obj_list - lista com os objetos a serem acrescentados à base de dados
        Outputs:
            None

        Exceptions (não tem em conta exceções geradas por outros métodos):

        """
        session.bulk_save_objects(obj_list)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
    
    @classmethod
    def delete_batch(cls, session, obj_list):
        """ 
        Ex:
            objs = [Transformer(id_transformer="SE1"), Furfural(id_transformer="SE1"), Oil_Quality(id_transformer="SE1")]
            objs = tr.add_batch(session)

        Descrição:
            Este metodo pesquisa cada obj (através da sua primary key) que esteja na lista obj_list e apaga-os da base de dados

        Inputs:
            cls - Classe MixinsTables que chama este metodo
            session - objeto de Session
            obj_list - lista com os objetos a serem apagados
        Outputs:
            None

        Exceptions (não tem em conta exceções geradas por outros métodos):

        """
        for obj in obj_list:
            obj = obj.get(session)
            session.delete(obj)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    @classmethod
    def delete_all(cls, session):
        for subcls in cls.__subclasses__():
            session.query(subcls).delete()
        session.commit()


class MixinsTablesMeasurements:
    datestamp = Column(Date)
    

    


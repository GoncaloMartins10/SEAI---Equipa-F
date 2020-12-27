MixinsTabelasGerais:
------------------------------
GET
obj = Class(pk=x)
get(session)
------------------------------

------------------------------
ADD
obj = Class(arg1=x1, arg2=x2, ...)
obj.add(session)
------------------------------

------------------------------
UPDATE
obj = Class(pk=x1, arg1=x2, arg2='delete', ...)
obj.update(session)
------------------------------

------------------------------
DELETE
obj = Class(pk=x1)
obj.delete(session)
------------------------------

------------------------------
GET BATCH
obj = Class(arg1=x1, arg2=x2, ...)
obj.get_batch()
------------------------------

------------------------------
UPDATE BATCH
search_obj = Class(arg1=x1, arg2=x2, ...)
change_obj = Class(arg3=x3, arg4=x4)
search_obj.update_batch(session, change_attr=change_obj)
------------------------------

------------------------------
DELETE BATCH
obj = Class(arg1=x1, arg2=x2, ...)
search_obj.update_batch(session, change_attr=change_obj)
------------------------------


MixinsMeasurements:

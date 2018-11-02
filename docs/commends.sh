# this is my notes, sixing

python3 swagger2marshmallow.py /Users/alfonso/workplace/moretime/docs/api.yaml -o /Users/alfonso/workplace/moretime/api/schema.py


python3 db2model.py > /Users/alfonso/workplace/moretime/orm/orm_mysql.py


python3 error2py.py


# 打log
from api.wapp import logworker
logworker.info(data)



GET方法
curl http://127.0.0.1:5000/v1/user/test\?nosig=1


POST方法
curl -H "Content-Type:application/json" -X POST -d '{"user_id": 5555, "nickname":"aa"}' http://127.0.0.1:8998/v1/user/test\?nosig=1
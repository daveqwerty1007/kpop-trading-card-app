from pydantic import BaseModel


# 定义一个Pydantic模型
class User(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# 创建一个字典
user_data = {'id': None, 'name': 'Alice'}

# 使用**操作符将字典解包作为参数传递给User模型
user = User(**user_data)

print(user)  # 输出: id=1 name='Alice'
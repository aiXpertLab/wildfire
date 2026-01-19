from app.main import create_app
app = create_app()  #Dependency injection



# 这里现在只做一件事：启动应用。

# ✔ asgi.py 里 不再出现 Settings / settings
# ✔ main.py 是唯一“消费配置”的地方
# ✔ config.py 是唯一“构造配置”的地方
# ✔ settings 这个名字只在函数内部存在
# ✔ singleton 规则被代码结构强制执行
# nohup uvicorn asgi:app --host 0.0.0.0 --port 8008 > uvicorn.log 2>&1 &
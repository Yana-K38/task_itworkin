# #!/bin/bash

# alembic -c /sm_app/simple_messager/alembic.ini upgrade head

# gunicorn simple_messager.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

#!/bin/bash

# Устанавливаем значение MIGRATIONS_DIR
MIGRATIONS_DIR="/simple_massage/"

# Применяем миграции с помощью Alembic
alembic -c /sm_app/simple_messager/alembic.ini -x migrations_dir=$MIGRATIONS_DIR upgrade head

# Запускаем Gunicorn
gunicorn simple_messager.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
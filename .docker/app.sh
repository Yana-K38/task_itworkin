# #!/bin/bash

# alembic -c /sm_app/simple_messager/alembic.ini upgrade head

# gunicorn simple_messager.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

#!/bin/bash

alembic upgrade head

gunicorn simple_messager.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
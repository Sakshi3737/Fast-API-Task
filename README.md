SET : DATABASE_URL=postgresql://user:pass@localhost:5432/mydb in .env. 
INSTALL :- pip install -r requirements.txt
tart: uvicorn main:app -- reload

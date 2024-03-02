# openai_assistant

## Env setup 
Create a .env file in manage.py directory

## Setup
1. Fork Repo
2. Install requirements

```bash
pip install -r requirements.txt
```

3. Run Migration

```bash
python manage.py migrate
```

4. Run Server

```bash
python manage.py runserver 0.0.0.0:8000
```
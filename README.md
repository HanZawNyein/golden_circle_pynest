# create a project
```zsh
pynest create-nest-app -n <MyAppName> -db postgresql --is-async
```

# create a module
```zsh
pynest g module -n <ModuleName>
```

# PyNest service

This is a template for a PyNest service.

## Start Service

## Step 1 - Create environment

- install requirements:

```bash
pip install -r requirements.txt
```

## Step 2 - start service local

1. Run service with main method

```bash
python main.py
```

2. Run service using uvicorn

```bash
uvicorn "app:app" --host "0.0.0.0" --port "8000" --reload
```

## Step 3 - Send requests

Go to the fastapi docs and use your api endpoints - http://127.0.0.1/docs

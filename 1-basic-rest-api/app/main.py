from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello"}


@app.get("/send_email")
def trigger_email():
    from app.tasks.email_task import send_email

    send_email.delay("recipient@example.com", "Test Subject", "This is a test email.")
    return {"message": "Email task has been triggered."}

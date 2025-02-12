import modal
# using containers
image = (
    modal.Image.debian_slim()
    .apt_install(
        "build-essential", 
        "python3-dev",  
    )
    .pip_install(
        "fastapi[standard]", 
        "uvicorn",
        "pydantic",
    )
)


app = modal.App(name="example-lifecycle-web", image=image)
# using web endpoints
@app.function()
@modal.web_endpoint(docs=True)
def greet(user: str = "World") -> str:
    
    return f"Hello {user}!"

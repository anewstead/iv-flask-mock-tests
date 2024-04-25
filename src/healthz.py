from .app import app


# make a healthz route
@app.route("/healthz")
def healthz():
    return "ok"

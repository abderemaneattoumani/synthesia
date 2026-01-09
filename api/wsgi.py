from index import app

# Export WSGI pour compatibilité
application = app

if __name__ == "__main__":
    app.run()
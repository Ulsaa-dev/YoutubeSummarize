from summarizer import app

if __name__ == '__main__':
    from waitress import serve
    print("Serving on port 8080")
    serve(app, host="0.0.0.0", port=8080)
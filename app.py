from flask import Flask , render_template

app = Flask(__name__)

@app.route("/")
def load_home():
    return render_template("index.html")

@app.route("/maint")
def load_main_template():
      return render_template("main_template.html")

if __name__ == "__main__":
        app.run()
from ucuzpisir import app

app.config["DATABASE_URI"] = "host='localhost' dbname='ucuzdb' user='postgres' password='.abc020615'"

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, Response
import json
import mysql.connector

app = Flask(__name__)

@app.route('/kenttä/<icaokoodi>')
def lentokentta(icaokoodi):
    try:
        yhteys = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            database='flight_game',
            user='lukashe',
            password='JhTaS87526',
            autocommit=True
        )

        kursori = yhteys.cursor()
        kursori.execute("SELECT ident, name, municipality FROM airport WHERE ident = %s", (icaokoodi,))
        lentokentta = kursori.fetchone()

        if lentokentta:
            tilakoodi = 200
            vastaus = {
                "ICAO": lentokentta[0],
                "Name": lentokentta[1],
                "Municipality": lentokentta[2]
            }
        else:
            tilakoodi = 404
            vastaus = {
                "status": tilakoodi,
                "teksti": "Lentokenttää ei löytynyt"
            }

    except mysql.connector.Error as e:
        tilakoodi = 500
        vastaus = {
            "status": tilakoodi,
            "teksti": f"Virhe tietokantayhteydessä: {str(e)}"
        }

    finally:
        if 'kursori' in locals():
            kursori.close()
        if 'yhteys' in locals():
            yhteys.close()

    jsonvast = json.dumps(vastaus)
    return Response(response=jsonvast, status=tilakoodi, mimetype="application/json")

@app.errorhandler(404)
def pagenot_found(virhekoodi):
    vastaus = {
        "status": 404,
        "teksti": "Virheellinen päätepiste"
    }
    jsonvast = json.dumps(vastaus)
    return Response(response=jsonvast, status=404, mimetype="application/json")

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
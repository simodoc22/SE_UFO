from database.DB_connect import DBConnect
from model.sighting import Sighting
from model.state import State
class DAO:
    @staticmethod
    def read_sighting():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM sighting """

        cursor.execute(query)

        for row in cursor:
            oggetto = Sighting(row["id"], row["s_datetime"], row["city"], row["state"], row["country"], row["shape"],
                               row["duration"], row["latitude"], row["longitude"])
            result.append(oggetto)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_state():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM state """

        cursor.execute(query)

        for row in cursor:
            oggetto = State(row["id"], row["name"], row["lat"], row["lng"], row["neighbors"])

            result.append(oggetto)

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def read_neighbors():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM neighbor"""
        cursor.execute(query)
        for row in cursor:
            result.append((row["state1"],row["state2"]))
        cursor.close()
        conn.close()
        return result
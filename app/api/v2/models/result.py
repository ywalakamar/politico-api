from app.api.v2.db import db


class Result:
    """ The candidate model """

    def __init__(self):
        self.db = db()

    def get(self, id):
        query = """SELECT offices.name, users.firstname, COUNT(*) as votes FROM votes
                   INNER JOIN offices ON offices.id=votes.office
                   INNER JOIN users ON users.id=votes.candidate WHERE office={}
                   GROUP BY offices.name, users.firstname;""".format(id)
        cursor = self.db.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        rows = []
        for i, items in enumerate(data):
            office, candidate, results = items
            result = dict(
                office=office,
                candidate=candidate,
                results=results
            )
            rows.append(result)

        return rows

    def search(self, office):
        """ This function returns True if a user is already voted"""
        cursor = self.db.cursor()
        cursor.execute(
            """SELECT * FROM offices WHERE id={}""".format(office))
        # cursor.execute(search('votes', createdby))
        data = cursor.fetchall()  # tuple
        if len(data) > 0:
            return True

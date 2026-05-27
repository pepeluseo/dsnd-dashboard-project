from employee_events.query_base import QueryBase


class Team(QueryBase):
    """
    Query class for team-level data.
    """
    
    name = "team"

    def names(self):
        """
        Return all teams with their names.
        """
        sql = """
            SELECT
                team_id,
                team_name
            FROM team
            ORDER BY team_name;
        """
        return self.query(sql)

    def event_counts(self, entity_id):
        """
        Return daily aggregated positive and negative event counts for one team.
        """
        sql = """
            SELECT
                event_date,
                SUM(positive_events) AS positive_events,
                SUM(negative_events) AS negative_events
            FROM employee_events
            WHERE team_id = ?
            GROUP BY event_date
            ORDER BY event_date;
        """
        return self.query(sql, params=(entity_id,))

    def members(self, entity_id):
        """
        Return employees belonging to one team.
        """
        sql = """
            SELECT
                employee_id,
                first_name || ' ' || last_name AS employee_name,
                team_id
            FROM employee
            WHERE team_id = ?
            ORDER BY employee_name;
        """
        return self.query(sql, params=(entity_id,))

    def notes(self, entity_id):
        """
        Return notes for one team.
        """
        sql = """
            SELECT
                note_date,
                note
            FROM notes
            WHERE team_id = ?
            ORDER BY note_date DESC;
        """
        return self.query(sql, params=(entity_id,))

    def model_data(self, entity_id):
        """
        Return model input data for one team.

        The model receives aggregated productivity values.
        """
        sql = """
            SELECT
                SUM(positive_events) AS positive_events,
                SUM(negative_events) AS negative_events
            FROM employee_events
            WHERE team_id = ?;
        """
        return self.query(sql, params=(entity_id,))
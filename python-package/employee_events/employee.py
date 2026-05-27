from employee_events.query_base import QueryBase


class Employee(QueryBase):
    """
    Query class for employee-level data.
    """

    name = "employee"

    def names(self):
        """
        Return all employees with their full names.
        """
        query = """
            SELECT
                employee_id,
                first_name || ' ' || last_name AS employee_name
            FROM employee
            ORDER BY employee_name;
        """
        return self.query(query)

    def event_counts(self, entity_id):
        """
        Return daily positive and negative event counts for one employee.
        """
        query = """
            SELECT
                event_date,
                positive_events,
                negative_events
            FROM employee_events
            WHERE employee_id = ?
            ORDER BY event_date;
        """
        return self.query(query, params=(entity_id,))

    def notes(self, entity_id):
        """
        Return notes for one employee.
        """
        query = """
            SELECT
                note_date,
                note
            FROM notes
            WHERE employee_id = ?
            ORDER BY note_date DESC;
        """
        return self.query(query, params=(entity_id,))

    def model_data(self, entity_id):
        """
        Return model input data for one employee.

        The model receives aggregated productivity values.
        """
        query = """
            SELECT
                SUM(positive_events) AS positive_events,
                SUM(negative_events) AS negative_events
            FROM employee_events
            WHERE employee_id = ?;
        """
        return self.query(query, params=(entity_id,))
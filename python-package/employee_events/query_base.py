from employee_events.sql_execution import SQLExecutionMixin


class QueryBase(SQLExecutionMixin):
    """
    Base query class with queries shared by Employee and Team.
    """

    def employees(self):
        """
        Return all employees.
        """
        sql = """
            SELECT
                employee_id,
                first_name,
                last_name,
                team_id,
                first_name || ' ' || last_name AS employee_name
            FROM employee
            ORDER BY last_name, first_name;
        """
        return self.query(sql)

    def teams(self):
        """
        Return all teams.
        """
        sql = """
            SELECT
                team_id,
                team_name,
                shift,
                manager_name
            FROM team
            ORDER BY team_name;
        """
        return self.query(sql)

    def employee_name(self, entity_id):
        """
        Return the full name of one employee.
        """
        sql = """
            SELECT
                employee_id,
                first_name || ' ' || last_name AS employee_name
            FROM employee
            WHERE employee_id = ?;
        """
        return self.query(sql, params=(entity_id,))

    def team_name(self, entity_id):
        """
        Return the name of one team.
        """
        sql = """
            SELECT
                team_id,
                team_name
            FROM team
            WHERE team_id = ?;
        """
        return self.query(sql, params=(entity_id,))
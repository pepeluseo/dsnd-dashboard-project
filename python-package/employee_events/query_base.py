<<<<<<< HEAD
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
=======
# Import any dependencies needed to execute sql queries
# YOUR CODE HERE

# Define a class called QueryBase
# Use inheritance to add methods
# for querying the employee_events database.
# YOUR CODE HERE

    # Create a class attribute called `name`
    # set the attribute to an empty string
    # YOUR CODE HERE

    # Define a `names` method that receives
    # no passed arguments
    # YOUR CODE HERE
        
        # Return an empty list
        # YOUR CODE HERE


    # Define an `event_counts` method
    # that receives an `id` argument
    # This method should return a pandas dataframe
    # YOUR CODE HERE

        # QUERY 1
        # Write an SQL query that groups by `event_date`
        # and sums the number of positive and negative events
        # Use f-string formatting to set the FROM {table}
        # to the `name` class attribute
        # Use f-string formatting to set the name
        # of id columns used for joining
        # order by the event_date column
        # YOUR CODE HERE
            
    

    # Define a `notes` method that receives an id argument
    # This function should return a pandas dataframe
    # YOUR CODE HERE

        # QUERY 2
        # Write an SQL query that returns `note_date`, and `note`
        # from the `notes` table
        # Set the joined table names and id columns
        # with f-string formatting
        # so the query returns the notes
        # for the table name in the `name` class attribute
        # YOUR CODE HERE

>>>>>>> 0f6de772d3af8da6c9332debada6f5aff23871b2

from orator.migrations import Migration


class CreateEmployeesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('employees') as table:
            table.string('id').unique()
            table.string('name')

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('employees')

from orator.migrations import Migration


class CreateMeetingRoomsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('meeting_rooms') as table:
            table.string('id').unique()
            table.string('name')

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('meeting_rooms')

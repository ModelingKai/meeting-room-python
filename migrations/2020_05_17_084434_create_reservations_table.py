from orator.migrations import Migration


class CreateReservationsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('reservations') as table:
            table.string('id').unique()
            table.string('meeting_room_id')
            table.string('reserver_id')
            table.enum('reservation_status', ['予約中', 'キャンセル済み'])
            table.integer('number_of_participants')
            table.datetime('start_datetime')
            table.datetime('end_datetime')

            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('reservations')

"""
create table wishes
date created: 2021-10-25 20:56:05.233739
"""


def upgrade(migrator):
    with migrator.create_table('wishes') as table:
        table.primary_key('id')


def downgrade(migrator):
    migrator.drop_table('wishes')

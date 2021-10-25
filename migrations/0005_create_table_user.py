"""
create table user
date created: 2021-10-25 20:56:05.231738
"""


def upgrade(migrator):
    with migrator.create_table('user') as table:
        table.primary_key('id')


def downgrade(migrator):
    migrator.drop_table('user')

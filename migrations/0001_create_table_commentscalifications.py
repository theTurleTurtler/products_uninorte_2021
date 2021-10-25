"""
create table commentscalifications
date created: 2021-10-25 20:56:05.222737
"""


def upgrade(migrator):
    with migrator.create_table('commentscalifications') as table:
        table.primary_key('id')


def downgrade(migrator):
    migrator.drop_table('commentscalifications')

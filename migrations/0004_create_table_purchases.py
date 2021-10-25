"""
create table purchases
date created: 2021-10-25 20:56:05.228739
"""


def upgrade(migrator):
    with migrator.create_table('purchases') as table:
        table.primary_key('id')


def downgrade(migrator):
    migrator.drop_table('purchases')

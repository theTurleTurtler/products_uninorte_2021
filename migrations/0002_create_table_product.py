"""
create table product
date created: 2021-10-25 20:56:05.224737
"""


def upgrade(migrator):
    with migrator.create_table('product') as table:
        table.primary_key('id')


def downgrade(migrator):
    migrator.drop_table('product')

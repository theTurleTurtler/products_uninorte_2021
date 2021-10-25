"""
create table purchasedproducts
date created: 2021-10-25 20:56:05.226738
"""


def upgrade(migrator):
    with migrator.create_table('purchasedproducts') as table:
        table.primary_key('id')


def downgrade(migrator):
    migrator.drop_table('purchasedproducts')

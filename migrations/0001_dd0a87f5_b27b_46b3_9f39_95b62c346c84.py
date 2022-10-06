"""
dd0a87f5_b27b_46b3_9f39_95b62c346c84
date created: 2022-10-06 04:57:48.985336
"""


def upgrade(migrator):
    with migrator.create_table('settings') as table:
        table.primary_key('id')
        table.char('type')
        table.char('name')
        table.char('view_name')
        table.text('value')

    migrator.execute_sql(
        """
            INSERT INTO settings(type, name, view_name, value)
            VALUES  ('bool','repeat', 'Повторять отправку файлов', 'true'),
                    ('text','wellcome_message', 'Приветственное сообщение', 'Привет');
        """
    )

    with migrator.create_table('users') as table:
        table.primary_key('id')
        table.integer('user_id')
        table.text('file', null=True)
        table.datetime('date_join')

    migrator.execute_sql(
        """
            ALTER TABLE users
            ADD COLUMN 'repeat' BOOLEAN DEFAULT TRUE; 
        """
    )


def downgrade(migrator):
    migrator.drop_table('settings')
    migrator.drop_table('users')

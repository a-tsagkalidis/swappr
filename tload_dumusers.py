import json
from fhelpers import cursor_execute
from fSQL import create_database_tables

create_database_tables()

with open('tdumusers.json', 'r') as json_file:
    users = json.load(json_file)

    query = '''
            INSERT INTO users (
                id,
                username,
                email,
                hash,
                registration_date,
                verified_account
            )
            VALUES (?, ?, ?, ?, ?, ?);
            '''

    for user in users:
        cursor_execute(
            query,
            user['user_id'],
            user['username'],
            user['email'],
            'scrypt:32768:8:1$qICfKjC9CagbVSrn$efd605af1c704a9ba1ac242acad6e8a49d7568d60aa9028e54271d94a69ecc0ebfa75a56c9278a48db227e1b685337bba53c1170a5b6016ba7336083a8bd259c',
            '2024-02-03 09:38:41.231061',
            0
        )

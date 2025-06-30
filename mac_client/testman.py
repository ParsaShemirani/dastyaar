

import sqliteinterface as db

result = db.execute_read(
    database_path={database_path},
    query={query},
    params={params},
    fetch_one={fetch_one}
)
print(result)
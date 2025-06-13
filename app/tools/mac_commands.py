from app.tools import sqlqueries
from app.tools import sqlgroupings
import os
import shutil
def localize_grouping(grouping_id):

    grouping_name = sqlgroupings.get_grouping_name_via_id(
        grouping_id=grouping_id
    )
    
    directory = f"/Users/parsashemirani/main/ingested/{grouping_name}"

    os.makedirs(directory)


    id_list = sqlqueries.ids_in_grouping(
        grouping_id=grouping_id
    )
    print(id_list)
    for id in id_list:
        file_name = sqlqueries.get_file_name_via_id(
            file_id=id
        )
        source = f"/Users/parsashemirani/Main/revampbase/{file_name}"
        destination = f"/Users/parsashemirani/main/ingested/{grouping_name}/{file_name}"
        shutil.copy2(source, destination)

    print("Copy complete")


"""
from app.tools.mac_commands import localize_grouping as lg
"""
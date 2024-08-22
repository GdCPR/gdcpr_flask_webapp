from helpers.manager_db import DBManager

dbmanager = DBManager()

locationObj = dbmanager.get_location_object()

for loc in locationObj:
    print(loc)
    for key, value in loc.items():
        if key == "NormalizedName":
            normalized_name = loc[key].split("_")
            class_normalized_name = ("-").join(normalized_name)
            # print(class_normalized_name)
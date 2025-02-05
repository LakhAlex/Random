import os

current_dir = os.path.dirname(os.path.abspath(__file__))

def save_to_file(file_name, jobs):
    file_path = os.path.join(current_dir, f"{file_name}.csv")
    # file = open(f"{file_name}.csv", "w", encoding="utf-8", newline='')
    file = open(file_path, "w", encoding="utf-8", newline='')
    file.write(f"Title,Company,Location,Pay,URL\n")

    for job in jobs:
        file.write(
            f"{job['title']},{job['company']},{job['location']},{job['pay']},{job['link']}/n"
        )
    
    file.close()
    
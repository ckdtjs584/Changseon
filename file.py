
def save_to_file(file_name, jobs):
    file = open(f"{file_name}.csv", "w", encoding='utf-8')
    file.write("job, comany, URL\n")

    for job in jobs:
        file.write(f"{job['job_name']}, {job['company']}, {job['link']}\n")
    file.close()
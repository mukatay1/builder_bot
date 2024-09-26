from config import STATUS


def calculate_completion_percentage(apartments):
    completed_counts = {status: 0 for status in STATUS}

    for apartment in apartments:
        current_status = apartment.status
        if current_status in STATUS:
            current_status_index = STATUS.index(current_status)
            for i in range(current_status_index + 1):
                completed_counts[STATUS[i]] += 1

    total_apartments = len(apartments)
    completion_percentage = {status: (count / total_apartments) * 100 if total_apartments > 0 else 0
                             for status, count in completed_counts.items()}

    return completion_percentage
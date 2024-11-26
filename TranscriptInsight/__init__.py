from functools import lru_cache
# TODO: Add you transcript file path so it can send across to get the transcript Insight 

@lru_cache
def get_transcript():
    # Read the transcript file
    try:
        with open('transcript.txt', 'r') as file:
            data = file.read().replace('\n', '')
            return data
    except Exception as e:
        print(f"Error reading transcript file: {e}")
        return None
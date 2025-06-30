import re

def summarize_log(file_path):
    summary = {
        'errors': [],
        'warnings': [],
        'login_attempts': []
    }

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if re.search(r'\bERROR\b', line, re.IGNORECASE):
                    summary['errors'].append(line)
                elif re.search(r'\bWARNING\b', line, re.IGNORECASE):
                    summary['warnings'].append(line)
                elif re.search(r'login|auth|signin|failed password', line, re.IGNORECASE):
                    summary['login_attempts'].append(line)
    except FileNotFoundError:
        print(f"⚠️ Log file not found: {file_path}")
    except Exception as e:
        print(f"❌ Error reading log: {e}")

    return summary
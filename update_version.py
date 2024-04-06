# update_version.py
import sys
import re

# The type of version update: 'major', 'minor', 'patch'
update_type = sys.argv[1]


def update_version(version, update_type):
    major, minor, patch = [int(x) for x in version.split('.')]
    if update_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif update_type == 'minor':
        minor += 1
        patch = 0
    elif update_type == 'patch':
        patch += 1
    return f"{major}.{minor}.{patch}"


# Read the setup.py content
with open("setup.py", "r") as file:
    content = file.read()

# Find the version string and update it
new_content = re.sub(
    r'(version=")(.*?)(")',
    lambda m: m.group(1) + update_version(m.group(2),
                                          update_type) + m.group(3),
    content
)

# Write the updated content back to setup.py
with open("setup.py", "w") as file:
    file.write(new_content)

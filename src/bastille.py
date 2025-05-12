# core
import json
import subprocess

JAIL_KEY_NAME = 'Name'
JAIL_KEY_IP = 'IP_Address'

def getJailsByState(state = 'Up'):
  try:
    process = subprocess.run(['sudo', 'bastille', 'list', '-j'], capture_output=True, text=True, check=True)
    jails = json.loads(process.stdout)
    RunningJails = [item for item in jails if 'State' in item and item['State'] == state]

    return RunningJails
    if process.stderr:
      print("Stderr:")
      print(process.stderr)
  except subprocess.CalledProcessError as e:
    print(f"Error running 'sudo bastille': {e}")
    print("Stdout:")
    print(e.stdout)
    print("Stderr:")
    print(e.stderr)
  except FileNotFoundError:
    print("Error: The command 'bastille' was not found. Make sure it's in your system's PATH.")
  except Exception as e:
    print(f"An unexpected error occurred: {e}")

  return None

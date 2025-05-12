# core
import time

# community
import requests

# custom
import pdns
import bastille

def main():
  JailCache = {}

  while True:
    RunningJails = bastille.getJailsByState()
    if RunningJails is None:
      continue

    RunningJailChecklist = list(JailCache.keys())

    for jail in RunningJails:
      if jail[bastille.JAIL_KEY_NAME] in RunningJailChecklist:
        RunningJailChecklist.remove(jail[bastille.JAIL_KEY_NAME])

      if jail[bastille.JAIL_KEY_NAME] not in JailCache:
        # add to cache
        print (f'New jail: {jail[bastille.JAIL_KEY_NAME]}, {jail[bastille.JAIL_KEY_IP]}')
        pdns.updatePdns(jail)
        JailCache[jail[bastille.JAIL_KEY_NAME]] = jail

    if len(RunningJailChecklist) > 0:
      for JailName in RunningJailChecklist:
        # remove from cache
        pdns.deleteRecord(JailCache[JailName])
        del JailCache[JailName]
        print (f'Dead Jail: {JailName}')
    time.sleep(5)

if __name__ == "__main__":
  main()

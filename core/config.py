import inspect
import json
import os


def save(conf):
    json.dump(conf, open('config', 'w'), sort_keys=True, indent=2)

if not os.path.exists('config'):
    print("Please rename 'config.default' to 'config' to set up your bot!")
    print("For help, see https://github.com/infinitylabs/UguuBot")
    print("Thank you for using UguuBot!")
    sys.exit()


def config():
    # reload config from file if file has changed
    config_mtime = os.stat('config').st_mtime
    if bot._config_mtime != config_mtime:
        try:
            bot.config = json.load(open('config'))
            bot._config_mtime = config_mtime
        except ValueError as e:
            print('error: malformed config', e)


bot._config_mtime = 0

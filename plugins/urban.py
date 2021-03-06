from util import hook, http, text

base_url = 'http://www.urbandictionary.com/iphone/search/define'

@hook.command('u')
@hook.command('ud')
@hook.command('nig')
@hook.command('ebonics')
@hook.command
def urban(inp):
    "urban <phrase> [id] -- Looks up <phrase> on urbandictionary.com."

    # clean and split the input
    input = inp.lower().strip()
    parts = input.split()

    # if the last word is a number, set the ID to that number
    if parts[-1].isdigit():
        id = int(parts[-1])
        # remove the ID from the input string
        del parts[-1]
        input = " ".join(parts)
    else:
        id = 1

    # fetch the definitions
    page = http.get_json(base_url, term=input, referer="http://m.urbandictionary.com")
    defs = page['list']

    if page['result_type'] == 'no_results':
        return 'Not found.'

    # try getting the requested definition
    try:
        output = "[%i/%i] \x02%s\x02: %s - %s" % \
              (id, len(defs), defs[id - 1]['word'],
              defs[id - 1]['definition'].replace('\r\n', ' '),defs[id - 1]['example'].replace('\r\n', ' '))
    except IndexError:
        return 'Not found.'

    #return text.truncate_str(output, 250)
    return output

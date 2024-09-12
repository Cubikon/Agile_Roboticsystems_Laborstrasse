import gettext

def set_language(lang):
    if lang == 'en':
        translation = gettext.translation('base', localedir='locale', languages=['en'])
    elif lang == 'de':
        translation = gettext.translation('base', localedir='locale', languages=['de'])
    else:
        translation = gettext.translation('base', localedir='locale', languages=['en'])

    translation.install()
    _ = translation.gettext

    print(_('Hello, World!'))

# Set language to English
set_language('en')  # Outputs: Hello, World!

# Set language to German
set_language('de')  # Outputs: Hallo, Welt!

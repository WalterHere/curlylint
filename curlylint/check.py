from functools import partial

import click

from curlylint.rules.aria_role.aria_role import aria_role
from curlylint.rules.django_forms_rendering.django_forms_rendering import (
    django_forms_rendering,
)
from curlylint.rules.html_has_lang.html_has_lang import html_has_lang
from curlylint.rules.image_alt.image_alt import image_alt
from curlylint.rules.indent.indent import INDENT, indent
from curlylint.util import flatten

err = partial(click.secho, fg="red", err=True)

checks = {
    "aria_role": aria_role,
    "django_forms_rendering": django_forms_rendering,
    "html_has_lang": html_has_lang,
    "image_alt": image_alt,
    INDENT: indent,
}


def check_rule(file, code: str, options):
    check = checks.get(code, None)

    if not check:
        err("Warning: rule `{}` does not exist.".format(code))
        return []

    return check(file, options)


def check_file(file, rules):
    return set(
        flatten(
            check_rule(file, code, options)
            for code, options in rules.items()
            if options != "off"
        )
    )


def check_files(files, rules):
    return flatten(check_file(file, rules) for file in files)

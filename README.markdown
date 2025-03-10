
# Name to Advisor #

This is a very simple python tool that reads a name or list of names, looks
this name up on Math Genealogy, and then returns the advisors for that name.

If the given name doesn't give any matches, it raises an error.


## Example Usage ##

Call something like

    python -m name_to_advisor "David Lowry-Duda"

Alternately, make a file with one name per line, like

    David Lowry-Duda
    Isaac Newton
    John Littlewood
    Godfrey Hardy
    NOTANAMEXXXX

and call

    python -m name_to_advisor -f fname

This should output

    Note that we space out calls to MathGenealogy.
    This might take a few moments.

    David Lowry-Duda: Jeffrey Ezra Hoffstein
    Isaac Newton: Isaac  Barrow and Benjamin  Pulleyn
    John Littlewood: Ernest William Barnes
    Godfrey Hardy: Augustus Edward Hough Love and Edmund Taylor Whittaker
    Found NOTANAMEXXXX either 0 or 2+ times. Skipping.

We deliberately space out requests sequentually, with pauses between requests,
so as to not abuse MathGenealogy. When combined with buffered output, this call
can take a little bit. But calls over 15 seconds cause an exception to be
raised.


## Code Quality ##

The code is *fine*, not great, and actually parses the HTML pages of
mathgenealogy. This is fundamentally fragile. But this has been stable in the
last 10 years in my experience.



## Be kind to Math Genealogy ##

MathGenealogy is a wonderful, kind resource. They have the database out there
for the public to explore. **Don't abuse their openness.**

This tool is not a good tool to try to scrape MathGenealogy. *Please don't use
this to try to scrape MathGenealogy.*


## Licensing ##

There is little here and all true credit goes to MathGenealogy. But this code
is available under the MIT License. A copy of this license is found here.
Alternately, see https://opensource.org/license/mit.

# https://stackoverflow.com/questions/38916452/nltk-download-ssl-certificate-verify-failed#50406704
# you'll probably need to load corpora:
#   `punkt`
# you'll probably need to load models:
#   `stopwords`

import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download()

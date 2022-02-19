import doctest


master_doc = 'README'
extensions = [
    'matplotlib.sphinxext.plot_directive',
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
]
project = 'pytest_bootstrap'
napoleon_custom_sections = [('Returns', 'params_style')]
plot_formats = [
    ('png', 144),
]
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://docs.scipy.org/doc/numpy', None),
}
doctest_default_flags = doctest.ELLIPSIS | doctest.IGNORE_EXCEPTION_DETAIL \
    | doctest.DONT_ACCEPT_TRUE_FOR_1 | doctest.NORMALIZE_WHITESPACE

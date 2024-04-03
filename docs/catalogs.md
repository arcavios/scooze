<style>
    /* https://github.com/squidfunk/mkdocs-material/discussions/2532 */
    /* number of ".md-nav__list" determines the max level of TOC to be displayed in TOC */
    /* e.g. if ".md-nav__list" is repeated 3 times - the headers ####, #####,  ... will not be displayed in TOC */
    .md-sidebar--secondary .md-nav__list .md-nav__list .md-nav__list {
        display: none
    }
</style>

::: scooze.catalogs
    options:
        inherited_members: false
        show_if_no_docstring: true
        filters:
            # exclude all private/protected objects, keep special ones (default filters)
            - "!^_[^_]"

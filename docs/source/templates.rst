.. _templates:

Templates
=========

If you don't want display the pages into `Page Menus`_ you can override the page
menu templates (``tree.html``, ``dropdown.html``, ``footer.html``) checking if
the ``pk`` of current page is not in ``unauthorized_pages`` template context variable.

Here’s a example of customization of original ``tree.html`` template::

    # ...
    {% if page.in_menu and page.pk not in unauthorized_pages %}
      <li class="
                 {% if page.is_current %} active{% endif %}
                 {% if not page.is_primary and forloop.first %} first{% endif %}
                 {% if forloop.last %} last{% endif %}"
          id="tree-menu-{{ page.html_id }}">
        <a href="{{ page.get_absolute_url }}">{{ page.title }}</a>
        {# wrap the next line with 'if page.is_current_or_ascendant' #}
        {# to only show child pages in the menu for the current page #}
        {% if page.is_current_or_ascendant %}
            {% if page.has_children_in_menu %}{% page_menu page %}{% endif %}
        {% endif %}
      </li>
    {% endif %}
    # ...

The ``unauthorized_pages`` variable is inserted into template context by context
processor ``'mezzanine_page_auth.context_processors.page_auth'``
(reference :ref:`template-context-processors`)

.. _`Page Menus`: http://mezzanine.jupo.org/docs/content-architecture.html#page-menus
Tool Reference
==============

All tools return JSON strings. On error they return a human-readable
``Error <status>: <message>`` string.

Projects
--------

plane_list_projects
~~~~~~~~~~~~~~~~~~~
List all projects in the workspace.

**Parameters:**

* ``per_page`` (int, default 20) — items per page (1–100)
* ``cursor`` (str, optional) — pagination cursor

plane_create_project
~~~~~~~~~~~~~~~~~~~~
Create a new project.

**Parameters:**

* ``name`` (str, required) — project name
* ``identifier`` (str, required) — short uppercase identifier e.g. ``PROJ``
* ``description`` (str, optional) — project description
* ``network`` (int, optional) — 0=Secret, 2=Public (default 2)

plane_get_project
~~~~~~~~~~~~~~~~~
Get project details by UUID.

**Parameters:** ``project_id`` (str, required)

plane_update_project
~~~~~~~~~~~~~~~~~~~~
Update a project (partial update).

**Parameters:** ``project_id`` (str), ``name``, ``description``, ``network`` (all optional)

plane_archive_project
~~~~~~~~~~~~~~~~~~~~~
Archive (soft delete) a project.

**Parameters:** ``project_id`` (str, required)

Work Items
----------

plane_list_issues
~~~~~~~~~~~~~~~~~
**Parameters:** ``project_id``, ``per_page``, ``cursor``, ``priority``

plane_create_issue
~~~~~~~~~~~~~~~~~~
**Parameters:** ``project_id``, ``name``, ``description_html``, ``priority``, ``state``, ``assignees``, ``labels``, ``start_date``, ``target_date``, ``parent``, ``is_draft``

plane_get_issue
~~~~~~~~~~~~~~~
**Parameters:** ``project_id``, ``issue_id``

plane_get_issue_by_sequence
~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Parameters:** ``project_id``, ``sequence_id``

plane_update_issue
~~~~~~~~~~~~~~~~~~
**Parameters:** ``project_id``, ``issue_id``, plus any fields to change

plane_delete_issue
~~~~~~~~~~~~~~~~~~
**Parameters:** ``project_id``, ``issue_id``

plane_search_issues
~~~~~~~~~~~~~~~~~~~
**Parameters:** ``project_id``, ``query``

States, Labels, Cycles, Modules
--------------------------------

Each resource follows the same CRUD pattern:

* ``plane_list_<resource>`` — list all
* ``plane_create_<resource>`` — create new
* ``plane_get_<resource>`` — get by UUID
* ``plane_update_<resource>`` — partial update
* ``plane_delete_<resource>`` — delete

Cycles and modules additionally have:

* ``plane_add_issues_to_<resource>`` — add work items
* ``plane_remove_issue_from_<resource>`` — remove a work item
* ``plane_list_<resource>_issues`` — list work items in the resource

Members
-------

* ``plane_list_project_members(project_id)``
* ``plane_list_workspace_members(per_page, cursor)``

Comments
--------

* ``plane_list_issue_comments(project_id, issue_id)``
* ``plane_create_issue_comment(project_id, issue_id, comment_html)``
* ``plane_update_issue_comment(project_id, issue_id, comment_id, comment_html)``
* ``plane_delete_issue_comment(project_id, issue_id, comment_id)``

Activity
--------

* ``plane_list_issue_activity(project_id, issue_id, per_page, cursor)``

Usage
=====

Starting the Server
-------------------

.. code-block:: bash

   PLANE_API_KEY=plane_api_... PLANE_WORKSPACE_SLUG=my-ws utract-mcp

The server communicates over stdio (standard MCP transport).

Available Tools
---------------

The server exposes **44+ tools** grouped by resource:

Projects (5 tools)
~~~~~~~~~~~~~~~~~~

* ``plane_list_projects`` — list all projects in the workspace
* ``plane_create_project`` — create a new project
* ``plane_get_project`` — get project details by UUID
* ``plane_update_project`` — update project name/description/visibility
* ``plane_archive_project`` — archive (soft delete) a project

Work Items / Issues (7 tools)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``plane_list_issues`` — list work items with optional priority filter
* ``plane_create_issue`` — create a work item
* ``plane_get_issue`` — get a work item by UUID
* ``plane_get_issue_by_sequence`` — get a work item by sequence ID
* ``plane_update_issue`` — update a work item (partial)
* ``plane_delete_issue`` — delete a work item
* ``plane_search_issues`` — search work items by text

States (5 tools)
~~~~~~~~~~~~~~~~

* ``plane_list_states`` — list workflow states
* ``plane_create_state`` — create a new state
* ``plane_get_state`` — get state details
* ``plane_update_state`` — update a state
* ``plane_delete_state`` — delete a state

Labels (5 tools)
~~~~~~~~~~~~~~~~

* ``plane_list_labels`` / ``plane_create_label`` / ``plane_get_label`` / ``plane_update_label`` / ``plane_delete_label``

Cycles / Sprints (8 tools)
~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``plane_list_cycles`` / ``plane_create_cycle`` / ``plane_get_cycle`` / ``plane_update_cycle`` / ``plane_delete_cycle``
* ``plane_add_issues_to_cycle`` / ``plane_remove_issue_from_cycle`` / ``plane_list_cycle_issues``

Modules (8 tools)
~~~~~~~~~~~~~~~~~

* ``plane_list_modules`` / ``plane_create_module`` / ``plane_get_module`` / ``plane_update_module`` / ``plane_delete_module``
* ``plane_add_issues_to_module`` / ``plane_remove_issue_from_module`` / ``plane_list_module_issues``

Members (2 tools)
~~~~~~~~~~~~~~~~~

* ``plane_list_project_members`` / ``plane_list_workspace_members``

Comments (4 tools)
~~~~~~~~~~~~~~~~~~

* ``plane_list_issue_comments`` / ``plane_create_issue_comment`` / ``plane_update_issue_comment`` / ``plane_delete_issue_comment``

Activity (1 tool)
~~~~~~~~~~~~~~~~~

* ``plane_list_issue_activity`` — get the history/activity log for a work item

Example Interactions
--------------------

**List all projects:**

.. code-block:: text

   > List all my projects

**Create a work item:**

.. code-block:: text

   > Create a high-priority bug titled "Fix login crash" in project proj-uuid

**Search issues:**

.. code-block:: text

   > Search for issues mentioning "database" in project proj-uuid

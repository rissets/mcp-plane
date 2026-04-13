Installation
============

Requirements
------------

* Python 3.11+
* A running Plane or utrack instance
* A valid Plane API key

Install from PyPI
-----------------

.. code-block:: bash

   pip install utract-mcp

Install with uvx (recommended for CLI use)
-------------------------------------------

.. code-block:: bash

   uvx utract-mcp

Install from source
-------------------

.. code-block:: bash

   git clone https://github.com/your-org/utract-mcp
   cd utract-mcp
   pip install -e .

Configuration
-------------

Set the following environment variables before running the server:

.. code-block:: bash

   export PLANE_API_KEY=plane_api_yourkey
   export PLANE_WORKSPACE_SLUG=your-workspace
   export PLANE_BASE_URL=https://api.plane.so   # or your self-hosted URL

Claude Desktop Integration
--------------------------

Add to ``~/Library/Application Support/Claude/claude_desktop_config.json``:

.. code-block:: json

   {
     "mcpServers": {
       "utract": {
         "command": "uvx",
         "args": ["utract-mcp"],
         "env": {
           "PLANE_API_KEY": "plane_api_yourkey",
           "PLANE_WORKSPACE_SLUG": "your-workspace",
           "PLANE_BASE_URL": "https://api.plane.so"
         }
       }
     }
   }

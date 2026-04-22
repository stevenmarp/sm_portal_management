================================================
Portal Documents Management — Documentation
================================================

.. contents:: Table of Contents
   :depth: 2
   :local:

----

1. Getting Started
==================

Prerequisites
-------------

+----------------------------+----------------------------------------------------------------+
| Requirement                | Description                                                    |
+============================+================================================================+
| Odoo 19.0                  | Community or Enterprise edition                                |
+----------------------------+----------------------------------------------------------------+
| ``portal`` module          | Must be installed (auto-installed with most Odoo packages)     |
+----------------------------+----------------------------------------------------------------+
| ``mail`` module            | Must be installed (ships with Odoo by default)                 |
+----------------------------+----------------------------------------------------------------+

Installation
------------

1. Place ``sm_portal_document`` folder in your Odoo addons path.
2. Restart Odoo server.
3. Go to **Apps**, update the Apps List, search for *Portal Documents Management* and click **Install**.

----

2. Configuration
================

Create Directories
------------------

1. Navigate to **Portal Documents → Directories → New**.
2. Enter a directory name and optionally set a parent directory.
3. Toggle **Allow Portal Upload** if you want portal users to create sub-directories and upload files.
4. In the chatter, add portal users as **followers** to grant them access.

.. note::
   Only followers of a directory can see it in the portal.
   Sub-directories created by portal users automatically inherit the parent's followers.

Manage Documents
----------------

1. Navigate to **Portal Documents → Documents**.
2. Create documents manually or let portal users upload them.
3. Each document is linked to a directory and inherits the directory's follower-based access.

----

3. Usage
========

Portal User Experience
----------------------

1. Portal users log in and go to **My Account** (``/my``).
2. A **Documents** card appears in the portal home page.
3. Clicking it opens the directory list at ``/my/directories``.
4. Clicking a directory shows:

   - **Sub-directories** as clickable cards
   - **Documents** in a table with file icons, size, uploader, date, and download button

5. If **Allow Portal Upload** is enabled, two action buttons appear:

   - **New Sub-Directory** — create a child folder
   - **Upload Document** — upload any file

6. Click the download button on any document to save it locally.

Backend User Experience
-----------------------

- **Kanban view**: Visual cards for directories and documents.
- **List view**: Tabular overview with all key fields.
- **Form view**: Full details with stat buttons linking to child directories/documents.
- **Chatter**: Add/remove followers to control portal access.

----

4. Access Control
=================

+---------------------+----------------------------+-------------------------------------------+
| User Type           | Access Level               | How                                       |
+=====================+============================+===========================================+
| System Admin        | Full CRUD                  | ``base.group_system``                     |
+---------------------+----------------------------+-------------------------------------------+
| Internal User       | Full CRUD                  | ``base.group_user``                       |
+---------------------+----------------------------+-------------------------------------------+
| Portal User         | Read + Create (no delete)  | ``base.group_portal`` + follower rule     |
+---------------------+----------------------------+-------------------------------------------+

Portal users can only see directories where they are added as a **follower**.
Documents inherit access from their parent directory's followers.

----

5. Technical Details
====================

Models
------

- ``sm.portal.directory`` — Directory model (inherits ``mail.thread``, ``portal.mixin``)
- ``sm.portal.document`` — Document model (inherits ``mail.thread``, ``portal.mixin``)

Portal Routes
-------------

+--------------------------------------------+------------------------------------------+
| Route                                      | Description                              |
+============================================+==========================================+
| ``/my/directories``                        | List root directories                    |
+--------------------------------------------+------------------------------------------+
| ``/my/directories/<id>``                   | Directory detail (sub-dirs + documents)  |
+--------------------------------------------+------------------------------------------+
| ``/my/directories/create``                 | Create root directory (POST)             |
+--------------------------------------------+------------------------------------------+
| ``/my/directories/<id>/create``            | Create sub-directory (POST)              |
+--------------------------------------------+------------------------------------------+
| ``/my/directories/<id>/upload``            | Upload document (POST)                   |
+--------------------------------------------+------------------------------------------+
| ``/my/documents/<id>/download``            | Download document file                   |
+--------------------------------------------+------------------------------------------+

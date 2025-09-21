# 📰 Blog API (Django + DRF)

<p align="center">
  <a href="https://www.djangoproject.com/">
    <img src="https://static.djangoproject.com/img/logos/django-logo-positive.svg" height="60" alt="Django">
  </a>
  &nbsp;&nbsp;&nbsp;
  <a href="https://www.django-rest-framework.org/">
    <img src="https://www.django-rest-framework.org/img/logo.png" height="60" alt="DRF">
  </a>
</p>

<p align="center">
  <a href="#"><img alt="Python" src="https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white"></a>
  <a href="#"><img alt="Django" src="https://img.shields.io/badge/Django-5.x-092E20?logo=django&logoColor=white"></a>
  <a href="#"><img alt="DRF" src="https://img.shields.io/badge/DRF-3.x-ff1709"></a>
  <a href="#"><img alt="OpenAPI" src="https://img.shields.io/badge/OpenAPI-3.0-brightgreen"></a>
  <a href="#"><img alt="License" src="https://img.shields.io/badge/License-MIT-blue"></a>
</p>

A production-ready **Blog REST API** built with **Django** & **Django REST Framework**.  
Features: posts, categories, tags, comments (single-level replies), likes, bookmarks, user profiles, JWT auth, and Swagger docs.

---

## 📋 Table of Contents
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
- [Auth Flow](#-auth-flow)
- [Core Endpoints](#-core-endpoints)
- [Data Model](#-data-model)
- [Development Tips](#-development-tips)
- [Testing](#-testing)
- [Deployment Notes](#-deployment-notes)
- [License](#-license)

---

## ✨ Features
- 🔐 **JWT Auth** with access/refresh + **Register** endpoint
- 📝 **Posts** CRUD, publish/unpublish, **likes**, **bookmarks**
- 🗂 **Categories** (slug-based) & **Tags** (M2M)
- 💬 **Comments** with single-level replies + like counts
- 👤 **Profile** (1-1) auto-created via **signals**, avatar upload (ImageField)
- 🔎 Search, ↕ ordering, 📄 pagination
- 📜 **OpenAPI 3.0** schema + **Swagger UI** (drf-spectacular + sidecar)
- ⚡ Optimized querysets (`select_related`, `prefetch_related`, `annotate`)

---

## 🧰 Tech Stack
- **Django** 5.x, **Django REST Framework** 3.x
- **SimpleJWT** for tokens
- **drf-spectacular** (+ sidecar) for API docs
- **Pillow** for images
- **SQLite** (dev) / **PostgreSQL** (prod-ready)

---

## 🗂 Project Structure
```
project-root/
├─ manage.py
├─ requirements.txt
├─ .env.example
├─ blogginapplication/ # project (settings/urls/wsgi/asgi)
│ ├─ init.py
│ ├─ settings.py
│ ├─ urls.py
│ └─ asgi.py / wsgi.py
└─ blog/ # main app
├─ init.py
├─ apps.py
├─ models.py
├─ signals.py # user -> profile auto-create
├─ permissions.py
├─ utils/ # helpers (slugify, auth_user, text utils…)
│ └─ init.py
├─ serializers/
│ ├─ init.py
│ ├─ auth.py # Register, Me, ChangePassword, DTOs
│ ├─ posts.py # PostList, PostDetail, PostWrite…
│ ├─ comments.py # CommentRead/Write/Reply
│ └─ common.py # UserMini, Category/Tag serializers
├─ views/
│ ├─ init.py
│ ├─ auth.py # Register, Me, ChangePassword
│ ├─ posts.py # PostViewSet (publish/like/bookmark)
│ ├─ taxonomy.py # CategoryViewSet, TagViewSet
│ └─ comments.py # CommentViewSet
└─ urls.py # routers + auth routes
```


---

## 🚀 Quick Start

> Prereqs: **Python 3.12**, **Git**. (SQLite by default; Postgres optional)

```bash
# 1) Clone
git clone <YOUR_REPO_URL>
cd <YOUR_REPO_FOLDER>

# 2) Virtualenv
python -m venv .venv
# mac/linux:
source .venv/bin/activate
# windows (powershell):
# .\.venv\Scripts\Activate

# 3) Install deps
pip install -r requirements.txt

# 4) Environment
cp .env.example .env
# then edit .env (see below)

# 5) DB & superuser (optional)
python manage.py migrate
python manage.py createsuperuser

# 6) Run dev server
python manage.py runserver

# 7) Open docs
# Swagger UI:   http://127.0.0.1:8000/api/docs/
# OpenAPI JSON: http://127.0.0.1:8000/api/schema/
```

## ⚙️ Configuration

## Security
```
DJANGO_SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB (defaults to SQLite if not set)
For Postgres (optional):
DATABASE_URL=postgresql://USER:PASSWORD@127.0.0.1:5432/blogdb

#JWT lifetimes
SIMPLE_JWT_ACCESS_MINUTES=1
SIMPLE_JWT_REFRESH_DAYS=7

# Media (dev)
MEDIA_URL=/media/
MEDIA_ROOT=media
```
Make sure settings.py reads these (via os.environ or python-dotenv).

## 📚 API Documentation

Swagger UI → GET /api/docs/

OpenAPI schema (JSON) → GET /api/schema/
Import the JSON into Postman to auto-generate a collection.

## 🔑 Auth Flow

### Endpoints

POST /api/auth/register/ → create user, returns { user, access, refresh }

POST /api/token/ → login (username/password) → { access, refresh }

POST /api/token/refresh/ → refresh access

GET /api/auth/me/ → current user (Bearer token)

POST /api/auth/password/change/ → change password (Bearer token)

## Register request
```
{
  "username": "ashish",
  "email": "ashish@example.com",
  "first_name": "Ashish",
  "last_name": "Pal",
  "password": "StrongP@ssw0rd",
  "confirm_password": "StrongP@ssw0rd"
}
```

## 🔗 Core Endpoints
## Categories (admin write)

GET /api/categories/

POST /api/categories/ ({ name, slug })

GET /api/categories/{slug}/

PUT/PATCH/DELETE /api/categories/{slug}/

## Tags (admin write)

GET /api/tags/

POST /api/tags/ ({ name, slug })

GET /api/tags/{slug}/

PUT/PATCH/DELETE /api/tags/{slug}/

## Posts

## 📝 Posts API — Colorful Cheatsheet

> All write ops require **Bearer JWT**. Content-Type: `application/json`.

<table>
  <tr>
    <td><img src="https://img.shields.io/badge/GET-blue?style=for-the-badge" /></td>
    <td><code>/api/posts/</code></td>
    <td>
      List posts with search/order/pagination.<br/>
      <strong>Query</strong>:
      <code>?search=term</code>,
      <code>?ordering=-created_at</code>,
      <code>?page=1&amp;page_size=10</code>,
      <code>?category=&lt;slug&gt;</code>,
      <code>?tags=tag1,tag2</code>
    </td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/POST-brightgreen?style=for-the-badge" /></td>
    <td><code>/api/posts/</code></td>
    <td>
      Create a post (category/tags by <em>slug</em>).<br/>
      <code>{
        "title":"DRF Tips",
        "body":"Best practices...",
        "status":"DRAFT",
        "category":"python",
        "tags":["drf","django"]
      }</code>
    </td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/GET-blue?style=for-the-badge" /></td>
    <td><code>/api/posts/{id}/</code></td>
    <td>Retrieve post detail (author, category, tags, counts, flags).</td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/PUT-orange?style=for-the-badge" /></td>
    <td><code>/api/posts/{id}/</code></td>
    <td>Full update the post (send all updatable fields).</td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/PATCH-purple?style=for-the-badge" /></td>
    <td><code>/api/posts/{id}/</code></td>
    <td>Partial update (e.g., <code>{ "status":"PUBLISHED" }</code>).</td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/DELETE-red?style=for-the-badge" /></td>
    <td><code>/api/posts/{id}/</code></td>
    <td>Delete the post (author or admin only).</td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/POST-brightgreen?style=for-the-badge" /></td>
    <td><code>/api/posts/{id}/publish/</code></td>
    <td>Publish the post (requires non-empty <code>body</code>).</td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/POST-brightgreen?style=for-the-badge" /></td>
    <td><code>/api/posts/{id}/unpublished/</code></td>
    <td>Unpublish (revert to draft/hidden state).</td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/POST-brightgreen?style=for-the-badge" /></td>
    <td><code>/api/posts/{id}/like/</code></td>
    <td>Like the post (idempotent).</td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/DELETE-red?style=for-the-badge" /></td>
    <td><code>/api/posts/{id}/like/</code></td>
    <td>Unlike the post.</td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/POST-brightgreen?style=for-the-badge" /></td>
    <td><code>/api/posts/{id}/bookmark/</code></td>
    <td>Bookmark the post.</td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/DELETE-red?style=for-the-badge" /></td>
    <td><code>/api/posts/{id}/bookmark/</code></td>
    <td>Remove bookmark.</td>
  </tr>
</table>

### Notes
- <strong>Write serializer expects slugs</strong> for <code>category</code> and <code>tags</code>.
- Publish rule: <code>PUBLISHED</code> posts must have a non-empty <code>body</code>.
- Flags in list/detail: <code>is_liked_by_me</code>, <code>is_bookmarked_by_me</code>, plus <code>like_count</code>, <code>comment_count</code>.

## Create Post (write serializer expects slugs)
```
{
  "title": "DRF Tips",
  "body": "Best practices...",
  "status": "DRAFT",
  "category": "python",           // category slug
  "tags": ["drf","django"]        // tag slugs
}
```


Publish rule: PUBLISHED posts must have non-empty body.
Partial update smartly uses existing body if not provided.


## Comments

## 💬 Comments API — Cheatsheet

> All write ops require **Bearer JWT**. Content-Type: `application/json`.

<table>
  <tr>
    <td><img src="https://img.shields.io/badge/GET-blue?style=for-the-badge" /></td>
    <td><code>/api/comments/?post={post_id}</code></td>
    <td>List comments (and one-level replies) for a post.</td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/POST-brightgreen?style=for-the-badge" /></td>
    <td><code>/api/comments/</code></td>
    <td>
      Create a top-level comment.<br/>
      <code>{ "post": 123, "body": "Nice article!" }</code>
    </td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/POST-brightgreen?style=for-the-badge" /></td>
    <td><code>/api/comments/</code></td>
    <td>
      Create a reply (single-level).<br/>
      <code>{ "post": 123, "parent": 456, "body": "Thanks!" }</code>
    </td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/GET-blue?style=for-the-badge" /></td>
    <td><code>/api/comments/{id}/</code></td>
    <td>Retrieve a specific comment.</td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/PUT-orange?style=for-the-badge" /></td>
    <td><code>/api/comments/{id}/</code></td>
    <td>
      Full update a comment.<br/>
      <code>{ "post": 123, "body": "Edited text" }</code>
    </td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/PATCH-purple?style=for-the-badge" /></td>
    <td><code>/api/comments/{id}/</code></td>
    <td>
      Partial update a comment.<br/>
      <code>{ "body": "Edited (partial)" }</code>
    </td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/DELETE-red?style=for-the-badge" /></td>
    <td><code>/api/comments/{id}/</code></td>
    <td>Delete a comment.</td>
  </tr>
</table>

### Notes
- Replies are **single-level** only (no reply-to-reply nesting).
- Visibility/status rules apply if implemented (e.g., only <code>VISIBLE</code> comments returned).
- Typical filters: <code>?post=&lt;id&gt;</code>, plus pagination: <code>?page=1&amp;page_size=10</code>.


## Profile

GET /api/me/profile/

PATCH /api/me/profile/ (multipart for avatar, text for display_name, bio)


## 🧠 Data Model (3NF)
```
User —< Post

User —< Comment (self FK parent → one-level replies)

Category 1—* Post

Tag — Post (through table)

PostLike: unique (user, post)

CommentLike: unique (user, comment)

Bookmark: unique (user, post)

Profile: 1—1 User (auto-create via signal)
```

## 💡 Development Tips
* Media (dev): urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

* Signals: apps.py -> ready(): from . import signals and INSTALLED_APPS = ["blog.apps.BlogConfig", ...]


## Permissions

* Categories/Tags: IsAdminOrReadOnly

* Posts/Comments: IsAuthenticatedOrReadOnly + object-level IsAuthorOrReadOnly

* Queryset perf: select_related("author","category"), prefetch_related("tags"), annotate() counts

* Swagger assets: install & add drf_spectacular_sidecar to INSTALLED_APPS

## VS Code Debug (optional)
Create .vscode/launch.json:
```
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Django: runserver (debug)",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/manage.py",
      "args": ["runserver", "127.0.0.1:8000", "--noreload"],
      "django": true,
      "justMyCode": true,
      "env": {
        "DJANGO_SETTINGS_MODULE": "blogginapplication.settings",
        "PYTHONPATH": "${workspaceFolder}"
      }
    }
  ]
}
```

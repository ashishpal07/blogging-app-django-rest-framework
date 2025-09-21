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

<p align="center">
  <a href="/api/docs/">
    <img src="https://img.shields.io/badge/Swagger-UI-85EA2D?logo=swagger&logoColor=white&style=for-the-badge" alt="Swagger UI">
  </a>
  &nbsp;
  <a href="/api/schema/">
    <img src="https://img.shields.io/badge/OpenAPI-3.0-6BA539?logo=openapiinitiative&logoColor=white&style=for-the-badge" alt="OpenAPI 3.0">
  </a>
</p>


<table>
  <tr>
    <td><img src="https://img.shields.io/badge/GET-blue?style=for-the-badge" /></td>
    <td><code>/api/docs/</code></td>
    <td>Swagger UI</td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/GET-blue?style=for-the-badge" /></td>
    <td><code>/api/schema/</code></td>
    <td>OpenAPI schema (JSON) — import into Postman to auto-generate a collection</td>
  </tr>
</table>

---

## 🔑 Auth Flow

<p align="center">
  <img src="https://img.shields.io/badge/Auth-JWT-000000?logo=jsonwebtokens&logoColor=white&style=for-the-badge" alt="JWT">
  &nbsp;
  <img src="https://img.shields.io/badge/Register/Login/Refresh/Me/Change-Password-3F51B5?style=for-the-badge" alt="Auth Flow">
</p>


> All bodies are <code>application/json</code>. Protected routes require <code>Authorization: Bearer &lt;access_token&gt;</code>.

<table>
  <tr>
    <th>Method</th>
    <th>Endpoint</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/POST-brightgreen?style=for-the-badge" /></td>
    <td><code>/api/auth/register/</code></td>
    <td>Create user, returns <code>{ user, access, refresh }</code></td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/POST-brightgreen?style=for-the-badge" /></td>
    <td><code>/api/token/</code></td>
    <td>Login (username/password) → <code>{ access, refresh }</code></td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/POST-brightgreen?style=for-the-badge" /></td>
    <td><code>/api/token/refresh/</code></td>
    <td>Refresh access token</td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/GET-blue?style=for-the-badge" /></td>
    <td><code>/api/auth/me/</code></td>
    <td>Current user info (Bearer token)</td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/POST-brightgreen?style=for-the-badge" /></td>
    <td><code>/api/auth/password/change/</code></td>
    <td>Change password (Bearer token)</td>
  </tr>
</table>

## 🔗 Core Endpoints

## 🗂 Categories API — (admin write)
<!-- 🗂 Categories — logo header -->
<p align="center">
  <img src="https://img.shields.io/badge/Categories-Taxonomy-8BC34A?logo=googleclassroom&logoColor=white&style=for-the-badge" alt="Categories">
  &nbsp;
  <img src="https://img.shields.io/badge/Slug--Based-Yes-689F38?style=for-the-badge" alt="Slug Based">
  &nbsp;
  <img src="https://img.shields.io/badge/Admin-Write-558B2F?style=for-the-badge" alt="Admin Write">
</p>

> List is public; **create/update/delete require admin/staff** (IsAdminOrReadOnly).

<table>
  <tr>
    <td><img src="https://img.shields.io/badge/GET-blue?style=for-the-badge" /></td>
    <td><code>/api/categories/</code></td>
    <td>
      List categories (supports search/order/pagination).<br/>
      <strong>Query</strong>:
      <code>?search=py</code>,
      <code>?ordering=name</code>,
      <code>?page=1&amp;page_size=20</code>
    </td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/POST-brightgreen?style=for-the-badge" /></td>
    <td><code>/api/categories/</code></td>
    <td>
      Create a category (admin).<br/>
      <code>{ "name": "Python", "slug": "python" }</code>
    </td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/GET-blue?style=for-the-badge" /></td>
    <td><code>/api/categories/{slug}/</code></td>
    <td>Retrieve a category (by slug).</td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/PUT-orange?style=for-the-badge" /></td>
    <td><code>/api/categories/{slug}/</code></td>
    <td>
      Full update (admin).<br/>
      <code>{ "name": "Python &amp; Django", "slug": "python-django" }</code>
    </td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/PATCH-purple?style=for-the-badge" /></td>
    <td><code>/api/categories/{slug}/</code></td>
    <td>
      Partial update (admin).<br/>
      <code>{ "name": "Python" }</code>
    </td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/DELETE-red?style=for-the-badge" /></td>
    <td><code>/api/categories/{slug}/</code></td>
    <td>Delete a category (admin).</td>
  </tr>
</table>

### Notes
- <strong>Slug</strong> is unique and used in URLs; choose URL-safe slugs (e.g., <code>django-rest</code>).
- Useful for post writes: send <code>category</code> as its <em>slug</em> in the Post write payload.

---

## 🏷 Tags API — (admin write)

<!-- 🏷 Tags — logo header -->
<p align="center">
  <img src="https://img.shields.io/badge/Tags-Many--to--Many-7E57C2?logo=hashnode&logoColor=white&style=for-the-badge" alt="Tags">
  &nbsp;
  <img src="https://img.shields.io/badge/Slugs-Required-5C6BC0?style=for-the-badge" alt="Slugs Required">
  &nbsp;
  <img src="https://img.shields.io/badge/Admin-Write-3949AB?style=for-the-badge" alt="Admin Write">
</p>


> List is public; **create/update/delete require admin/staff** (IsAdminOrReadOnly).

<table>
  <tr>
    <td><img src="https://img.shields.io/badge/GET-blue?style=for-the-badge" /></td>
    <td><code>/api/tags/</code></td>
    <td>
      List tags (supports search/order/pagination).<br/>
      <strong>Query</strong>:
      <code>?search=drf</code>,
      <code>?ordering=name</code>,
      <code>?page=1&amp;page_size=20</code>
    </td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/POST-brightgreen?style=for-the-badge" /></td>
    <td><code>/api/tags/</code></td>
    <td>
      Create a tag (admin).<br/>
      <code>{ "name": "DRF", "slug": "drf" }</code>
    </td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/GET-blue?style=for-the-badge" /></td>
    <td><code>/api/tags/{slug}/</code></td>
    <td>Retrieve a tag (by slug).</td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/PUT-orange?style=for-the-badge" /></td>
    <td><code>/api/tags/{slug}/</code></td>
    <td>
      Full update (admin).<br/>
      <code>{ "name": "Django REST", "slug": "django-rest" }</code>
    </td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/PATCH-purple?style=for-the-badge" /></td>
    <td><code>/api/tags/{slug}/</code></td>
    <td>
      Partial update (admin).<br/>
      <code>{ "name": "Django" }</code>
    </td>
  </tr>

  <tr>
    <td><img src="https://img.shields.io/badge/DELETE-red?style=for-the-badge" /></td>
    <td><code>/api/tags/{slug}/</code></td>
    <td>Delete a tag (admin).</td>
  </tr>
</table>

### Notes
- <strong>Slug</strong> is unique and used in Post write payloads (e.g., <code>"tags": ["drf","django"]</code>).
- Keep names human-readable; use lowercase hyphenated slugs for consistency.

## 📝 Posts API

<p align="center">
  <img src="https://img.shields.io/badge/Posts-Blog-FF5722?logo=blogger&logoColor=white&style=for-the-badge" alt="Posts">
  &nbsp;
  <img src="https://img.shields.io/badge/Content-Create/Read/Update/Delete-795548?style=for-the-badge" alt="CRUD">
</p>


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

## 💬 Comments API

<!-- 💬 Comments — logo header -->
<p align="center">
  <img src="https://img.shields.io/badge/Comments-API-00BCD4?logo=discourse&logoColor=white&style=for-the-badge" alt="Comments API">
  &nbsp;
  <img src="https://img.shields.io/badge/Replies-One%20Level-009688?style=for-the-badge" alt="One-level replies">
  &nbsp;
  <img src="https://img.shields.io/badge/CRUD-GET%20POST%20PUT%20PATCH%20DELETE-795548?style=for-the-badge" alt="CRUD">
</p>


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


<!-- 👤 Profile — logo header -->
<p align="center">
  <img src="https://img.shields.io/badge/Profile-API-607D8B?logo=gravatar&logoColor=white&style=for-the-badge" alt="Profile API">
  &nbsp;
  <img src="https://img.shields.io/badge/Avatar-Upload-455A64?style=for-the-badge" alt="Avatar Upload">
  &nbsp;
  <img src="https://img.shields.io/badge/Protected-Bearer%20JWT-263238?style=for-the-badge" alt="Protected">
</p>

## 👤 Profile

> Requires <code>Authorization: Bearer &lt;access_token&gt;</code>.

<table>
  <tr>
    <td><img src="https://img.shields.io/badge/GET-blue?style=for-the-badge" /></td>
    <td><code>/api/me/profile/</code></td>
    <td>Get my profile (display_name, bio, avatar, etc.).</td>
  </tr>
  <tr>
    <td><img src="https://img.shields.io/badge/PATCH-purple?style=for-the-badge" /></td>
    <td><code>/api/me/profile/</code></td>
    <td>
      Update profile (multipart).<br/>
      <strong>Fields:</strong> <code>display_name</code> (text), <code>bio</code> (text), <code>avatar</code> (file).
    </td>
  </tr>
</table>

### Example (cURL) — update with avatar
```bash
curl -X PATCH http://127.0.0.1:8000/api/me/profile/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Accept: application/json" \
  -F "display_name=Ashish" \
  -F "bio=Backend dev & blogger" \
  -F "avatar=@/path/to/avatar.jpg"
```


## 🧠 Data Model (3NF)

<p align="center">
  <img src="https://img.shields.io/badge/Schema-3NF-4CAF50?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Relations-1:1%20%7C%201:N%20%7C%20N:M-2196F3?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Integrity-PK%20%7C%20Unique-9C27B0?style=for-the-badge" />
</p>

```mermaid
erDiagram
    USER ||--o{ POST : writes
    USER ||--o{ COMMENT : writes
    USER ||--|| PROFILE : has
    CATEGORY ||--o{ POST : categorizes
    POST }o--o{ TAG : tagged_with
    POST ||--o{ COMMENT : has
    USER ||--o{ POST_LIKE : likes
    USER ||--o{ BOOKMARK : bookmarks
    USER ||--o{ COMMENT_LIKE : likes
    COMMENT ||--o{ COMMENT : has_reply

    USER {
      int id PK
      string username
      string email
    }

    PROFILE {
      int id PK
      int user_id
      string display_name
      string bio
      string avatar
    }

    CATEGORY {
      int id PK
      string name
      string slug
      datetime created_at
      datetime updated_at
    }

    TAG {
      int id PK
      string name
      string slug
      datetime created_at
      datetime updated_at
    }

    POST {
      int id PK
      int author_id
      int category_id
      string title
      string slug
      text body
      string status
      datetime published_at
      datetime created_at
      datetime updated_at
    }

    COMMENT {
      int id PK
      int post_id
      int author_id
      int parent_id
      text body
      string status
      datetime created_at
      datetime updated_at
    }

    POST_LIKE {
      int id PK
      int user_id
      int post_id
    }

    COMMENT_LIKE {
      int id PK
      int user_id
      int comment_id
    }

    BOOKMARK {
      int id PK
      int user_id
      int post_id
    }
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

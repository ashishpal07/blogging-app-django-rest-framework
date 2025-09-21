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

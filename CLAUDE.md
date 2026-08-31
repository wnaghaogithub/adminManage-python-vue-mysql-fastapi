# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Greenfield admin management system. Two sibling projects:

- **Front-adminManage/** — Vue 3 + Element Plus frontend
- **Back-adminManage/** — Python + FastAPI + MySQL backend

Both directories are currently empty scaffolds and have not been implemented yet.

## Planned Requirements

- **Login page** and logout
- **Home page (user management)** with CRUD (增删改查) for fields:
  - 用户名 (username)
  - 用户省市区 (province/city/region)
  - 用户图像 (user avatar — upload)
  - 年龄 (age)
  - 密码 (password — display both masked and unmasked)
- All operations sync to MySQL

## Backend API Endpoints (planned)

- User CRUD
- User login
- User logout

## Database Plan (planned)

- MySQL database: `managedata_base`
- `users` table — to be created with realistic seed data

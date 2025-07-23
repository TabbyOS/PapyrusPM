# Papyrus Project Manager

A lightweight Python tool for managing, compiling, and organizing Papyrus scripting projects for Bethesda games (Skyrim SE/AE).  
Currently in internal use, subject to further development and refinement.

Repository: [https://github.com/TabbyOS/PapyrusPM](https://github.com/TabbyOS/PapyrusPM)

---

## Features

- Project list with persistent storage
- Folder structure view per project
- Project compilation via external compiler
- Settings manager (compiler path, source/output directories)
- Log file reader (auto-refresh)
- Modular architecture (core / ui / utils)

---

## Requirements

- Python 3.10 or later
- Papyrus compiler (from Creation Kit or equivalent)

---

## Working on:

- Per-project compiler settings (INI handling)

- Build profile support

- Drag-and-drop for adding projects

- Script template creation (New Script dialog)

- Compilation error parser with clickable log navigation

- Archive2 or BSA packer integration

- MCM-based script scanner

- Plugin system for extending functionality

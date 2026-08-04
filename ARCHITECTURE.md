# Blender Production System (BPS) Architecture

## Overview

The Blender Production System (BPS) is a modular production pipeline for creating animation-ready characters inside Blender.

The system is designed around independent production stages rather than one large script.

Each production stage performs one specific task.

---

# Production Pipeline

Character Project

↓

Reference Import

↓

Blueprint Generation

↓

Base Mesh Generation

↓

Mesh Fusion

↓

Sculpt Preparation

↓

Retopology

↓

Rigging

↓

Materials

↓

Animation

↓

Rendering

---

# Core Principles

## Modular

Every production stage is independent.

Examples:

- Blueprint Generator
- Base Mesh Generator
- Rig Generator
- Material Generator

Each module should be replaceable without affecting the rest of the system.

---

## Non-Destructive

Generated assets should never overwrite previous production stages.

Every stage creates new production assets while preserving earlier work whenever practical.

---

## Reusable

Shared code belongs in reusable helper modules.

Examples:

- Mesh Helpers
- Proportion Library
- Naming Utilities
- Collection Utilities

---

## Scalable

The architecture is designed to support:

- Educational characters
- Game characters
- Animated films
- Studio pipelines

---

# Project Structure

```
addon/

checks/
operators/
ui/
properties/
generators/
utilities/
```

---

# Generator System

The Base Mesh Generator is divided into reusable modules.

Current generators include:

- Head Generator
- Torso Generator
- Arm Generator
- Leg Generator
- Hand Generator
- Foot Generator

Future generators may include:

- Hair Generator
- Ear Generator
- Eye Generator
- Mouth Generator
- Tail Generator
- Wing Generator

---

# Character Templates

Future versions will support predefined character templates.

Examples:

- Kyro
- Nyla
- Leafy
- Sammie
- Allie
- Asia

Templates define:

- proportions
- species
- mesh generation
- rig settings
- materials

---

# Production Goals

The long-term goal of BPS is to provide a complete production pipeline capable of generating production-ready characters with minimal manual setup.

The system is intended to support educational animation, games, independent creators, and professional production environments.

---

# Design Philosophy

Small modules.

Reusable code.

Clear production stages.

Professional workflow.

Maintainable architecture.

Expandable system.

# Blender Production System (BPS)

# Development Standards

Version: 1.0

Author: Patrice Newson

---

# Purpose

This document defines the engineering standards used throughout Blender Production System (BPS).

Every contributor should follow these standards to keep the project consistent, maintainable, and production-ready.

---

# Core Principles

1. Readability First

Code should be easy to understand before it is optimized.

2. Consistency Over Cleverness

Simple, predictable code is preferred over complex shortcuts.

3. One Responsibility

Each module should perform one clearly defined task.

4. Production Ready

Every feature should support a real production workflow.

5. Documentation Is Required

No feature is considered complete until its documentation has been updated.

---

# Naming Standards

## Panels

BPS_PT_CharacterPanel

BPS_PT_BlueprintPanel

BPS_PT_ModelingPanel

---

## Operators

BPS_OT_GenerateBlueprint

BPS_OT_GenerateRig

BPS_OT_CreateCharacter

---

## Engines

CharacterEngine

BlueprintEngine

RiggingEngine

---

## Data

CharacterData

RigData

MaterialData

---

## Checks

NamingCheck

TransformCheck

RigCheck

TopologyCheck

---

## Reports

CharacterReport

RigReport

CertificationReport

---

# Folder Standards

addon/

checks/

data/

engine/

operators/

reports/

templates/

ui/

utils/

Every new feature belongs inside one of these folders.

---

# UI Standards

Panels display information.

Panels launch operators.

Panels never contain production logic.

---

# Operator Standards

Operators should:

Validate input

Call an engine

Handle errors

Return status to Blender

Operators should never contain production algorithms.

---

# Engine Standards

Engines contain production logic.

Engines should:

Create

Modify

Validate

Process

Return results

Engines should never draw Blender UI.

---

# Check Standards

Checks answer only one question:

"Is this correct?"

Each check should return:

PASS

or

FAIL

with a clear explanation.

---

# Report Standards

Reports summarize production.

Reports should include:

Date

Version

Character

Stage

Results

Certification Status

---

# Documentation Standards

Every release updates:

Product Bible

Architecture

Development Standards

Release Notes

Roadmap

Change Log

---

# Versioning

Major

Breaking architecture changes.

Example

2.0.0

Minor

New production features.

Example

1.2.0

Patch

Bug fixes.

Example

1.2.1

---

# Release Process

1.

Save All

2.

Update Version

3.

Build Extension

4.

Install Extension

5.

Restart Blender

6.

Run Validation

7.

Update Documentation

8.

Commit to GitHub

9.

Push to GitHub

10.

Publish Release Notes

---

# Git Commit Format

Examples

Add Modeling Studio

Add Rigging Studio

Fix Blueprint Registration

Improve Character Engine

Add Certification Report

---

# Pull Request Standards

Every pull request should answer:

What was changed?

Why was it changed?

How was it tested?

Does documentation need updating?

---

# Error Handling

Never allow silent failures.

Always provide:

Meaningful error messages

Recovery suggestions

Production-safe defaults

---

# Testing Standards

Every feature should be tested using a real production asset.

Primary validation project:

Kyro & Nyla's Learning Adventures

A feature is not complete until it has been successfully used during production.

---

# Future Contributors

Before writing code:

Read:

Product Bible

Technical Architecture

Development Standards

Understand the production pipeline before implementing new features.

---

# Goal

Maintain a clean, professional, scalable codebase capable of supporting long-term production work and open-source collaboration.

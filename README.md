# Tennis Match Predictor

> **Status: In Progress**

A machine learning project for predicting ATP tennis match outcomes using historical match data, time-aware feature engineering, and chronological model evaluation.

The goal of the project is to build a realistic prediction pipeline that uses only information available **before a match takes place**, avoiding temporal data leakage.

---

## Overview

The project processes historical ATP match data and builds pre-match features describing the relative strength, form, surface performance, matchup history, and service performance of two players.

Instead of training directly on raw winner/loser data, matches are transformed into an outcome-independent **Player A / Player B** representation.

The model is trained on historical data and evaluated chronologically against a simple ATP ranking-based baseline.

---

## Current Features

The current feature set includes:

- Overall Elo rating
- Surface-specific Elo rating
- ATP ranking difference
- Overall win rate
- Recent form
- Surface-specific recent form
- Head-to-head win rate
- Number of historical matches played
- Rolling ace rate
- Rolling double-fault rate
- Rolling first-serve percentage
- Rolling first-serve points won percentage
- Rolling second-serve points won percentage
- Rolling break-points saved percentage

Feature values are represented primarily as differences between **Player A** and **Player B**.

---

## Time-Aware Feature Engineering

One of the main goals of the project is to prevent data leakage.

Matches are processed chronologically.

For each match:

1. The current historical state of both players is retrieved.
2. Pre-match features are calculated using only previously played matches.
3. The features are stored for the current match.
4. Only after that is the player state updated using the result and statistics of the current match.

This ensures that a prediction never uses information that would not have been available at prediction time.

---

## Player State

The project maintains an evolving historical state for every player.

The state currently tracks information such as:

- Elo rating
- Surface Elo ratings
- Matches played
- Matches won
- Recent match results
- Surface-specific recent results
- Rolling service statistics

This state is updated incrementally after each match.

---

## Player A / Player B Representation

The source dataset identifies players as `winner` and `loser`.

Using those labels directly as model inputs would reveal the outcome of the match.

To avoid this, every match is converted into a neutral representation:

- Player A
- Player B

Player ordering is determined independently from the match result.

The prediction target indicates whether Player A won the match.

---

## Rolling Statistics

Recent performance metrics use rolling historical windows rather than full-career averages.

For percentage-based service statistics, raw counts are aggregated first and the final rate is calculated afterwards.

For example:

```text
ace_rate =
total_aces / total_service_points
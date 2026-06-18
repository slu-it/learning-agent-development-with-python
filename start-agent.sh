#!/bin/bash
#HTTP_TRACE=true
uv run uvicorn app.server:app --reload

#!/bin/bash
llama-server -hf ggml-org/gemma-4-E4B-it-GGUF --jinja --ctx-size 65536 --port 9000 --alias gemma-4

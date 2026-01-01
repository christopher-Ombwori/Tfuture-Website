#!/bin/bash
# Script to compile MJML email templates

echo "Compiling MJML email templates..."
cd templates/core/emails

# Compile all MJML files
npx mjml mjml/*.mjml -o .

# Clean the compiled HTML files
python clean_html.py

echo "✓ Email templates compiled successfully"

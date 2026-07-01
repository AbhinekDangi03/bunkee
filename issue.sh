#!/bin/bash

read -p "Issue Title: " I_title
read -p "Issue Label [go for (good first issue), (inhancement)" I_label

gh issue create \
  --title "$I_title" \
  --label "$I_label" \
  --assignee "@me"

echo "ISSUE RAISE"

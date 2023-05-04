#!/bin/bash

az login --allow-no-subscriptions

az rest --method get --uri https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies
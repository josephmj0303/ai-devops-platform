# Kubernetes Authorization Troubleshooting

During Kubernetes action testing, cluster inspection succeeded but
a deployment restart returned an Unauthorized response.

## Root Cause

Kubernetes API connectivity and Kubernetes authorization are separate
concerns. The backend could communicate with the cluster but did not
initially have the required authorization for the operational action.

## Resolution

The Kubernetes credential and authorization configuration was corrected.

The deployment restart operation was then successfully executed and
the result was recorded in DevOps action history.

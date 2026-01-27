# Use the same base image you were using in devcontainer.json
FROM mcr.microsoft.com/devcontainers/jekyll:latest

# WORKAROUND: Fix the expired Yarn GPG key
# We simply remove the yarn repository list because it causes apt-get update to fail.
# If you explicitly need Yarn, you can re-install it later or update the key, 
# but usually removing this stale entry allows the build to proceed.
RUN rm -f /etc/apt/sources.list.d/yarn.list
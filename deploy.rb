#!/usr/bin/env ruby

require "open3"

# --- CONFIGURATION ---
REMOTE_USER = "kabilan"
REMOTE_HOST = "rlogin.cs.vt.edu"
REMOTE_PATH = "/web/people/kabilan/"
LOCAL_DIR   = "_site/"

def run_command(cmd)
  puts "▶ #{cmd}"
  success = system(cmd)

  unless success
    puts "❌ Error running: #{cmd}"
    exit(1)
  end
end

def main
  puts "🚀 Starting deployment to #{REMOTE_HOST}..."

  # Step 1: Build Jekyll site
  puts "🔨 Building Jekyll site..."
  run_command("bundle exec jekyll build")

  # Step 2: Deploy with rsync
  puts "📤 Pushing files to server..."

  rsync_cmd = "rsync -avz --delete #{LOCAL_DIR} #{REMOTE_USER}@#{REMOTE_HOST}:#{REMOTE_PATH}"
  run_command(rsync_cmd)

  puts "✅ Deployment Complete!"
end

main
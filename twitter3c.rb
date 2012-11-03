#!/usr/bin/env ruby
#
# finds available 3 character twitter accounts
# might add userlist support later but its not really needed
# twitter has an api limit on these requests - how many, i don't know.
# requests need to be throttled greatly or maybe implement w/ tor gem
# for exit node switching to evade limits. idk.
# don't hate.

require 'net/http'
require 'uri'

def russians_write_the_best_malware
  users = ('aaa'..'zzz').to_a
  users.each do |u|
  	sleep(3)
  	uri = URI.parse("http://api.twitter.com/1/users/show.json?screen_name=#{u}")
  	resp = Net::HTTP.get_response(uri)
  	if resp.code == "404"
  	  puts "[~] AVAILABLE: #{u}"
  	end
  puts "[!] not available: #{u}"
  end
end

puts "\n[~] Starting search..."
russians_write_the_best_malware

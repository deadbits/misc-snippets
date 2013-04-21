#!/usr/bin/env ruby
##
# ruby `watch` command equivalent
# made for OS X since its lacking the real binary
#
# https://github.com/ohdae/misc-snippets
##

usage = "usage: ./watch.rb <command>\ninterval defaults to 30 seconds"

class Watch
  def initialize(command)
    puts "(*) starting watch for #{command} ..."
    begin
      while true
        system("clear")
        system(command)
        sleep(5)
      end
    rescue Interrupt
      puts "(!) signal interrupt caught!"
    end
  end
end

begin
  cmd = ARGV.join(" ")
  Watch.new(cmd)
rescue
  puts usage
end


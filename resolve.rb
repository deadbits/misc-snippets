#!/usr/bin/env ruby

require 'resolv'

def pancakes(fin)
  start = Time.now
  File.open("#{fin}").each_line do |l|
    begin
      host = l.to_s.chomp
      puts "\nEntry: #{la}"
      puts Resolv.getaddress(host)
    rescue Exception
      puts "[!] error resolving #{host}"
    end
  end  
  finish = Time.now
  puts "\n[*] Took #{finish - start} seconds to complete!"
end

print "Enter input filename: "
fin = gets.chomp!
pancakes(fin)

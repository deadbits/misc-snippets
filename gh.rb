#!/usr/bin/env ruby
#
# quick hack job to parse ips from my nginx access logs
# and perform dns resolves against them. this probably wont
# work for everyone and has some bugs. took me all of 3 mins
# to write so its far from perfect. 
# better usage of this would be to add output file support
# or just pipe everything to a file like 
# ./gh.rb /var/log/nginx > hosts.txt
# 

require 'resolv'

def banner
  puts "\n\tparse log ips => dns"
  puts "  usage:\t./gh.rb <nginx log path>"
  puts "example:\t./gh.rb /var/log/nginx"
end

def get_dns(ip_list)
  ip_list.each do |addr|
    begin
      dns = Resolv.getname "#{addr}"
      puts "\nIP:\t#{addr}\nHost:\t#{dns}"
    rescue
      puts "\nIP:\t#{addr}\nHost:\tnot found"
    end
  end
  puts "[*] complete."
end

def parse_ips(log_name)
  @ip_list = []
  parsed = `cat #{log_name} | awk '{print $1}' | uniq` ; result=$?.success?
  if result
    ips = parsed.split("\n")
    ips.each do |addr|
      @ip_list.push(addr)
      puts "[~] parsed #{addr}"
    end
    get_dns(@ip_list)
  else
    puts "[!] error parsing log file #{log_name}"
    exit(1)
  end
end

def load_logs(log_path)
  @logs = []
  raise ArgumentError unless File.exists?(log_path)
  Dir.foreach(log_path) do |log_name|
    parse_ips("#{log_path}/#{log_name}") unless log_name.include?(".gz") or log_name.include?("error.log")
  end
end


log_path = ARGV[0]
if log_path
  load_logs(log_path)
else
  banner
  exit(1)
end



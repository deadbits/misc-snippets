#!/usr/bin/env ruby

require 'open-uri'
require 'nokogiri'
require 'rubygems'

def banner
  puts "\n\tdownforeveryoneorjustme.com"
  puts "\t   unofficial ruby script"
  puts "\t\tauthor: ohdae"
  puts "\n\tusage: ./down.rb <hostname>"
end

def pancakes(host)
  puts "[*] Checking host: #{host}..."
  all = Nokogiri::HTML(open("http://downforeveryoneorjustme.com/#{host}"))
  res = all.css("div").text.split("\n")[2]
  puts "[~] Result: "
  puts "    #{res}"
end

unless ARGV.length == 1
  banner
  exit
end

host = ARGV[0]
pancakes(host)



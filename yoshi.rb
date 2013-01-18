#!/usr/bin/env ruby
##
# ohdae [2013]
#
# TODO:
# - implement small database for storage and queries
# - perform virustotal checks
# - perform threatexpert checks
# - utilize yara for sig scanning
# - extend cli app to perform stored sample queries
# - add optparse support instead of ugly ARGV[0] ish
##

require 'open-uri'
require 'digest/md5'
require 'digest/sha1'
require 'json'
require 'net/http'

@base = "#{ENV['HOME']}/maz"

usage = "\n\tusage: ./yoshi.rb <filename or directory>"
desc = %{\tYoshi performs quick analysis and storage of malware samples.
\tYou can either supply an individual sample or a directory of samples, which
\tYoshi will iterate through and analyze each file. A unique storage directory
\tis created for each sample using the filename and md5 hash. When the analysis
\tis complete, this directory will contain the sample itself, ascii strings output,
\ta ShadowServer report if available, and a report file with basic information on
\tthe malware.}

def check_basic
  puts "[*] starting analysis of #{@file_name} ..."
  @info = {
    :name => @file_name,
    :type => `file #{@file_name}`.chomp,
    :time => Time.now,
    :size => File.size?(@file_name),
    :md5  => Digest::MD5.hexdigest(File.read(@file_name)),
    :sha1 => Digest::SHA1.hexdigest(File.read(@file_name))
  }
end

def shadow_query
  # borrowed mostly the shadowserver ruby gem
  @shadow = {}
  url = URI.parse("http://innocuous.shadowserver.org/api/?query=#{@info[:md5]}")
  request = Net::HTTP::Get.new("#{url.path}?#{url.query}")
  http = Net::HTTP.new(url.host, url.port)
  req = http.request(request)
  if not req.body.include?("No match found")
    result = req.body
    lines = result.split(/\n/)
    md5, sha1, first, last, type, ssdeep = lines[0].gsub(/\"/,'').split(/,/)
    avresults = JSON.parse(lines[1])
    @shadow = {
      :md5 => md5,
      :sha => sha1,
      :first => first,
      :last => last,
      :type => type,
      :ssdeep => ssdeep,
      :avres  => avresults
    }
  else
    puts "[!] no shadowserver match found!"
  end
  gen_output
end

def gen_output
  output = ""
  output << "\n  Filename:\t#{@file_name}"
  output << "\n      Size:\t#{@info[:size]}"
  output << "\n File Type:\t#{@info[:type]}"
  output << "\nSubmission:\t#{@info[:time]}"
  output << "\n  MD5 Hash:\t#{@info[:md5]}"
  output << "\n SHA1 Hash:\t#{@info[:sha1]}"
  if not @shadow.empty?
    output << "\n    Ssdeep:\t#{@shadow[:ssdeep]}"
    output << "\nFirst Seen:\t#{@shadow[:first]}"
    output << "\n Last Seen:\t#{@shadow[:last]}"
    output << "\n\n"
    output << "Anti-Virus Results: "
    @shadow[:avres].each_pair do |av|
      output << "\n#{av}"
    end
  end
  File.open("#{@p}/report.txt", 'w') do |fout|
    output.each_line do |line|
      fout.puts "#{line}"
    end
  end
  finish
end

def finish
  `strings #{@file_name} > #{@p}/strings.txt`
  puts "\n    sample name:\t#{@file_name}"
  puts "   storage path:\t#{@p}"
  puts "  ascii strings:\t#{@p}/strings.txt"
  puts "analysis report:#{@p}/report.txt\n"
end

def environment
  # TODO: add check if sample dir all ready exists so we dont crash yoshi!
  if File.directory?(@base)
    puts "[*] environment okay."
  else
    puts "[*] creating ~/maz directory ..."
    Dir.mkdir(@base)
    Dir.mkdir("#{@base}/samples")
  end
  check_basic
  full = "#{@base}/samples/#{File.basename(@file_name).chomp(File.extname(@file_name))}"
  @p = "#{full}_#{@info[:md5]}"
  Dir.mkdir(@p)
  `cp #{@file_name} #{@p}`
end  

def load_files(directory)
  puts "[*] loading samples from #{directory} ..."
  queue = []
  count = 0
  raise ArgumentError unless File.directory?(directory)
  Dir.foreach(directory) do |entry|
    if File.directory?(entry) == false
      path = File.join(directory, entry)
      queue << path
      count += 1
    end
  end
  puts "[*] loaded #{count} total samples!"
  queue.each do |s|
    @file_name = s
    environment 
    shadow_query
  end
  exit
end

# TODO: fix this because it's seriously very ugly and lame.
if ARGV[0] == nil
  puts usage
  puts desc
else
  if File.directory?(ARGV[0])
    load_files(ARGV[0])
  else
    @file_name = ARGV[0]
    if File.exist(@file_name) == false
      puts "[!] file cannot be found: #{@file_name}"
    end
    environment
    shadow_query
  end
end


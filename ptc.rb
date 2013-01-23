#!/usr/bin/env ruby
# Project Template Creator
# ohdae [ams] - 2013
# https://github.com/ohdae/misc-snippets


require 'trollop'

@dirs = [ "/bin/", "/conf", "/data", "/docs", "/lib", "/script", "/test" ]
@files = [ "/bin/application.rb", "/conf/config.yaml", "/data/placeholder", "/docs/README", "/docs/LICENSE", 
  "/docs/INSTALL", "/docs/GUIDE", "/script/console", "/script/destroy",
  "/script/generate", "/test/test_helper.rb", "/test/test_app.rb", "/Manifest.txt" ]

def build_dirs
  puts "[*] creating project directory structure ..."
  @dirs.each do |d|
    dir = @base + d
    Dir.mkdir("#{dir}")
    puts "\t - #{dir}"
  end
  Dir.mkdir("#{@base}/lib/#{@name}")
end

def build_files
  puts "[*] creating project file templates ..."
  @files.each do |f|
    file = @base + f
    `touch #{file}`
    puts "\t - #{file}"
  end
  `touch #{@base}/lib/#{@name}.rb`
  `touch #{@base}/lib/#{@name}/#{@name}.rb`
end

def staging
  @base = "#{@path}/#{@name}"
  puts "\nProject Name: #{@name}"
  puts "Project Base: #{@base}"
  unless File.directory?(@path)
    puts "[*] creating base directory: #{@path} ..."
    Dir.mkdir(@path)
  end
  puts "[*] creating project home: #{@base} ..."
  Dir.mkdir("#{@base}")
  build_dirs
  build_files
end

def main
  opts = Trollop::options do
    version = "version 1.0 :: 2013 :: ohdae [ams]"
    banner <<-EOS
      Project Template Creator [version 1.0]
      website: https://github.com/ohdae/

      ptc.rb is a script to generate a new environment for application development
      projects. PTC will automatically create the projects directory structure, documentation
      and license place holders, headers for your source code files and optionally initialize
      a new Git repository in the projects directory. The predefined directory and file structures
      might not be right for you and your code, but you can always edit the files and dirs list in
      the source of this script. 

        Usage: ptc.rb [options] [arguments]
      Example: ptc.rb --path /home/user/Git --name ptc
      This will create the base directory '/home/user/Git/ptc' with all the files and directories
      placed inside. * Do not include the trailing '/' at the end of your --path argument! *

      Options: 
      EOS
    opt :path, "Base project path", :type => String
    opt :name, "Project name", :type => String
    opt :git, "Initialize Git repository"
  end
  
  if opts[:path] and opts[:name]
    @path = opts[:path]
    @name = opts[:name]
    staging
  else
    puts "[error] you must supply both project name and project path arguments!"
    exit
  end
  if opts[:git]
    puts "[*] initializing Git repository in #{@path}/#{@name} ..."
    Dir.chdir("#{@path}/#{@name}")
    `git init`
  end
end

main

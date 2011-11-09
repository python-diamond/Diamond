watch('test/.*') { test }

Signal.trap('QUIT') { test }
Signal.trap('INT')  { abort("\n") }

def test()
  puts "*** Running..."
  %x{nosetests -v}
end

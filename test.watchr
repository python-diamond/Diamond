watch('src/(.*)\.py')     { go }
watch('test/(.*)\.py')    { go }
watch('test/fixtures/.*') { go }

Signal.trap('QUIT') { go }
Signal.trap('INT')  { abort("\n") }

def go()
  puts '*** Running...'
  %x{find . -name '*.pyc' -delete}
  %x{nosetests-2.7 -v}
end

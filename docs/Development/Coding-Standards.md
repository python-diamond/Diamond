# Coding Standards

## General

 * Unit tests are highly recommended
 * PEP-8
 * Documentation should be done docstr style at the start of the collector. This is how we generate the wiki
 * The use of positional arguments for functions is strongly discouraged.

## Collectors

 * Collector default configuration should be in the get_default_config method of the class
 * All collectors should verify before doing. For example, if the collector requires the existence of a file, check to verify that it exists and is readable before opening.
 * use small high-resolution units as default (such as bits or bytes).  this gives you most options afterwards.  note that graphite will show k/M/G etc prefixes by default if needed.

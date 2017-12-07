#!/usr/bin/env python3

import mobile_localization.cli
import sys

if __name__ == "__main__":
  print(sys.argv)
  if len(sys.argv) < 2 or sys.argv[1] != 'test':
    mobile_localization.cli.start()
  else:
    mobile_localization.cli.test()

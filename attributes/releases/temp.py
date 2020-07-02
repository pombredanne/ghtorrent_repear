from datetime import datetime
import arrow

start = datetime(2014, 1, 17)
end = datetime(2014, 6, 20)

for d in arrow.Arrow.range('day', end, start):
    print(d)
# Global imports
#import pandas as pd
# Local imports
import financedata as fd
reload(fd)
import simulator as si
reload(si)
import strategies as st
reload(st)

F = fd.FinanceData(name_list=fd.DAX)
S = si.Simulator(
					bankroll=10000,
					strategy=st.strategy_inter_day_even_hold_if_less,
					finance=F,
					fees=0
				)
X = S.run()

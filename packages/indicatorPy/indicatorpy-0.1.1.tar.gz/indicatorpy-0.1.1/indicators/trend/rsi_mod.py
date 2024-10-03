import numpy as np
def RSI(prices, n= 14):
      upsum = dnsum = 0.0000000000001
      deltas = np.diff(prices)
      seed = deltas[:n+1]
      up = seed[seed >= 0].sum()/n
      down = -seed[seed < 0].sum()/n
      rsi = np.zeros_like(prices)
      print("delta is ", deltas)
      for i in range(n, len(prices)):
            delta = deltas[i-1]

            if delta > 0:
                  upsum = ((n-1)*up + delta)/n
                  dnsum *= (n-1)/n

            else:
                  dnsum = ((n-1)*down-delta)/n
                  upsum *= (n-1)/n

            rsi[i] = (100 * (upsum/(upsum+dnsum))) - 50 
            # subtract50 to get the values at 0 in attempt to achieve stationarity
            if n == 2:
                  rsi[i] = -10.0 * np.log(2.0/(1+0.00999*(2*rsi[i] - 100)) -1 )

      return rsi

# def compute_RSI(lookback, close, output):
#       output = [0]*len(close)
#       lookback = lookback
#       front_bad = lookback  # Number of undefined values at start
#       back_bad = 0  # Number of undefined values at end

#       for icase in range(front_bad):
#             output[icase] = 0.0  # Set undefined values to neutral value

#     # Initialize
#       upsum = dnsum = 1.e-60
#       for icase in range(1, front_bad):
#             diff = close[icase] - close[icase - 1]
#             if diff > 0.0:
#                   upsum += diff
#             else:
#                   dnsum -= diff
#       upsum /= (lookback - 1)
#       dnsum /= (lookback - 1)

#       # Initialization is done. Start computing.
#       for icase in range(front_bad, len(close)):
#             diff = close[icase] - close[icase - 1]
#             if diff > 0.0:
#                   upsum = ((lookback - 1) * upsum + diff) / lookback
#                   dnsum *= (lookback - 1.0) / lookback
#             else:
#                   dnsum = ((lookback - 1) * dnsum - diff) / lookback
#                   upsum *= (lookback - 1.0) / lookback
#             output[icase] = 100.0 * upsum / (upsum + dnsum)
#             output[icase] -= 50
      
#       return output


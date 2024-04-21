import pandas as pd
import streamlit as st
import yfinance as yf
from plot import create_plot


def load_css(file_name):
    with open(file_name, "r") as f:
        style = f.read()
        st.markdown(f'<style>{style}</style>', unsafe_allow_html=True)

load_css('header.css')
st.markdown('<div class="glitch">DCA Calculator</div>', unsafe_allow_html=True)

tickers = ['BTC-USD', 'XRP-USD', 'TRX-USD', 'WAVES-USD', 'ZIL-USD', 'ONE-USD', 'COTI-USD', 'SOL-USD', 'EGLD-USD', 'AVAX-USD', 'NEAR-USD', 'FIL-USD', 'AXS-USD', 'ROSE-USD', 'AR-USD', 'MBOX-USD', 'YGG-USD', 'BETA-USD', 'PEOPLE-USD', 'EOS-USD', 'ATOM-USD', 'FTM-USD', 'DUSK-USD', 'IOTX-USD', 'OGN-USD', 'CHR-USD', 'MANA-USD', 'XEM-USD', 'SKL-USD', 'ICP-USD', 'FLOW-USD', 'WAXP-USD', 'FIDA-USD', 'ENS-USD', 'SPELL-USD', 'LTC-USD', 'IOTA-USD', 'LINK-USD', 'XMR-USD', 'DASH-USD', 'MATIC-USD', 'ALGO-USD', 'ANKR-USD', 'COS-USD', 'KEY-USD', 'XTZ-USD', 'REN-USD', 'RVN-USD', 'HBAR-USD', 'BCH-USD', 'COMP-USD', 'ZEN-USD', 'SNX-USD', 'SXP-USD', 'SRM-USD', 'SAND-USD', 'SUSHI-USD', 'YFII-USD', 'KSM-USD', 'DIA-USD', 'RUNE-USD', 'AAVE-USD', '1INCH-USD', 'ALICE-USD', 'FARM-USD', 'REQ-USD', 'GALA-USD', 'POWR-USD', 'OMG-USD', 'DOGE-USD', 'SC-USD', 'XVS-USD', 'ASR-USD', 'CELO-USD', 'RARE-USD', 'ADX-USD', 'CVX-USD', 'WIN-USD', 'C98-USD', 'FLUX-USD', 'ENJ-USD', 'FUN-USD', 'KP3R-USD', 'ALCX-USD', 'ETC-USD', 'THETA-USD', 'CVC-USD', 'STX-USD', 'CRV-USD', 'MDX-USD', 'DYDX-USD', 'OOKI-USD', 'CELR-USD', 'RSR-USD', 'ATM-USD', 'LINA-USD', 'POLS-USD', 'ATA-USD', 'RNDR-USD', 'NEO-USD', 'ALPHA-USD', 'XVG-USD', 'KLAY-USD', 'DF-USD', 'VOXEL-USD', 'LSK-USD', 'KNC-USD', 'NMR-USD', 'MOVR-USD', 'PYR-USD', 'ZEC-USD', 'CAKE-USD', 'HIVE-USD', 'UNI-USD', 'SYS-USD', 'BNX-USD', 'GLMR-USD', 'LOKA-USD', 'CTSI-USD', 'REEF-USD', 'AGLD-USD', 'MC-USD', 'ICX-USD', 'TLM-USD', 'MASK-USD', 'IMX-USD', 'XLM-USD', 'BEL-USD', 'HARD-USD', 'NULS-USD', 'TOMO-USD', 'NKN-USD', 'BTS-USD', 'LTO-USD', 'STORJ-USD', 'ERN-USD', 'XEC-USD', 'ILV-USD', 'JOE-USD', 'SUN-USD', 'ACH-USD', 'TROY-USD', 'YFI-USD', 'CTK-USD', 'BAND-USD', 'RLC-USD', 'TRU-USD', 'MITH-USD', 'AION-USD', 'ORN-USD', 'WRX-USD', 'WAN-USD', 'CHZ-USD', 'ARPA-USD', 'LRC-USD', 'IRIS-USD', 'UTK-USD', 'QTUM-USD', 'GTO-USD', 'MTL-USD', 'KAVA-USD', 'DREP-USD', 'OCEAN-USD', 'UMA-USD', 'FLM-USD', 'UNFI-USD', 'BADGER-USD', 'POND-USD', 'PERP-USD', 'TKO-USD', 'GTC-USD', 'TVK-USD', 'MINA-USD', 'RAY-USD', 'LAZIO-USD', 'AMP-USD', 'BICO-USD', 'CTXC-USD']

#Dropdown Box to select the coin
dropdown = st.selectbox('Select Your Cryptocurrency:',tickers, index=tickers.index('SOL-USD'))

#Dropdown to select date
start = st.date_input('Start Date of Investment:', value = pd.to_datetime('2021-02-14'))

#input box to enter investment amount
investment = st.number_input('Investment Amount:', value=100)

#input box to enter the frequency
frequency = st.text_input("Enter Frequency", value="M")
with st.expander("Frequency Format Guide"):
        st.write("""
        - 'D' : Daily
        - 'B' : Business days
        - 'W' : Weekly (default 'W-SUN')
        - 'M' : Month end
        - 'MS' : Month start
        - 'Q' : Quarter end
        - 'QS' : Quarter start
        - 'A' : Year end
        - 'AS' : Year start
        - 'H' : Hourly
        - 'T' or 'min' : Minute
        - 'S' : Second
        - Specify multiples, like '5D' for every five days, '3H' for every three hours, etc.
        """)

# Download historical data from Yahoo Finance for the selected cryptocurrency
df = yf.download(dropdown, start = start)

# Generate a series of purchase dates based on the given frequency
buydates = pd.date_range(df.index[0],df.index[-1], freq=frequency)

#Retrieve the daily closing prices on the specified purchase dates 
buyprices = df[df.index.isin(buydates)].Close

coin_amt = investment / buyprices

coin_amt_sum = coin_amt.cumsum()

coin_amt_sum.name = 'Coin_DCA'

df_final = pd.concat([coin_amt_sum, df], axis=1).ffill()

df_final['Portfolio_DCA']= df_final.Close * df_final.Coin_DCA

total_inv = investment*len(buyprices)
performance_DCA = (df_final['Portfolio_DCA'][-1]/ total_inv) - 1

##st.line_chart(df_final['Portfolio_DCA'])

# Create and display the plot
fig = create_plot(df_final)
st.plotly_chart(fig)

st.info('DCA Performance: '+ str(round( performance_DCA *100,2)) + '%')
st.info('Total Investment to Date: '+ '$'+ str(total_inv))
st.info('Todays Investment Amount: ' +'$'+ str(df_final['Portfolio_DCA'][-1]))
st.info('Total ' +str(dropdown.replace("-USD", ""))+ ' Accumulated: '+ str(coin_amt_sum[-1]))
import pandas as pd
from mdpython.account import reconcile

inp_fl = r"C:\Users\Dell\Onedrive\Desktop\input.xlsx"
out_fl = r"C:\Users\Dell\Onedrive\Desktop\output.xlsx"

disc_ar = [2, 2.5, 5, 10]

bill_df = pd.read_excel(inp_fl, usecols="B:C").dropna()
pymt_df = pd.read_excel(inp_fl, usecols="G:H").dropna()

recon = reconcile.reconcile_payment(
    bill_df=bill_df
    , pymt_df=pymt_df
    , bill_dt_col="Bill Date"
    , bill_amt_col="Bill Amount"
    , pymt_dt_col="Payment Date"
    , pymt_amt_col="Payment Amount"
    , disc_ar=disc_ar
)

recon.to_excel(out_fl)

print(recon.bill_dtl_df)
print(recon.pymt_dtl_df)
